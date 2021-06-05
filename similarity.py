class Similarity():

    def similarity_index(self,X , Y):
        m = len(X)
        n = len(Y)
        L = [[0] * (n+1)] * (m+1)
        for i in range(1, m+1):
            for j in range(1, n+1):
                if X[i-1] == Y[j-1]:
                    L[i][j] = L[i-1][j-1]+1
                else:
                    L[i][j] = max(L[i-1][j] , L[i][j-1])
        return max(m,n) - L[m][n]


    def place_selection(self,places, place_abbr, user_place):
        nearest_place = ''
        max_sim = 3
        n_places = []
        if user_place.strip() == '':
            return False, {} 
        for place in places:
            if user_place in place:
                n_places.append(place_abbr[place])
            sim_index = self.similarity_index(user_place, place)
            if sim_index == 0:
                return True, place_abbr[place]
            elif sim_index < max_sim:
                nearest_place = place
                max_sim = sim_index
        if nearest_place:
            n_places.append(place_abbr[nearest_place])
        return False, set(n_places)


    @staticmethod
    def parse_input(place):
        return ''.join(place.lower().split())


if __name__ == "__main__":
    import requests
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    req = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states', headers=headers)
    places = req.json()['states']
    users = {}
    id_lookup = {d['state_name'] : d['state_id'] for d in places}
    place_lookup = {id : place for place, id in id_lookup.items()}
    place_abbr = {''.join(place.lower().split()) : place  for place in id_lookup}
    places = {place for place in place_abbr}
# for place in places:
#     print(place)
    condition = False
    userplace = 'ter'
    sim = Similarity()
    userplace = sim.parse_input(userplace)
    while not condition:
        condition, place = sim.place_selection(places=places, place_abbr=place_abbr, user_place=userplace)
        if not condition:
            print(place)
            userplace = input("Enter the place name : ")
            userplace = sim.parse_input(userplace)
    print(place)
