class OAPI_Town:
    def __init__(self, data):
        timestamps = data['timestamps']
        status = data['status']
        stats = data['stats']

        self.timestamps = {
            'founded': timestamps['registered'],
            'joinedNation': timestamps['joinedNationAt']
        }

        strings = data['strings']
        self.name = strings['board']
        self.board = strings['board']
        self.colour = strings['mapColorHexCode']
        self.mayor = strings['mayor']
        self.founder = strings['founder']
        self.nation = data['affiliation']['nation']

        self.area = stats['numTownBlocks']
        self.x = data['home']['x']
        self.z = data['home']['z']

        self.residents = data['residents']
        self.spawn = data['spawn']

        perms = data['perms']
        rnaoPerms = perms['rnaoPerms']

        self.perms = {
            'switch': rnaoPerms['switchPerms'],
            'itemUse': rnaoPerms['itemUsePerms'],
            'build': rnaoPerms['buildPerms'],
            'destroy': rnaoPerms['destroyPerms']
        }

        self.flags = perms['flagPerms']
        self.ranks = data['ranks']

    def __repr__(self):
        str = "Name: %s \nNation: %s \nMayor: %s \nResidents: %s \nArea: %s \nX: %s \nZ: %s"
        list = (self.name, self.nation, self.mayor, self.residents, self.area, self.x, self.z)

        return str % list