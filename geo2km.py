# https://stackoverflow.com/questions/365826/calculate-distance-between-2-gps-coordinates
import math
def degreesToRadians(degrees):
    return degrees * math.pi / 180

def geo2km(lat1, lon1, lat2, lon2):
    earthRadiusKm = 6371

    dLat = degreesToRadians(lat2-lat1)
    dLon = degreesToRadians(lon2-lon1)

    lat1 = degreesToRadians(lat1)
    lat2 = degreesToRadians(lat2)

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));
    return earthRadiusKm * c

geo2km(37.371113,-122.01282,37.36927,-122.01275)