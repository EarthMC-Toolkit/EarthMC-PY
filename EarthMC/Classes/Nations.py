from ..Utils import utilFuncs
utils = utilFuncs()

from .Towns import towns
from cachetools.func import ttl_cache

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
        
class nations(towns):
    def __init__(self, mapName):
        super().__init__(mapName)
        self.nations = self
        self.towns = towns(mapName)

        print("Created new 'nations' instance")

    @ttl_cache(4, 120)
    def get(self, nationName, nations=None):
        if nations is None: nations = self.all()
        foundNation = utils.find(lambda n: n['name'] == nationName, nations)

        if foundNation is None: return "Could not find nation '" + nationName + "'" 
        return foundNation

    @ttl_cache(16, 120)
    def all(self):
        raw = {}
        output = []

        for town in towns.all(self.towns):
            nationName = town["nation"]
            if nationName == 'No Nation': continue

            # Doesn't already exist, create new nation.
            if raw.get(nationName, None) == None:
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