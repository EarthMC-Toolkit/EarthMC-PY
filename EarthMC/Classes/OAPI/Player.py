class OAPI_Player:
    def __init__(self, data):
        self.name = data['name']
        self.nation = data['nation']
        self.town = data['town']
        self.balance = data['balance']
        self.registered = data['registered']

    def __repr__(self):
        str_template = (
            "Name: %s \nNation: %s \nTown: %s \nBalance: %s \nRegistered: %s"
        )
        info_list = (
            self.name, self.nation, self.town, self.balance, self.registered
        )

        return str_template % info_list
