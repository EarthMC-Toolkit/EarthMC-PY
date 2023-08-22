from EarthMC.Utils import AutoRepr

class OAPI_Player(AutoRepr):
    def __init__(self, data):
        self.name = data['name']
        self.nation = data['nation']
        self.town = data['town']
        self.balance = data['balance']
        self.registered = data['registered']