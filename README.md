# EarthMC Package

Provides info on the EarthMC Minecraft server. 

## Installation
```bash
$ pip install earthmc
```

## Import and instantiate classes
```py
from EarthMC import towns, nations, players

towns = towns()
nations = nations()
players = players()
```

## Methods
<details>
<summary>Player Related</summary>
<p>

### Get all online players
```py
onlinePlayers = players.allOnline()

print(onlinePlayers)

# => [{"x": 0, "y": 64, "z": 0, "isUnderground": true, "nickname": "PlayerNickname", "name": "PlayerName"}, ...]
```

### Get an online player
```py
op = players.getOnlinePlayer("PlayerName")

print(op)

# => {"x": 0, "y": 64, "z": 0, "isUnderground": true, "nickname": "PlayerNickname", "name": "PlayerName"}
```
</p>
</details>  

<details>
<summary>Town Related</summary>
<p>

### Get all towns
```py
allTowns = towns.all()

print(allTowns)

# => [{ area: 975, x: -352, z: -9904, name: 'TownName', nation: 'NationName', mayor: 'MayorName', residents: ['Resident', 'OtherResident', ...], pvp: false, mobs: false, public: false, explosion: false, fire: false, capital: true }, ...]
```

### Get a town by name
```py
town = towns.get("TownName")

print(town)

# => { area: 975, x: -352, z: -9904, name: 'TownName', nation: 'NationName', mayor: 'MayorName', residents: ['Resident', 'OtherResident', ...], pvp: false, mobs: false, public: false, explosion: false, fire: false, capital: true }
```
</p>
</details>

<details>
<summary>Nation Related</summary>
<p>

### Get all nations
```py
allNations = nations.all()

print(allNations)

# => [{ name: 'NationName', residents: ['Resident', 'OtherResident', ...], towns: ['Town', 'OtherTown', ...], king: 'KingName', capitalName: 'CapitalName', capitalX: -352, capitalZ: -9904, area: 7289 }, ...]
```

### Get a nation by name
```py
nation = nations.get("NationName")

print(nation)

# => { name: 'NationName', residents: ['Resident', 'OtherResident', ...], towns: ['Town', 'OtherTown', ...], king: 'KingName', capitalName: 'CapitalName', capitalX: -352, capitalZ: -9904, area: 7289 }
```
</p>
</details>  