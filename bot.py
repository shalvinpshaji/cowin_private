from requests.models import RequestEncodingMixin
from similarity import Similarity
from user import User
from discord.ext import commands, tasks
import requests

from dotenv import load_dotenv
import api
import os

load_dotenv('.env')
TOKEN = os.environ.get('DISCORD_TOKEN')
GUILD = os.environ.get('DISCORD_GUILD')

sim = Similarity()


sim = Similarity()
client = commands.Bot(command_prefix='!')
users = {}

@client.command(name='register', help='Registers a user')
async def reg(ctx, username: str,age, *address):
    username = username.strip()
    if username == '' or len(address)==0:
        await ctx.send("Invalid arguments")
        return
    if username in users:
        await ctx.send('Username already taken, Try Again')
        return
    else:
        district = address[-1]
        state = ' '.join(address[:-1])
        state_dict = api.get_states()
        ret, states = sim.place_selection(state_dict['states'], state_dict['state_abbr'], state)
        states = list(states)
        if ret:
            dist_dict = api.get_districts(state_dict['id_lookup'][states[0]])
            ret1, districts = sim.place_selection(dist_dict['districts'], dist_dict['district_abbr'], district)
            districts = list(districts)
            if not ret1:
                k = ''
                for i in districts:
                    k = i +k+ '\n'
                await ctx.send(f'District not found \nSuggestions : \n {k}')
                return
            else:
                users[username] = User(username,age, state=states[0], district=districts[0], state_id=state_dict['id_lookup'][states[0]], district_id=dist_dict['id_lookup'][districts[0]])
                await ctx.send(f"Username {username} is created successfully")
                return
        else:
            k = ''
            for state in states:
                k = k + state+'\n'
            await ctx.send(f'State not found \nSuggestions : \n {k}')
            return
@client.command(name='info', help="Reply with the user's information")
async def info(ctx, username):
    if username not in users:
        await ctx.send(f'No user with name {username}')
        return
    u = users[username]
    k = f'Username : {u.username} \nAge : {u.age} \nState : {u.state} \nDistrict : {u.district}'
    await ctx.send(k)

client.command(name='delete', help='Delete the user')
async def delete(ctx, username):
    if username not in users:
        await ctx.send(f'No user with name {username}')
        return
    del users[username]
    await ctx.send(f'Username {username} is deleted')

@tasks.loop(minutes=1)
async def check_avail():
    for user in users:
        channel = client.get_channel(764056683294097420)
        r = api.get_appointment(users[user].district_id, users[user].age)
        if r:
            k = f'Doses available for {user} : \n' + '\n'.join(r)
            await channel.send(k)
        else:
            await channel.send(f'No doses available for {user} for next 4 days')
    

@client.event
async def on_ready():
    check_avail.start()
client.run(TOKEN)
