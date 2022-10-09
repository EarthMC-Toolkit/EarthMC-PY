from ..Utils import FetchError, utils
utils = utils()

class Town:
    def __init__(self, name="", nation="", mayor="", residents=[], area=0, x=0, z=0):
        self.name = name
        self.nation = nation
        self.mayor = mayor
        self.residents = residents
        self.area = area
        self.x = x
        self.z = z
    def __repr__(self):
        return "Name: %s \nNation: %s \nMayor: %s \nResidents: %s \nArea: %s \nX: %s \nZ: %s" % (self.name, self.nation, self.mayor, self.residents, self.area, self.x, self.z)
        
class towns:
    def __init__(self, map): self.mapName = map
    def all(self):
        townsArray, areas = []
        mapData = None
        
        try: 
            mapData = utils.mapData(self.mapName)

            if mapData is not None: areas = mapData["sets"]['townyPlugin.markerset']["areas"]
            else: raise FetchError
        except FetchError: print("Error fetching map data! Type is 'None'")

        townAreaNames = list(areas.keys())

        for i in range(len(townAreaNames)):
            town = areas[townAreaNames[i]]
            rawinfo = town["desc"].split("<br />")

            info = []

            for x in rawinfo:
                info.append(utils.striptags(x))

            townName = info[0].split(" (")[0].strip()         
            if townName.endswith("(Shop)"): continue
        
            mayor = info[1][7:]
            if mayor == "": continue

            nationName = info[0].split(" (")[1][0:-1] if "" else info[0].split(" (")[1][0:-1].strip()
            residents = info[2][9:].split(", ")

            area = utils.calcArea(town["x"], town["z"], len(town["x"]), 256)

            x = round((max(town["x"]) + min(town["x"])) / 2)
            z = round((max(town["z"]) + min(town["z"])) / 2)

            currentTown = Town(townName, nationName, mayor, residents, area, x, z)
            townsArray.append(currentTown)

        return townsArray
    def get(self, townName, towns=None):
        if towns is None: towns = self.all()
        foundTown = utils.find(lambda town: town.name == townName, towns)

        if foundTown is None: return "Could not find town '" + townName + "'" 
        return foundTown