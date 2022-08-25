from .Utils import utils
from .OnlinePlayers import onlinePlayers

utils = utils()
onlinePlayers = onlinePlayers()

class Town:
    def __init__(self, name="", nation="", mayor="", residents=[], x=0, z=0):
        self.name = name
        self.nation = nation
        self.mayor = mayor
        self.residents = residents
        self.x = x
        self.z = z
    def __repr__(self):
        return "Name: %s \nNation: %s \nMayor: %s \nResidents: %s \nX: %s \nZ: %s" % (self.name, self.nation, self.mayor, self.residents, self.x, self.z)

class towns:
    def all(self):
        mapData = utils.getMapData()
        townsArray = []

        if mapData is not None: townData = mapData["sets"]['townyPlugin.markerset']["areas"]
        else: raise ValueError("Map data is of type 'None'")

        townAreaNames = list(townData.keys())

        for i in range(len(townAreaNames)):
            town = townData[townAreaNames[i]]
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

            x = round((max(town["x"]) + min(town["x"])) / 2)
            z = round((max(town["z"]) + min(town["z"])) / 2)

            currentTown = Town(townName, nationName, mayor, residents, x, z)
            townsArray.append(currentTown)

        return townsArray
    def get(self, townName):
        return utils.find(lambda town: town.name == townName, self.all())