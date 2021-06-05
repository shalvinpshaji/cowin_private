class User:
    def __init__(self,username, age, state=None, district=None, state_id=None, district_id=None) -> None:
        self.username = username
        self.age = int(age)
        self.state = state
        self.district = district
        self.state_id = state_id
        self.district_id = district_id
