# EarthMC Package
Provides data on people, places and more on the EarthMC Minecraft server.

## Install
```bash
$ pip install EarthMC
```

## Initialize Map(s)
```py
from EarthMC import Maps

Aurora = Maps.Aurora()
Nova = Maps.Nova()
```

## Methods
<details>
<summary>Players</summary>
<p>

#### **Base Reference**
```py 
ap = Aurora.Players
print(ap.all()) # => Outputs all players. (Townless and Residents)
```

#### **All** (List)
```py
online = ap.online.all() # => Outputs list of online players.
townless = ap.townless.all() # => Outputs list of townless players. (Online without a town)
residents = ap.residents.all() # => Outputs list of residents. 
```

#### **Get** (Object)
```py
op = ap.online.get('PlayerName')
tp = ap.townless.get('PlayerName')
res = ap.residents.get('ResidentName') 
```
</p>
</details>

## Official API
Similarly to the [EarthMC NPM](https://github.com/EarthMC-Toolkit/EarthMC-NPM) library, 
it is possible to send calls to EarthMC's [Official API](https://earthmc.net/docs/api).<br>
This includes Towny data like balances, timestamps, perms, ranks and more.

```py
from EarthMC import OfficialAPI

town = OfficialAPI.town('venice')
nation = OfficialAPI.nation('venice')
player = OfficialAPI.player('fix') 
```