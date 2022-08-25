from .Utils import utils
from .Nations import nations, Nation
from .Towns import towns, Town
from .OnlinePlayers import onlinePlayers, OnlinePlayer

# TODO: Add more map properties

class Map:
    def __init__(self, name=''): 
        if name.lower() != 'aurora' or 'nova': 
            return ValueError("Invalid map name!\nMust be 'aurora' or 'nova'")

        self.name = name

        totals = utils.getTotals()
        self.totalResidents = totals.residents
        self.totalTowns = totals.towns
        self.totalNations = totals.nations