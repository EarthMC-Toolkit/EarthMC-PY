from cachetools.func import ttl_cache
from EarthMC.Utils import utils, FetchError
from EarthMC.DataHandler import OfficialAPI

class Players:
    def __init__(self, towns):
        self.towns = towns
        self.online = self.Online(self)
        self.residents = self.Residents(self)
        self.townless = self.Townless(self)

    @ttl_cache(2, 120)
    def all(self):
        names = self.residents.all() + [pl['name'] for pl in self.townless.all()]
        return names

    class Residents:
        def __init__(self, players):
            self.towns = players.towns

        @ttl_cache(8, 120)
        def all(self):
            output = [res for t in self.towns.all() for res in t['residents']]
            return output

        def get(self, resName, resList=None):
            if resList is None:
                resList = self.all()
            foundRes = utils.find(lambda res: res == resName, resList)
            return foundRes if foundRes else f"Could not find resident '{resName}'"

    class Townless:
        def __init__(self, players):
            self.resList = players.residents.all()
            self.ops = players.online.all()

        @ttl_cache(8, 120)
        def all(self):
            output = [p for p in self.ops if utils.find(lambda res: res == p['name'], self.resList) is None]
            return output

    class Online:
        def __init__(self, players):
            self.players = players
            self.official_api = OfficialAPI("player")  # Initialize the OfficialAPI instance

        @ttl_cache(8, 120)
        def all(self):
            try:
                playerData = self.players.official_api.get_info('players', self.players.map)
            except FetchError as e:
                print(e)
                return []

            output = [vars(OnlinePlayer(op)) for op in playerData["players"]]
            return output

        def find(self, playerName):
            return self.get(playerName)

        def get(self, playerName, ops=None):
            if ops is None:
                ops = self.all()
            foundPlayer = utils.find(lambda player: player['name'] == playerName, ops)
            return foundPlayer if foundPlayer else f"Could not find player '{playerName}'"

class OnlinePlayer:
    def __init__(self, player):
        self.name = player["account"]
        self.world = player["world"]
        self.x = player["x"]
        self.y = player["y"]
        self.z = player["z"]

    def __repr__(self):
        return f"Name: {self.name}\nWorld: {self.world}\nX: {self.x}\nY: {self.y}\nZ: {self.z}"

class Town:
    def __init__(self, name="", nation="No Nation", mayor="", area=0, x=0, z=0, residents=[], flags={}, colourCodes={}):
        self.name = name
        self.nation = nation
        self.mayor = mayor
        self.area = area
        self.x = x
        self.z = z
        self.residents = residents
        self.flags = flags
        self.colourCodes = colourCodes

    def __repr__(self):
        str = "Name: %s \nNation: %s \nMayor: %s \nResidents: %s \nArea: %s \nX: %s \nZ: %s"
        list = (self.name, self.nation, self.mayor, self.residents, self.area, self.x, self.z)
        return str % list

class Towns:
    def __init__(self, mapName):
        self.mapName = mapName
        print("Created new 'towns' instance.")

    @ttl_cache(16, 120)
    def all(self):
        townsArray = []

        try:
            official_api = OfficialAPI("town")  # Use OfficialAPI for fetching data
            mapData = official_api.get_info(self.mapName)  # API request here
        except FetchError as e:
            print(e)
            return []

        markerset = mapData["sets"]['townyPlugin.markerset']
        areas = markerset['areas']
        townAreaNames = list(areas.keys())

        cachedTowns = []
        temp = {}

        for i in range(len(townAreaNames)):
            town = areas[townAreaNames[i]]
            rawinfo = town["desc"].split("<br />")

            info = []

            for x in rawinfo:
                info.append(utils.striptags(x))

            if "Shop" in info[0]:
                continue

            mayor = info[1][7:]
            if mayor == "":
                continue

            split = info[0].split(" (")
            nationName = (split[1] if len(split) < 3 else split[2])[0:-1]
            residents = info[2][9:].split(", ")

            x = round((max(town["x"]) + min(town["x"])) / 2)
            z = round((max(town["z"]) + min(town["z"])) / 2)

            flags = {
                'pvp': utils.strAsBool(info[4][5:]),
                'mobs': utils.strAsBool(info[5][6:]),
                'public': utils.strAsBool(info[6][8:]),
                'explosions': utils.strAsBool(info[7][11:]),
                'fire': utils.strAsBool(info[8][6:]),
                'capital': utils.strAsBool(info[9][9:])
            }

            colourCodes = {
                'fill': town['fillcolor'],
                'outline': town['color']
            }

            ct = Town(
                name=utils.removeStyleCharacters(town['label']),
                mayor=mayor,
                area=utils.townArea(town),
                x=x, z=z,
                residents=residents,
                flags=flags,
                colourCodes=colourCodes
            )

            if nationName != '':
                ct.nation = nationName.strip()

            townsArray.append(ct)

        for t in townsArray:
            if temp.get(t.name, None) is None:
                temp[t.name] = t
                cachedTowns.append(utils.parseObject(t))
            else:
                temp[t.name].area += t.area

        return cachedTowns

    def get(self, townName, towns=None):
        if towns is None:
            towns = self.all()

        foundTown = utils.find(lambda town: town['name'] == townName, towns)

        if foundTown is None:
            return "Could not find town '" + townName + "'"
        return foundTown

class Nation:
    def __init__(self, name="", king="", capital="", residents=[], towns=[], area=0):
        self.name = name
        self.king = king
        self.capital = capital
        self.residents = residents
        self.towns = towns
        self.area = area

    def __repr__(self):
        str = "Name: %s \nKing: %s \nCapital: %s \nResidents: %s \nTowns: %s \nArea: %s \n"
        list = (self.name, self.king, self.capital, self.residents, self.towns, self.area)
        return str % list

class Nations:
    def __init__(self, mapName):
        self.towns = OfficialAPI.town(mapName)
        self.nations = self

        print("Created new 'nations' instance")

    @ttl_cache(4, 120)
    def get(self, nationName, nations=None):
        if nations is None:
            nations = self.all()
        foundNation = utils.find(lambda n: n['name'] == nationName, nations)

        if foundNation is None:
            return "Could not find nation '" + nationName + "'"
        return foundNation

    @ttl_cache(16, 120)
    def all(self):
        raw = {}
        output = []

        official_api = OfficialAPI("nation")  # Use OfficialAPI for fetching data
        towns_data = official_api.get_info(self.towns.mapName)  # API request for towns data

        for town in towns_data:
            nationName = town["nation"]
            if nationName == 'No Nation':
                continue

            # Doesn't already exist, create new nation.
            if raw.get(nationName, None) is None:
                raw[nationName] = Nation(
                    name=nationName,
                    residents=town['residents'],
                    towns=[],
                    area=0
                )

                output.append(vars(raw[nationName]))

            # Add up existing values
            townName = town['name']
            raw[nationName].area += town['area']

            raw[nationName].residents.extend(town['residents'])
            raw[nationName].residents = utils.listFromDictKey(raw[nationName].residents)

            if raw[nationName].name == town['nation']:
                raw[nationName].towns.append(townName)

            if town['flags']['capital'] is True:
                raw[nationName].king = town['mayor']
                raw[nationName].capital = {
                    'name': townName,
                    'x': town['x'],
                    'z': town['z']
                }

        return output