import requests
import concurrent.futures
from time import time
import numpy as np

def request_get(url):
    return requests.get(url=url)

def scraper(stations,token):
    urls = ['https://api.waqi.info/feed/A' + str(s) + '/?token=' + token for s in stations]
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
        r = [executor.submit(request_get, url) for url in urls]
        concurrent.futures.wait(r)
    r = [v.result().json() for v in r]
    return r
#     return [sum([iaqi2SI(g['data']['iaqi'][p]['v'],p)*w for g,w in zip(r,di)]) for p in var]

if __name__ == "__main__":
#     geo = [37.36927,-122.01275] # current position #todo1 update position from location service
    stations = range(184858,184898) #246229) # [1213,184858, 224008, 201238,246229,13759] #,'A224485','A153037'] #todo1 find closest stations st 0<w<1
    tkn = open('waqi_token.txt').read()
    t0 = time()
    r = scraper(stations, tkn)
    print('total time = %.1f s' % (dt:=time() -t0))
    d = {-v['data']['idx']: v['data']['city']['geo'] for v in r if v['status'] == 'ok'}
    print('polled/found stations: %.0f, %.0f (%.1f%%)' % (np := len(stations), ns := len(d), ns/np*100))
    print('API polls per second (max = 1000): %.0f' % (np / dt))
    
#     [print(k,v) for k,v in d.items()]