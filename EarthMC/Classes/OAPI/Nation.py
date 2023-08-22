class OAPI_Nation:
    def __init__(self, data):
        timestamps = data['timestamps']
        stats = data['stats']

        self.timestamps = {
            'founded': timestamps['registered'],
        }

        strings = data['strings']

        self.board = strings['board']
        self.name = strings['nation']
        self.capital = strings['capital']
        self.king = strings['king']

        self.spawn = data['spawn']
        self.area = stats['numTownBlocks']
        self.residents = data['residents']
        self.towns = data['towns']

        self.allies = data['allies']
        self.enemies = data['enemies']
        self.color = strings['mapColorHexCode']

    def __repr__(self):
        str_template = (
            "Name: %s \nKing: %s \nCapital: %s \nResidents: %s \nArea: %s \nTowns: %s \n"
        )
        info_list = (
            self.name, self.king, self.capital, self.residents, self.area, self.towns
        )

        return str_template % info_list