from ..Utils import utilFuncs
utils = utilFuncs()

from .Towns import towns

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
        
class nations:
    def __init__(self, map):
        self.towns = towns(map).all()
    def get(self, nationName, nations=None):
        if nations is None: nations = self.all()
        foundNation = utils.find(lambda n: n['name'] == nationName, nations)

        if foundNation is None: return "Could not find nation '" + nationName + "'" 
        return foundNation
    def all(self):
        nations = []
        raw = {}

        for town in self.towns:
            nationName = town["nation"]
            if nationName == 'No Nation': continue

            existing = raw.get(nationName, None)

            # Doesn't already exist, create new nation.
            if existing == None:
                existing = raw[nationName] = Nation(nationName)
                nations.append(vars(existing))

            # Add up existing values
            townName = town['name']
            existing.area += town['area']

            existing.residents.extend(town['residents'])
            existing.residents = list(dict.fromkeys(existing.residents))

            if existing.name == nationName:
                existing.towns.append(townName)
                existing.towns = list(dict.fromkeys(existing.towns))

            if town['flags']['capital'] is True:
                existing.king = town['mayor']
                existing.capital = {
                    'name': townName,
                    'x': town['x'], 
                    'z': town['z']
                }
            
            raw[nationName] = existing

        return nations