import math
# import geocoder


def find_distance(lat1, lng1, lat2, lng2):
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLng = math.radians(lng2 - lng1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLng / 2)\
        * math.sin(dLng / 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d

# This script is used in profiles.adapter, look through its comments.
# def get_coordinates_from_ip(ip):
#     g = geocoder.ipinfo(ip)
#     return g.latlang
