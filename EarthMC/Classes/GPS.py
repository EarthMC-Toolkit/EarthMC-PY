from EarthMC import Maps
import math

Aurora = Maps.Aurora()
Nova = Maps.Nova()

class Location:
    def __init__(self, x, z):
        self.x = x
        self.z = z

class GPS:
    def __init__(self):
        self.map_aurora = Aurora()
        self.map_nova = Nova()

    def fetch_town(self, town_name, map_name):
        if map_name.lower() == 'aurora':
            town = self.map_aurora.Towns.get(town_name)
        elif map_name.lower() == 'nova':
            town = self.map_nova.Towns.get(town_name)
        else:
            return 'map didnt match any maps'

        if town:
            town_spawn = Location(town['x'], town['z'])
            global town_spawn

        return None

    def fetch_nation(self, nation_name, map_name):
        if map_name.lower() == 'aurora':
            nation = self.map_aurora.Nations.get(nation_name)
        elif map_name.lower() == 'nova':
            nation = self.map_nova.Nations.get(nation_name)
        else:
            return 'map didnt match any maps'

        if nation:
            capital = nation['capital']
            pvp = nation['pvp']
            public = nation['public']

            nation_spawn = Location(capital['x'], capital['z'])
            global nation_spawn

        return None

    @staticmethod
    def manhattan(loc1, loc2):
        return abs(loc2.x - loc1.x) + abs(loc2.z - loc2.z)

    def fastest_route(self, player_name='', town='', nation='', map_name=''):
        if map_name.lower() == 'aurora':
            player = self.map_aurora.Players.get(player_name)
        elif map_name.lower() == 'nova':
            player = self.map_nova.Players.get(player_name)
        else:
            return 'map didnt match any maps'

        if not player:
            return None

        player_location = Location(player['x'], player['z'])
        destination = None

        if isinstance(town, str):
            destination = self.fetch_town(town, map_name)
        elif isinstance(nation, str):
            destination = self.fetch_nation(nation, map_name)

        if destination and player_location and nation:
            distance = GPS.manhattan(player_location, destination)
            return f"nation:\n{nation}\nlocation: {nation_spawn}\ndistance: {distance}"

        if destination and player_location and town:
            distance = GPS.manhattan(player_location, destination)
            return f"town: {town}\nlocation: {town_spawn}\ndistance: {distance}"

        return None

    def safest_route(self, loc):
        nations = self.map_aurora.Nations.all() + self.map_nova.Nations.all()
        towns = self.map_aurora.Towns.all() + self.map_nova.Towns.all()
        filtered = []

        for nation in nations:
            capital = next((t for t in towns if t['name'] == nation['capital']['name']), None)

            if capital:
                flags = capital['flags']
                if not (flags['public'] or (flags['pvp'] and flags['mobs'])):
                    filtered.append(nation)

        min_distance, closest_nation = float('inf'), None

        for nation in filtered:
            dist = self.manhattan(nation['capital']['x'], nation['capital']['z'], loc.x, loc.z)

            if dist < min_distance:
                min_distance = dist
                closest_nation = {
                    'name': nation['name'],
                    'capital': nation['capital']
                }

        direction = self.cardinal_direction(closest_nation['capital'], loc)
        return {'nation': closest_nation, 'distance': round(min_distance), 'direction': direction}

    @staticmethod
    def cardinal_direction(loc1, loc2):
        delta_x = loc2.x - loc1['x']
        delta_z = loc2.z - loc1['z']

        angle_rad = math.atan2(delta_z, delta_x)
        angle_deg = (angle_rad * 180) / math.pi

        if -45 <= angle_deg < 45:
            return "east"
        elif 45 <= angle_deg < 135:
            return "north"
        elif angle_deg >= 135 or angle_deg < -135:
            return "west"
        else:
            return "south"
