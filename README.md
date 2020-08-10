# EarthMC Package

Provides info on the EarthMC Minecraft server. 

## Installation
```bash
$ pip install earthmc
```

## Import and create Classes
```py
from src.Towns import towns
from src.Nations import nations
from src.Players import players

towns = towns()
nations = nations()
players = players()
```

## Methods
<details>
<summary>Player Related</summary>
<p>

### Get All Players
```py
allPlayers = players.all()

print(allPlayers)

// => [{"x": 0, "y": 64, "z": 0, "isUnderground": true, "nickname": "PlayerNickname", "name": "PlayerName"}, ...]
```

### Get Online Player
```py
op = players.getOnlinePlayer("PlayerName")

print(op)

// => {"x": 0, "y": 64, "z": 0, "isUnderground": true, "nickname": "PlayerNickname", "name": "PlayerName"}
</p>
</details>  