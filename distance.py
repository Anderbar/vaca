import geopy.distance
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Vaca")

location1 = geolocator.geocode("Troy NY")
location2 = geolocator.geocode("NYC")
coords1 = (location1.latitude, location1.longitude)
coords2 = (location2.latitude, location2.longitude)

print(coords1)
print(coords2)

print(geopy.distance.geodesic(coords1, coords2).miles,"miles")