from ..Utils import utils, FetchError, AutoRepr
from cachetools.func import ttl_cache

from ..DataHandler import Endpoint
endpoint = Endpoint()

class OnlinePlayer(AutoRepr):
    def __init__(self, player):
        self.name = player["account"]
        self.world = player["world"]
        self.x = player["x"]
        self.y = player["y"]
        self.z = player["z"]

class players:
    def __init__(self, map, towns):
        self.Towns = towns

        self.online = self.online(map)
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
            self.Towns = players.Towns

        @ttl_cache(8, 120)
        def all(self):
            output = []
            
            for t in self.Towns.all():
                for res in t['residents']:
                    output.append(res)

            return output

        def get(self, resName, resList=None):
            if resList is None: resList = self.all()
            foundRes = utils.find(lambda res: res.lower() == resName.lower(), resList)

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
                foundRes = utils.find(lambda res: res.lower() == p['name'].lower(), self.resList)
                if foundRes is not None: continue
                
                output.append(p)

            return output

    class online:
        def __init__(self, map):
            self.map = map

        @ttl_cache(8, 120)
        def all(self):
            output = []

            try: playerData = endpoint.fetch('players', self.map)
            except FetchError as e: 
                print(e)
                return []

            for op in playerData["players"]: 
                output.append(vars(OnlinePlayer(op)))

            return output

        def find(self, playerName): return self.get(playerName)

        def get(self, playerName, ops=None):
            if ops is None: ops = self.all()
            foundPlayer = utils.find(lambda player: player['name'].lower() == playerName.lower(), ops)
        
            if foundPlayer is None: return "Could not find player '" + playerName + "'" 
            return foundPlayer