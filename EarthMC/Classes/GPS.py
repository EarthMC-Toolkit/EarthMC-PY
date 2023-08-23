from EarthMC.DataHandler import *
from cachetools.func import ttl_cache

class Gps:
    def __init__(self):
        self.url_player = f'https://earthmc.net/map/aurora/standalone/MySQL_update.php?world=earth'

    def fetch_players(self, player_name):
        try:
            response = requests.get(self.url_player)
            response.raise_for_status()
            player_data = {}

            pattern = f'<div class="player-info".*?name="{player_name}"[^>]*>(.*?)</div>'
            match = re.search(pattern, response.text, re.DOTALL)

            if match:
                player_data['name'] = player_name
                player_data['location'] = match.group(1).strip()
                return player_data  # Return the fetched player data

        except requests.exceptions.RequestException as e:
            print("Error fetching data:", e)
            return None  # Return None in case of error

    def fetch_towns(self, name):
        towns = OAPI.fetch_all(type="nations")
        town = towns.get(name)
        if town:
            town_spawn = town['spawn']
            return town_spawn
        return None

    def fetch_nations(self, name):
        nations = OAPI.fetch_all(type="nations")
        nation = nations.get(name)
        if nation:
            nation_spawn = nation['spawn']
            return nation_spawn
        return None

    def calculate_manhattan_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return abs(x2 - x1) + abs(y2 - y1)
    def shortest_route(self, nation_spawn, town_spawn, player_name='', town='', nation=''):

        player_location = self.fetch_players(player_name)['location']
        if isinstance(town, str):
            destination = self.fetch_towns(town)
        elif isinstance(nation, str):
            destination = self.fetch_nations(nation)
 
        if destination and player_location:
            distance = self.calculate_manhattan_distance(player_location, destination)
            return distance


