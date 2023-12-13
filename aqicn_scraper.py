import requests
import concurrent.futures
from geo2km import geo2km, geo2xy
from time import sleep
import numpy as np

# https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf
# https://en.wikipedia.org/wiki/Air_quality_index#Computing_the_AQI

aqi = [0,50,100,150,200,300,400,500]
c = {'o3': [0,54,70,85,105,200,404,504,604], # <404 for 8h, >=4048 for 1h
     'pm25': [0,12,35.4,55.4,150.4,250.4,350.4,500.4],
     'pm10': [0,54,154,254,354,424,504,604],
     'co': [0,4.4,9.4,12.4,15.4,30.4,40.4,50.4],
     'no2': [0,53,100,360,649,1249,1649,2049]}

def iaqi2SI(v, p):
    if p in c.keys():
        for j,a in enumerate(aqi[1:]):
            if v<=a:
                return (v-aqi[j])/(aqi[j+1]-aqi[j])*(c[p][j+1]-c[p][j])+c[p][j]
    else: return v

def interp2d(g):
    n = len(g)
    if n == 1:
        return [1]
    else: #todo3 change interpolation to Kriging
        A = np.ones((n,n))
        q = [(0,0),(1,0),(0,1),(1,1),(2,0),(0,2),(2,1),(1,2),(2,2),(3,0),(0,3),(3,1),(1,3),(3,2),(2,3),(3,3)]
    for j in range(1,n):
        A[:,j] = np.array([v[0]**q[j][0] * v[1]**q[j][1] for v in g])
#     print(A)
    return np.linalg.inv(A)[0,:]

def request_get(url):
    return requests.get(url=url)

def scraper(var, geo, stations,token): #todo1 put in seperate lib since geo scraper will also use it
    urls = ['https://api.waqi.info/feed/' + s + '/?token=' + token for s in stations]
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
        r = [executor.submit(request_get, url) for url in urls]
        concurrent.futures.wait(r)
    r = [v.result().json() for v in r]
    di = interp2d([geo2xy(*g['data']['city']['geo'],*geo) for g in r])
    print(di)
    return [sum([iaqi2SI(g['data']['iaqi'][p]['v'],p)*w for g,w in zip(r,di)]) for p in var]

if __name__ == "__main__":
#     print([[iaqi2SI(v,u) for v in aqi] for u in c])
    geo = [37.36927,-122.01275] # current position #todo1 update position from location service
    stations = ['A184858' , 'A224008', 'A201238','A246229','A13759'] #,'A224485','A153037'] #todo1 find closest stations st 0<w<1
    tkn = open('waqi_token.txt').read()
    vars = ['t', 'h', 'pm25']

    print(' '.join(['{:5}'.format(e) for e in vars]))
    while True:
        y = scraper(vars, geo, stations, tkn)
        print(' '.join(['{:5.1f}'.format(e) for e in y]))
        sleep(100)

    #todo2 report averages as (personal) (daily) (health) score
    #todo3 add (automatic) indicator for being indoors/vehicle or wearing mask
    #todo3 plot averages on map vs route followed
    #todo4 change/add past routes to update personal aqi score card
    #todo5 personal goals and rewards