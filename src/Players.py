from .Functions import functions

functions = functions()

class players:
    def __init__(self):
        self.methodsArray = ["all", "townless", "getOnlinePlayer", "getOnlinePlayers", "getResident", "getResidents"]
    def methods(self): return self.methodsArray
    def allOnline(self): return functions.getPlayerData()["players"]
    def getOnlinePlayer(self, playerName):
        onlinePlayerData = functions.getPlayerData()

        foundPlayer = functions.find(lambda x: x.get("account") == playerName, onlinePlayerData.get("players", []))

        if foundPlayer is None: return "Could not find player '" + playerName + "'" 
        else: return foundPlayer