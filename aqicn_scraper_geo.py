import requests
import concurrent.futures
from time import time
import json

with open ('waqi_stations.json', 'r') as f:
    y = json.load(f)
    
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
    tkn = open('waqi_token.txt').read()
    s, ds, np = 229900, 100, 0
    d = {}
    t0 = time()
    while s < 240000:
#         stations = : #184858,184878) #246229) # [1213,184858, 224008, 201238,246229,13759] #,'A224485','A153037'] #todo1 find closest stations st 0<w<1
        r = scraper(range(s,s+ds), tkn) 
        for v in r:
            if v['status'] == 'ok':
                d[-v['data']['idx']] = {'geo': v['data']['city']['geo'], 'qntt': list(v['data']['iaqi'].keys())} 
        s += ds; np += ds
        print('polled/found stations: %.0f, %.0f (%.1f%%)' % (np, ns := len(d), ns/np*100))
    dd = {str(k):v for k,v in d.items() if str(k) not in y.keys()}
    print('total time = %.1f s' % (dt:=time() -t0))
    print('API polls per second (max = 1000): %.0f' % (np / dt))
    print('new/old stations found: %.0f, %.0f' % (
        len(dd), sum([str(k) in y.keys() for k in d.keys()])))
#     y.update(dd)
#     with open ('waqi_stations.json', 'w') as f:
#         json.dump(y, f)
#     [print(k,v) for k,v in d.items()]