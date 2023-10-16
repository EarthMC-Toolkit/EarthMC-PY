from ..Utils import FetchError, utils, AutoRepr
from cachetools.func import ttl_cache
from ..DataHandler import Endpoint
endpoint = Endpoint()

class Town(AutoRepr):
    def __init__(self,
        name="", nation="No Nation",
        mayor="", area=0, x=0, z=0,
        residents=None, flags=None, colourCodes=None
    ):
        if residents is None:
            residents = []

        if flags is None:
            flags = {}

        if colourCodes is None:
            colourCodes = {}

        self.name = name
        self.nation = nation
        self.mayor = mayor
        self.area = area
        self.x = x
        self.z = z
        self.residents = residents
        self.flags = flags
        self.colourCodes = colourCodes

class Towns:
    def __init__(self, map_name):
        self.map_name = map_name
        print("Created new 'Towns' instance.")

    @ttl_cache(16, 120)
    def all(self):
        towns_array = []

        try:
            map_data = endpoint.fetch('map', self.map_name)
        except FetchError as e:
            print(e)
            return []

        markerset = map_data["sets"]['townyPlugin.markerset']
        areas = markerset['areas']
        town_area_names = list(areas.keys())

        for i in range(len(town_area_names)):
            town = areas[town_area_names[i]]
            raw_info = town["desc"].split("<br />")

            info = []

            for x in raw_info:
                info.append(utils.striptags(x))

            if "Shop" in info[0]:
                continue

            mayor = info[1][7:]
            if mayor == "":
                continue

            split = info[0].split(" (")
            nation_name = (split[1] if len(split) < 3 else split[2])[0:-1]
            residents = info[2][9:].split(", ")

            x = round((max(town["x"]) + min(town["x"])) / 2)
            z = round((max(town["z"]) + min(town["z"])) / 2)

            flags = {
                'pvp': utils.strAsBool(info[4][5:]),
                'mobs': utils.strAsBool(info[5][6:]),
                'public': utils.strAsBool(info[6][8:]),
                'explosions': utils.strAsBool(info[7][11:]),
                'fire': utils.strAsBool(info[8][6:]),
                'capital': utils.strAsBool(info[9][9:])
            }

            colourCodes = {
                'fill': town['fillcolor'],
                'outline': town['color']
            }

            ct = Town(
                name=utils.removeStyleCharacters(town['label']),
                mayor=mayor,
                area=utils.townArea(town),
                x=x, z=z,
                residents=residents,
                flags=flags,
                colourCodes=colourCodes
            )

            if nation_name != '':
                ct.nation = nation_name.strip()

            towns_array.append(ct)

        cached_towns: list[dict[str, Town]]  = []
        temp = {}

        for t in towns_array:
            if temp.get(t.name, None) is None:
                temp[t.name] = t
                cached_towns.append(vars(t))
            else:
                temp[t.name].area += t.area

        return cached_towns

    def get(self, town_name, towns=None):
        if towns is None:
            towns = self.all()
        found_town = utils.find(lambda town: town['name'].lower() == town_name.lower(), towns)

        if found_town is None:
            return "Could not find town '" + town_name + "'"
        return found_town

    def nearby(self, x_input, z_input, x_radius, z_radius, towns=None):
        if towns is None:
            towns = self.all()

        filtered_towns = []
        for t in towns:
            distance_x = t['x'] - x_input
            distance_z = t['z'] - z_input

            if -x_radius <= distance_x <= x_radius and -z_radius <= distance_z <= z_radius:
                filtered_towns.append(t)

        return filtered_towns if filtered_towns else []