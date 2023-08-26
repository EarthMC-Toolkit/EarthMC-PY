from EarthMC import Map
import math

class Location:
    def __init__(self, x, z):
        self.x = x
        self.z = z

class GPS:
    def __init__(self, map: Map):
        self.map = map # The parent Map the GPS was set up on.

    def fetch_location_town(self, town_name):
        location = self.map.Towns.get(town_name)

        if location:
            location_spawn = Location(location['x'], location['z'])
            global location_spawn

        return None

    def fetch_location_nation(self, nation_name):
        location = self.map.Nations.get(nation_name)

        if location:
            capital = location['capital']

            # Both unused?
            pvp = location['pvp']
            public = location['public']

            location_spawn = Location(capital['x'], capital['z'])
            global location_spawn

        return None

    @staticmethod
    def manhattan_distance(loc1, loc2):
        return abs(loc2.x - loc1.x) + abs(loc2.z - loc2.z)

    def find_fastest_route(self, player_name='', town='', nation=''):
        player = self.map.Players.get(player_name)

        if not player:
            return None

        player_location = Location(player['x'], player['z'])
        destination = None

        if isinstance(town, str):
            destination = self.fetch_location_town(town)
        elif isinstance(nation, str):
            destination = self.fetch_location_nation(nation)

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
            capital = nation['capital']
            dist = GPS.manhattan_distance(capital, loc)

            if dist < min_distance:
                min_distance = dist
                closest_nation = {
                    'name': nation['name'],
                    'capital': capital
                }

        direction = GPS.calculate_cardinal_direction(closest_nation['capital'], loc)
        return {
            'nation': closest_nation,
            'distance': round(min_distance),
            'direction': direction
        }

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
