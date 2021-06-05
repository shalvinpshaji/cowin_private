import requests
from datetime import date, timedelta


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
def get_states():
    req = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states', headers=headers)
    states = req.json()['states']
    id_lookup = {d['state_name'] : d['state_id'] for d in states}
    state_lookup = {id : state for state, id in id_lookup.items()}
    state_abbr = {''.join(state.lower().split()) : state  for state in id_lookup}
    states = {state for state in state_abbr}
    return {'states':states,'state_lookup': state_lookup,'id_lookup': id_lookup, 'state_abbr':state_abbr}

def get_districts(state_id):
    req = requests.get(f'https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}', headers=headers)
    districts = req.json()['districts']
    id_lookup = {d['district_name']: d['district_id'] for d in districts}
    district_lookup ={ dis_id: value for value, dis_id in id_lookup.items()}
    district_abbr = {''.join(district.lower().split()) : district  for district in id_lookup}
    districts = {district for district in district_abbr}
    return {'districts':districts,'district_lookup':district_lookup,'id_lookup': id_lookup, 'district_abbr':district_abbr}

def get_appointment(district_id, age):
    today = date.today()
    dates = [(today + timedelta(days=i)) for i in range(4)]
    dates = [d.strftime("%d-%m-%y") for d in dates]
    for d in dates:
        req = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={district_id}&date={d}'
        r = requests.get(req, headers=headers)
        sess = r.json()['sessions']
        ret = []
        for s in sess:
            name = s['name']
            cap = s['available_capacity']
            min_age_limit = s['min_age_limit']
            if cap > 0 and age >= int(min_age_limit):
               ret.append(f'{name} - Available dose-{cap} on {d}')
    return ret