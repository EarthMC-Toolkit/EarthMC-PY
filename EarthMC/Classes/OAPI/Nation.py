class OAPI_Nation:
    def __init__(self, data):
        timestamps = data['timestamps']
        stats = data['stats']

        self.timestamps = {
            'founded': timestamps['registered'],
        }

        strings = data['strings']
        self.name = strings['board']
        self.board = strings['board']
        self.color = strings['mapColorHexCode']
        self.king = strings['king']
        self.capital = strings['capital']

        self.area = stats['numNationBlocks']
        self.residents = data['residents']
        self.towns = data['towns']

        perms = data['perms']
        self.rnao_perms = perms['rnaoPerms']
        self.flag_perms = perms['flagPerms']

        self.area = stats['numTownBlocks']
        self.x = data['home']['x']
        self.z = data['home']['z']

        self.allies = data['allies']
        self.enemies = data['enemies']

    def __repr__(self):
        str_template = (
            "Name: %s \nKing: %s \nCapital: %s \nResidents: %s \nArea: %s \nTowns: %s \n"
        )
        info_list = (
            self.name, self.king, self.capital, self.residents, self.area, self.towns
        )

        return str_template % info_list