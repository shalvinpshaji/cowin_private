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
        user_place = self.parse_input(user_place)
        if user_place.strip() == '':
            return False, {} 
        for place in places:
            if user_place in place:
                n_places.append(place_abbr[place])
            sim_index = self.similarity_index(user_place, place)
            if sim_index == 0:
                return True, {place_abbr[place]}
            elif sim_index < max_sim:
                nearest_place = place
                max_sim = sim_index
        if nearest_place:
            n_places.append(place_abbr[nearest_place])
        return False, set(n_places)


    @staticmethod
    def parse_input(place):
        return ''.join(place.lower().split())
