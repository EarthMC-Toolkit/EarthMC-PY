from EarthMC.Utils import AutoRepr

class OAPI_Nation(AutoRepr):
    def __init__(self, data):
        timestamps = data['timestamps']
        stats = data['stats']

        self.timestamps = {
            'founded': timestamps['registered']
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

        self.public = data['public']
        self.pvp = strings['pvp']

        self.allies = data['allies']
        self.enemies = data['enemies']
        self.color = strings['mapColorHexCode']