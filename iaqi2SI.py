# https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf
# https://en.wikipedia.org/wiki/Air_quality_index#Computing_the_AQI

aqi = [0,50,100,150,200,300,400,500]
c = {'o3': [0,54,70,85,105,200,404,504,604], # <404 is 8h, after 1h
     'pm25': [0,12,35.4,55.4,150.4,250.4,350.4,500.4],
     'pm10': [0,54,154,254,354,424,504,604],
     'co': [0,4.4,9.4,12.4,15.4,30.4,40.4,50.4],
     'no2': [0,53,100,360,649,1249,1649,2049]}

def iaqi2SI(v, p):
    if p in c.keys():
        for j,a in enumerate(aqi[1:]):
            if v<=a:
                return (v-aqi[j])/(aqi[j+1]-aqi[j])*(c[p][j+1]-c[p][j])+c[p][j]
    else:
        return v

[[iaqi2SI(v,u) for v in aqi] for u in c]