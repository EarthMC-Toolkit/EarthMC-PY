from EarthMC import Map
import math

class Location:
    def __init__(self, x, z):
        self.x = x
        self.z = z

class GPS:
    def __init__(self, map: Map):
        self.map = map

    def fetch_location_town(self, location_name, map_name):
        if map_name.lower() == 'aurora':
            location = self.map.Towns.get(location_name)
        elif map_name.lower() == 'nova':
            location = self.map.Towns.get(location_name)
        else:
            return 'map didnt match any maps'

        if location:
            location_spawn = Location(location['x'], location['z'])
            global location_spawn

        return None

    def fetch_location_nation(self, location_name, map_name):
        location = self.map.Nations.get(location_name)

        if location:
            capital = location['capital']
            pvp = location['pvp']
            public = location['public']

            location_spawn = Location(capital['x'], capital['z'])
            global location_spawn

        return None

    @staticmethod
    def manhattan_distance(loc1, loc2):
        return abs(loc2.x - loc1.x) + abs(loc2.z - loc2.z)

    def find_fastest_route(self, player_name='', town='', nation='', map_name=''):
        player = self.map.Players.get(player_name)

        if not player:
            return None

        player_location = Location(player['x'], player['z'])
        destination = None

        if isinstance(town, str):
            destination = self.fetch_location_town(town, map_name)
        elif isinstance(nation, str):
            destination = self.fetch_location_nation(nation, map_name)

        if destination and player_location and nation:
            distance = GPS.manhattan_distance(player_location, destination)
            return f"nation:\n{nation}\nlocation: {location_spawn}\ndistance: {distance}"

        if destination and player_location and town:
            distance = GPS.manhattan_distance(player_location, destination)
            return f"town: {town}\nlocation: {location_spawn}\ndistance: {distance}"

        return None

    def find_safest_route(self, loc):
        nations = self.map.Nations.all()
        towns = self.map.Towns.all()

        filtered = []

        for nation in nations:
            capital = next((t for t in towns if t['name'] == nation['capital']['name']), None)

            if capital:
                flags = capital['flags']
                if not (flags['public'] or (flags['pvp'] and flags['mobs'])):
                    filtered.append(nation)

        min_distance, closest_nation = float('inf'), None

        for nation in filtered:
            dist = self.manhattan_distance(nation['capital']['x'], nation['capital']['z'], loc.x, loc.z)

            if dist < min_distance:
                min_distance = dist
                closest_nation = {
                    'name': nation['name'],
                    'capital': nation['capital']
                }

        direction = self.calculate_cardinal_direction(closest_nation['capital'], loc)
        return {'nation': closest_nation, 'distance': round(min_distance), 'direction': direction}

    @staticmethod
    def calculate_cardinal_direction(loc1, loc2):
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
