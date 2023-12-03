import requests
from geo2km import geo2km
from iaqi2SI import iaqi2SI
from time import sleep

def scraper(var, geo, stations):
    urls = ['https://api.waqi.info/feed/' + s + '/?token=1c62da71e2174820957f6bd9cbd9fc2dfbaeb741' for s in stations]
    r = [requests.get(url).json() for url in urls]
    di = [1.0/geo2km(*g['data']['city']['geo'],*geo) for g in r]
    sd = sum(di)
    di = [v/sd for v in di]
#     [[print(g['data']['iaqi'][p]['v']) for g in r] for p in var]
    return [sum([iaqi2SI(g['data']['iaqi'][p]['v'],p)*w for g,w in zip(r,di)]) for p in var]

geo = [37.36927,-122.01275] # current position
stations = ['A184858', 'A201238', 'A224008']
vars = ['t', 'h', 'pm25']

print(' '.join(['{:5}'.format(e) for e in vars]))
while True:
    y = scraper(vars, geo, stations)
    print(' '.join(['{:5.1f}'.format(e) for e in y]))
    sleep(10)