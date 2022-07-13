from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Vaca")

location = geolocator.geocode("Troy NY")

print((location.latitude, location.longitude))