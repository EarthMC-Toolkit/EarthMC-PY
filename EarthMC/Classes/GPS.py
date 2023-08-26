from enum import Enum

from EarthMC import Map
import math
from ..Utils import utils

from typing import TypedDict

LocationType = TypedDict('LocationType', { 'x': int, 'z': int })
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
    def __init__(self, map: Map):
        self.map = map # The parent Map the GPS was set up on.

    def fetch_location_town(self, town_name):
        town = self.map.Towns.get(town_name)

        if town:
            location_spawn = Location(town['x'], town['z'])

        return None

    def fetch_location_nation(self, nation_name):
        nation = self.map.Nations.get(nation_name)

        if nation:
            capital = nation['capital']

            # Both unused?
            pvp = nation['pvp']
            public = nation['public']
            location_spawn = Location(capital['x'], capital['z'])

        return None

    def find_route(self, loc: LocationType, route: Route):
        return None

    def find_safest_route(self, loc: LocationType):
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
            dist = utils.manhattan_distance(capital, loc)

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
