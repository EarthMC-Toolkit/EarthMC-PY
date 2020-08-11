from .Functions import functions

functions = functions()

class towns:
    def __init__(self):
        self.methodsArray = ["all", "get"]
    def methods(self): return self.methodsArray
    def all(self):
        return "Not created yet."
    def get(self, townName):
        return "Not created yet."

        # mapData = functions.getMapData()
        # #playerData = functions.getPlayerData()

        # #townsArray = [], townsArrayNoDuplicates = []

        # if mapData is not None: townData = mapData["sets"]['townyPlugin.markerset']["areas"]
        # else: return

        # townAreaNames = townData.keys()

        # for i in range(len(townAreaNames)):
        #     town = townData["townAreaNames"[i]]
        #     rawinfo = town["desc"].split("<br />")

        #     info = []

        #     for x in rawinfo:
        #         soup = BeautifulSoup(x)
        #         info.append(soup.get_text())