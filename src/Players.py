import json, requests

def find(pred, iterable):
    for element in iterable:
        if pred(element):
            return element
    return None

def getPlayerData():
    return requests.get("https://earthmc.net/map/up/world/earth/").json()

class players:
    def __init__(self):
        self.methods = ["all", "townless", "getOnlinePlayer", "getOnlinePlayers", "getResident", "getResidents"]
    def printMethods(self):
        for method in self.methods:
            print('\t%s ' % method)
    def getOnlinePlayer(self, playerName):
        onlinePlayerData = getPlayerData()

        foundPlayer = find(lambda x: x.get("account") == playerName, onlinePlayerData.get("players", []))

        if foundPlayer is None: return "Could not find player '" + playerName + "'" 
        else: return foundPlayer
    def all(self):
        return getPlayerData()["players"]