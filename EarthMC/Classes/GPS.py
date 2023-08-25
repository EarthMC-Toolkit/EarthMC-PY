from EarthMC import Map

class Location:
    def __init__(self, x: int, z: int):
        self.x = x
        self.z = z

class GPS:
    def __init__(self, map: Map):
        self.map = map

    def fetch_town(self, town_name: str):
        town = self.map.Towns.get(town_name)

        if town:
            town_spawn = Location(town['x'], town['z'])
            return town_spawn

        return None

    def fetch_nation(self, nation_name: str):
        nation = self.map.Nations.get(nation_name)

        if nation:
            capital = nation['capital']
            nation_spawn = Location(capital['x'], capital['z'])
            return nation_spawn

        return None

    @staticmethod
    def manhattan(loc1, loc2):
        return abs(loc2.x - loc1.x) + abs(loc2.z - loc2.z)

    def fastest_route(self, player_name='', town='', nation=''):
        player = self.map.Players.get(player_name)
        if not player:
            return None

        player_location = Location(player['x'], player['z'])
        destination = None

        if isinstance(town, str):
            destination = self.fetch_town(town)
        elif isinstance(nation, str):
            destination = self.fetch_nation(nation)

        if destination and player_location:
            distance = GPS.manhattan(player_location, destination)
            return distance

        return None