import math

def degreesToRadians(degrees):
    return degrees * math.pi / 180

def geo2km(lat1, lon1, lat2, lon2):
    # https://stackoverflow.com/questions/365826/calculate-distance-between-2-gps-coordinates
    earthRadiusKm = 6371

    dLat = degreesToRadians(lat2-lat1)
    dLon = degreesToRadians(lon2-lon1)

    lat1 = degreesToRadians(lat1)
    lat2 = degreesToRadians(lat2)

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));
    return earthRadiusKm * c

def geo2xy(lat1, lon1, lat2, lon2):
    # https://en.wikipedia.org/wiki/Latitude#Length_of_a_degree_of_latitude
    # https://en.wikipedia.org/wiki/Longitude#Length_of_a_degree_of_longitude
#     R = 6371
    
    dy = math.pi / 180 * (lat2-lat1) #* R
    dx = math.pi / 180 * (lon2-lon1) * math.cos(math.pi / 180 * lat1) #* R
    return dy, dx

if __name__ == "__main__":
    lat1, lon1 = 37.371113,-122.01282
    lat2, lon2 = 37.369270,-122.01275
    print(geo2km(lat1, lon1, lat2, lon2))
    dy, dx = geo2xy(lat1, lon1, lat2, lon2)
    print(6371*math.sqrt(dy**2+dx**2), dy, dx)