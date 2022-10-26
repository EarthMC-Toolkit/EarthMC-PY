from ..Utils import FetchError, utilFuncs
utils = utilFuncs()

from cachetools.func import ttl_cache

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
        
class towns:
    def __init__(self, mapName):
        self.mapName = mapName
        self.towns = self
        
        print("Created new 'towns' instance.")

    @ttl_cache(16, 120)
    def all(self):
        townsArray = []
        markerset = {}
        mapData = None

        try: 
            mapData = utils.fetchData('map', self.mapName)

            if mapData is not None: markerset = mapData["sets"]['townyPlugin.markerset']
            else: raise FetchError
        except FetchError: print("Error fetching map data! Type is 'None'")

        areas = markerset['areas']
        townAreaNames = list(areas.keys())

        for i in range(len(townAreaNames)):
            town = areas[townAreaNames[i]]
            rawinfo = town["desc"].split("<br />")

            info = []

            for x in rawinfo:
                info.append(utils.striptags(x))
     
            if "Shop" in info[0]: continue
    
            mayor = info[1][7:]
            if mayor == "": continue

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

            if (nationName != ''):
                ct.nation = nationName.strip()

            townsArray.append(ct)
            
        cachedTowns = []
        temp = {}

        for t in townsArray:
            if temp.get(t.name, None) == None: 
                temp[t.name] = t
                cachedTowns.append(vars(t))
            else: temp[t.name].area += t.area

        return cachedTowns
    def get(self, townName, towns=None):
        if towns is None: towns = self.all()
        foundTown = utils.find(lambda town: town['name'] == townName, towns)

        if foundTown is None: return "Could not find town '" + townName + "'" 
        return foundTown