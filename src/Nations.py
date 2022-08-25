from .Utils import utils
utils = utils()

class Nation:
    def __init__(self, name="", king="", capital="", residents=[], towns=[]):
        self.name = name
        self.king = king
        self.capital = capital
        self.residents = residents
        self.towns = towns
    def __repr__(self):
        return "Name: %s \nKing: %s \nCapital: %s \nResidents: %s \nTowns: %s \n" % (self.name, self.king, self.capital, self.residents, self.towns)

class nations:
    def all(self): return NotImplementedError