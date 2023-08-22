from ..Utils import utils, AutoRepr

from .Towns import towns
from cachetools.func import ttl_cache

class Nation(AutoRepr):
    def __init__(self, name="", king="", capital="", residents=None, towns=None, area=0):
        if towns is None:
            towns = []

        if residents is None:
            residents = []

        self.name = name
        self.king = king
        self.capital = capital
        self.residents = residents
        self.towns = towns
        self.area = area

class nations:
    def __init__(self, mapName):
        self.towns = towns(mapName)
        self.nations = self

        print("Created new 'nations' instance")

    @ttl_cache(4, 120)
    def get(self, nationName, nations=None):
        if nations is None:
            nations = self.all()

        foundNation = utils.find(lambda n: n['name'].lower() == nationName.lower(), nations)
        if foundNation is None:
            return "Could not find nation '" + nationName + "'"

        return foundNation

    @ttl_cache(16, 120)
    def all(self):
        raw = {}
        output = []

        for town in self.towns.all():
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