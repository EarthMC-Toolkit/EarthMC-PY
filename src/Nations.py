from .Functions import functions

functions = functions()

class Nation:
    def __init__(self, name="", king="", capital="", residents=[], towns=[]):
        self.name = name
        self.king = king
        self.capital = capital
        self.residents = residents
        self.towns = towns
    def __repr__(self):
        return "Name: %s \nKing: %s \nCapital: %s \nResidents: %s \nTowns: %s \n" % (self.name, self.king, self.capital, self.residents, self.towns)

def createNation(name, king, capital, residents, towns):
    return Nation(name, king, capital, residents, towns)

class nations:
    def all(self): return NotImplementedError