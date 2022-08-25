# EarthMC Package
Provides data on people, places and more on the EarthMC Minecraft server.

## Install
```bash
$ pip install EarthMC
```

## Import Map(s)
```py
from EarthMC import Aurora, Nova
```

## Methods
<details>
<summary>Players</summary>
<p>

```py 
ap = Aurora.players
print(ap()) # => Outputs all players. (Townless and Residents)
```

#### All (List)
```py
online = ap.online.all()
townless = ap.townless.all()
residents = ap.residents.all() 
```

#### Get (Object)
```py
op = ap.online.get('PlayerName')
tp = ap.townless.get('PlayerName')
res = ap.residents.get('ResidentName') 
```
</p>