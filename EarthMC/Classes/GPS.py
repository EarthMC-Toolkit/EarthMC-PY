from enum import Enum
from EarthMC import Map
import math
from ..Utils import utils

from typing import TypedDict

import asyncio
from pyee import EventEmitter

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

class GPS(EventEmitter):
    map: Map
    emitted_underground: bool
    last_loc: {}

    def __init__(self, map: Map):
        # Initialize event emitter
        super().__init__()

        # Used when `track()` is called.
        self.emitted_underground = False
        self.last_loc = None

        # The parent Map the GPS was set up on.
        self.map = map

    def get_town_location(self, town_name):
        town = self.map.Towns.get(town_name)

        if town:
            location_spawn = Location(town['x'], town['z'])

        return None

    def get_nation_location(self, nation_name):
        nation = self.map.Nations.get(nation_name)

        if nation:
            capital = nation['capital']

            # Both unused?
            pvp = nation['pvp']
            public = nation['public']
            location_spawn = Location(capital['x'], capital['z'])

        return None

    async def track(self, player_name: str, interval=3000, route: Route = None):
        if route is None:
            route = {
                "avoidPvp": False,
                "avoidPublic": False
            }

        async def track_interval():
            while True:
                player = await self.map.Players.get(player_name)
                if not player["world"]:
                    self.emit("error", {
                        "err": "INVALID_PLAYER",
                        "msg": "Player is offline or does not exist!"
                    })

                    return

                underground = (player["x"] == 0 and player["z"] == 0 and
                               player["world"] != "some-other-bogus-world")

                if underground:
                    if not self.emitted_underground:
                        self.emitted_underground = True

                        if not self.last_loc:
                            self.emit("underground", "No last location. Waiting for this player to show.")
                            return

                        try:
                            route_info = self.find_route(self.last_loc, route)
                            self.emit("underground", {"lastLocation": self.last_loc, "routeInfo": route_info})
                        except Exception as e:
                            self.emit("error", {"err": "INVALID_LAST_LOC", "msg": str(e)})
                else:
                    loc = {
                        "x": player["x"],
                        "z": player["z"]
                    }
                    self.last_loc = loc

                    try:
                        route_info = self.find_route(loc, route)

                        self.emit("locationUpdate", route_info)
                    except Exception as e:
                        self.emit("error", {"err": "INVALID_LOC", "msg": str(e)})

                await asyncio.sleep(interval / 1000)

        asyncio.create_task(track_interval())

    def find_route(self, loc: LocationType, route: Route):
        # TODO: Implement route finder
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
