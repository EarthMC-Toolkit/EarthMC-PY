from EarthMC.Utils import AutoRepr

class OAPI_Player(AutoRepr):
    def __init__(self, data):
        strings = data['strings']
        affiliation = data['affiliation']
        timestamps = data['timestamps']
        perms = data['perms']
        stats = data['stats']
        status = data['status']

        self.title = strings['title']
        self.name = strings['username']
        self.surname = strings['surname']

        if len(affiliation) != 0:
            if 'town' in affiliation:
                self.town = affiliation['town']

            if 'nation' in affiliation:
                self.nation = affiliation['nation']

        self.balance = stats['balance']
        self.online = status['isOnline']

        self.timestamps = {
            "registered": timestamps['registered'],
            "joinedTown": timestamps['joinedTownAt'],
            "lastOnline": timestamps['lastOnline']
        }

        rnaoPerms = perms['rnaoPerms']
        self.perms = {
            "build": rnaoPerms['buildPerms'],
            "destroy": rnaoPerms['destroyPerms'],
            "switch": rnaoPerms['switchPerms'],
            "itemUse": rnaoPerms['itemUsePerms']
        }

        self.flags = perms['flagPerms']
        self.ranks = data['ranks']
        self.friends = data['friends']