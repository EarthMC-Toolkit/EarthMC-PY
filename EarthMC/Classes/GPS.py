import requests
import re
from EarthMC.DataHandler import OAPI
from cachetools.func import ttl_cache

class Gps():
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
                return player_data

        except requests.exceptions.RequestException as e:
            print("Error fetching data:", e)
            return None

    def parse_location_coordinates(self, location_string):
        match = re.search(r'x=(-?\d+)&y=(-?\d+)', location_string)
        if match:
            x, y = int(match.group(1)), int(match.group(2))
            return x, y
        return None

    def fetch_towns(self, name):
        towns = OAPI.fetch_all(type="nations")
        town = towns.get(name)
        if town:
            town_spawn = self.parse_location_coordinates(town['spawn'])
            return town_spawn
        return None

    def fetch_nations(self, name):
        nations = OAPI.fetch_all(type="nations")
        nation = nations.get(name)
        if nation:
            nation_spawn = self.parse_location_coordinates(nation['spawn'])
            return nation_spawn
        return None

    def calculate_manhattan_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return abs(x2 - x1) + abs(y2 - y1)

    def shortest_route(self, player_name='', town='', nation=''):
        player_data = self.fetch_players(player_name)
        if not player_data:
            return None

        player_location = self.parse_location_coordinates(player_data['location'])

        if isinstance(town, str):
            destination = self.fetch_towns(town)
        elif isinstance(nation, str):
            destination = self.fetch_nations(nation)

        if destination and player_location:
            distance = self.calculate_manhattan_distance(player_location, destination)
            return distance
        return None