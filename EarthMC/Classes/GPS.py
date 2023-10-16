from enum import Enum
import math

from .Towns import Town
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
    avoid_pvp: bool
    avoid_public: bool

    def __init__(self, pvp, public):
        self.avoid_pvp = pvp
        self.avoid_public = public

class Route(Enum):
    SAFEST = RouteOptions(True, True)
    FASTEST = RouteOptions(False, False)
    AVOID_PVP = RouteOptions(True, False)
    AVOID_PUBLIC = RouteOptions(False, True)

class RouteInfo:
    nation: object
    distance: int
    direction: str

    def __init__(self, nation, distance, direction):
        self.nation = nation
        self.distance = distance
        self.direction = direction

class GPS(EventEmitter):
    map: None
    emitted_underground: bool
    last_loc: {}

    def __init__(self, map):
        # Initialize event emitter
        super().__init__()

        # Used when `track()` is called.
        self.emitted_underground = False
        self.last_loc = None

        # The parent Map the GPS was set up on.
        self.map = map

    async def track(self, player_name: str, interval=3000, route: RouteOptions = Route.FASTEST.value):
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

    def find_safest_route(self, loc: LocationType):
        return self.find_route(loc, Route.SAFEST.value)

    def find_fastest_route(self, loc: LocationType):
        return self.find_route(loc, Route.FASTEST.value)

    def find_route(self, loc: LocationType, route: RouteOptions):
        towns = self.map.Towns.all()
        nations = self.map.Nations.all()

        filtered = []
        for n in nations:
            capital: Town = next((t for t in towns if t.name == n['capital']['name']), None)
            if capital is None: continue

            PVP = route.avoid_pvp and capital.flags['pvp']
            PUBLIC = route.avoid_public and (capital.flags['public'] is None)
            if PVP or PUBLIC: continue

            filtered.append(n)

        if len(filtered) < 1:
            return None

        distance, nation = 0.0, None
        for n in filtered:
            closest = GPS.find_closest(distance, n, loc)
            distance, nation = closest['distance'], closest['nation']

        direction = GPS.cardinal_direction(nation['capital'], loc)
        return RouteInfo(nation, distance, direction)

    @staticmethod
    def find_closest(dist, nation, loc: LocationType):
        capital = nation["capital"]
        curDist = utils.manhattan_distance(capital, loc)

        if dist < curDist:
            return dist

        return {
            "distance": round(curDist),
            "nation": {
                "name": nation["name"],
                "capital": capital
            }
        }

    @staticmethod
    def cardinal_direction(loc1: LocationType, loc2: LocationType):
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
