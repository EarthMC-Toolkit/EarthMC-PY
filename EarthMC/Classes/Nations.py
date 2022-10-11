from ..Utils import utilFuncs
utils = utilFuncs()

class Nation:
    def __init__(self, name="", king="", capital="", residents=[], towns=[], area=0):
        self.name = name
        self.king = king
        self.capital = capital
        self.residents = residents
        self.towns = towns
        self.area = area
    def __repr__(self):
        str = "Name: %s \nKing: %s \nCapital: %s \nResidents: %s \nTowns: %s \n"
        list = (self.name, self.king, self.capital, self.residents, self.towns)
        return str % list 
        
class nations:
    def __init__(self, map):
        self.mapName = map 
        print(map)

    def all(self): return NotImplementedError