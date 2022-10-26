from ..Utils import utilFuncs
utils = utilFuncs()

from cachetools.func import ttl_cache

class OnlinePlayer:
    def __init__(self, player):
        self.name = player["account"]
        self.world = player["world"]
        self.x = player["x"]
        self.y = player["y"]
        self.z = player["z"]
    def __repr__(self):
        return "Name: %s \nWorld: %s \nX: %s \nY: %s \nZ: %s" % (self.name, self.world, self.x, self.y, self.z)

class players:
    def __init__(self, map):
        self.playerData = utils.fetchData('players', map)

        self.online = self.online(self)
        self.residents = self.residents(self)
        self.townless = self.townless(self)

    @ttl_cache(2, 120)
    def all(self): 
        names = []
        names.extend(self.residents.all())

        for pl in self.townless.all():
            names.append(pl['name'])
            
        return names

    class residents: 
        def __init__(self, players):
            self.towns = players.towns

        @ttl_cache(8, 120)
        def all(self):
            output = []
            
            for t in self.towns.all():
                for res in t['residents']:
                    output.append(res)

            return output

        def get(self, resName, resList=None):
            if resList is None: resList = self.all()
            foundRes = utils.find(lambda res: res == resName, resList)

            if foundRes is None: return "Could not find resident '" + resName + "'" 
            return foundRes    

    class townless:
        def __init__(self, players):
            self.resList = players.residents.all()
            self.ops = players.online.all()

        @ttl_cache(8, 120)    
        def all(self):
            output = []

            for p in self.ops:
                foundRes = utils.find(lambda res: res == p['name'], self.resList)
                if foundRes is not None: continue
                
                output.append(p)

            return output

    class online:
        def __init__(self, players): 
            self.ops = players.playerData["players"]

        @ttl_cache(8, 120)
        def all(self):
            output = []
            
            for op in self.ops: 
                output.append(vars(OnlinePlayer(op)))

            return output

        def find(self, playerName): return self.get(playerName)
        def get(self, playerName, ops=None):
            if ops is None: ops = self.all()
            foundPlayer = utils.find(lambda player: player['name'] == playerName, ops)
        
            if foundPlayer is None: return "Could not find player '" + playerName + "'" 
            return foundPlayer