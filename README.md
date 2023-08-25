# EarthMC-PY
An **unofficial** Python package for interacting with both the [Official](https://earthmc.net/docs/api) 
and [Dynmap](https://earthmc.net/map/aurora/) EarthMC APIs.<br>
This package is part of the [EarthMC Toolkit](https://emctoolkit.vercel.app) and provides 
extensive info on people, places and more.

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

## Usage Example
```py
from EarthMC import Maps, OfficialAPI
Aurora = Maps.Aurora()

ops = Aurora.Players.all()

def format(res):
    return res.name + ": " + str(round(res.balance))

def onlineBalTop():
    residents = []

    for op in ops:
        res = OfficialAPI.player(op['name'])
        residents.append(res)

    return list(map(format, sorted(residents, key=lambda r: r.balance, reverse=True)))

print(onlineBalTop())
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