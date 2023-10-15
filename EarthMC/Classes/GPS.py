from enum import Enum
import time
import math
from EarthMC.Utils import utils
from typing import TypedDict

LocationType = TypedDict('LocationType', {'x': int, 'z': int})
class Location:
    def __init__(self, x, z):
        self.x = x
        self.z = z


class RouteOptions:
    def __init__(self, pvp, public):
        self.avoid_pvp = pvp
        self.avoid_public = public



class Route(Enum):

    SAFEST = RouteOptions(True, True)
    FASTEST = RouteOptions(False, False)
    AVOID_PVP = RouteOptions(True, False)
    AVOID_PUBLIC = RouteOptions(False, True)



class GPS:
    def __init__(self,map ):
        self.map = map # The parent Map the GPS was set up on.

    def manhattan_distance(self,loc1, loc2):

        return abs(loc2 - loc1) + abs(loc2 - loc1)
    def fetch_location_town(self, town_name):
        town = self.map.Towns.get(town_name)

        if town:
            location_spawn = Location(town['x'], town['z'])

        return None

    def fetch_location_nation(self, nation_name):
        nation = self.map.Nations.get(nation_name)

        if nation:
            capital = nation['capital']


            pvp = nation['pvp']
            public = nation['public']
            location_spawn = Location(capital['x'], capital['z'])

        return None

    async def find_route(self,loc:LocationType, options,map_name:str):
        if not loc['x']:
            x = loc['x']
            print( f'Invalid {x}')

        elif not loc['z']:
            z = loc['z']
            print(f'Invalid {z}')

        towns = self.map.Towns.all()
        nations = self.map.Nations.all()
        filtered = []

        for nation in nations:
            capital = next((t for t in towns if t['name'] == nation['capital']['name']), None)
            if not capital:
                continue

            flags = capital['flags']
            PVP = options['avoidPvp'] and flags['pvp']
            PUBLIC = options['avoidPublic'] and not flags['public']
            if PVP or PUBLIC:
                continue

            filtered.append(nation)

        result = filtered[0] if filtered else None
        if result:
            min_dist = None
            closest_nation = None
            for nation in filtered:
                dist = utils.manhattan(nation['capital']['x'], nation['capital']['z'], loc['x'], loc['z'])
                if not min_dist or dist < min_dist:
                    min_dist = dist
                    closest_nation = {
                        'name': nation['name'],
                        'capital': nation['capital']
                    }

            direction = self.calculate_cardinal_direction(closest_nation['capital'], loc)
            return {
                'nation': closest_nation,
                'distance': round(min_dist),
                'direction': direction
            }

        return None

    def find_safest_route(self, loc:LocationType):
        nations = self.map.Nations.all()
        towns = self.map.Towns.all()

        filtered = []

        for nation in nations:
            capital = next((t for t in towns if t['name'] == nation['capital']['name']), None)

            if capital:
                flags = capital['flags']
                if not (flags['public'] or flags['pvp']):
                    filtered.append(nation)

        min_distance, closest_nation = float('inf'), None

        for nation in filtered:
            capital = nation['capital']

            dist = self.manhattan_distance(capital,loc)

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
    def calculate_cardinal_direction(loc1: LocationType, loc2: LocationType):
        delta_x = loc2['x'] - loc1['x']
        delta_z = loc2['z'] - loc1['z']

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

class Tracker:
    def __init__(self, x, z,map):
        self.x = x
        self.z = z
        self.Map = map


        self.current_players_aurora = {}
        self.current_players_nova = {}
        self.old_players_aurora = {}
        self.old_players_nova = {}

    def retrieve_and_update_players(self):
        self.current_players_aurora = self.Map.Players.all
        self.current_players_nova = self.Map.Players.all
        self.old_players_aurora = self.current_players_aurora.copy()
        self.old_players_nova = self.current_players_nova.copy()

    def run(self):
        while True:
            self.retrieve_and_update_players()
            time.sleep(60)

    def track_player(self, player_name, map_name):
        player = None

        if map_name.lower() == 'aurora':
            player = self.current_players_aurora.get(player_name)

        elif map_name.lower() == 'nova':
            player = self.current_players_nova.get(player_name)

        if player:
            location = Location(player['x'], player['z'])

            if map_name.lower() == 'aurora':
                if player_name in self.current_players_aurora:
                    print(f'Current location of {player_name}: {location}')

                elif player_name in self.old_players_aurora:
                    old_location_aurora = self.old_players_aurora[player_name]
                    print(f'Last known location of {player_name}: {old_location_aurora}')

            elif map_name.lower() == 'nova':
                if player_name in self.current_players_nova:
                    print(f'Current location of {player_name}: {location}')
                elif player_name in self.old_players_nova:
                    old_location_nova = self.old_players_nova[player_name]
                    print(f'Last known location of {player_name}: {old_location_nova}')

        print(f'Player {player_name} not found on {map_name} map')
