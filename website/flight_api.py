import time
import airportsdata
import geopy.distance
from geopy.geocoders import Nominatim
import requests
import json


def find_airports(location):
    #find coordinates of starting location
    airports = airportsdata.load("IATA")
    geolocator = Nominatim(user_agent = "Vaca")
    g_loc = geolocator.geocode(location)
    loc_coords = (g_loc.latitude, g_loc.longitude)

    #search for closest international airport from starting location   
    airport_info = {}     
    for x in airports.keys():
        if "International" in airports[x]["name"] and airports[x]["country"] == "US": 
            airport_coords = (airports[x]["lat"], airports[x]["lon"])
            dist = geopy.distance.geodesic(loc_coords, airport_coords).miles
            if len(airport_info) == 0 or dist < airport_info["distance"]:
                airport_info["name"] = airports[x]["iata"]
                airport_info["distance"] = dist
    #return airport code and distance from starting location (mi)
    return airport_info


def get_api_info(origin, dest, travelers, dep_date, arr_date):
    #Access Skyscanner API
    url = "https://skyscanner44.p.rapidapi.com/search"
    querystring = {"adults": travelers,"origin": origin,"destination": dest,"departureDate": dep_date, "returnDate": arr_date, "currency":"USD"}
    headers = {
	"X-RapidAPI-Key": "33625dbcd4msh979bc32938b510ep171a83jsn49d99e321daf",
	"X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    #convert response text to dict
    res = json.loads(response.text)
    #print(res)
    ct = 0
    #let API gather data
    #can only have 10 requests within a minutes so loop breaks once 30 seconds have passed
    
    while res["context"]["status"] == "incomplete":
        time.sleep(5)
        ct += 5
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)
        if len(res["itineraries"]) != 0 or ct == 30:
            break
    return res

def find_flight_info(origin, dest, travelers, dep_date, arr_date):
    res = get_api_info(origin, dest, travelers, dep_date, arr_date)
    all_info = {}
    #API gives information of the top 3 cheapest flights
    for x in range(len(res['itineraries']['buckets'][2]["items"])):
        path1 = res['itineraries']['buckets'][2]["items"][x]
        #get link to specific flight
        all_info["link" + str(x)] = path1["deeplink"]
        #get all information of the cheapest flight
        if x == 0:
            all_info["price"] = path1["price"]["raw"]
            all_info["link0"] = path1["deeplink"]
            all_info["trip duration"] = path1["legs"][0]["durationInMinutes"]
            #outbound flight information
            outbound_info = []
            for y in path1["legs"][0]["segments"]:
                leg_info = {}
                leg_info["origin"] = y["origin"]["flightPlaceId"]
                leg_info["dest"] = y["destination"]["flightPlaceId"]
                leg_info["duration"] = y["durationInMinutes"]
                leg_info["dep_time"] = y["departure"]
                leg_info["arr_time"] = y["arrival"]
                leg_info["airline"] = y["marketingCarrier"]["name"]
                leg_info["flight"] = y["marketingCarrier"]["alternateId"] + y["flightNumber"]
                outbound_info.append(leg_info)
            #return flight information
            return_info = []
            for y in path1["legs"][1]["segments"]:
                leg_info = {}
                leg_info["origin"] = y["origin"]["flightPlaceId"]
                leg_info["dest"] = y["destination"]["flightPlaceId"]
                leg_info["duration"] = y["durationInMinutes"]
                leg_info["dep_time"] = y["departure"]
                leg_info["arr_time"] = y["arrival"]
                leg_info["airline"] = y["marketingCarrier"]["name"]
                leg_info["flight"] = y["marketingCarrier"]["alternateId"] + y["flightNumber"]
                return_info.append(leg_info)
            all_info["outbound"] = outbound_info
            all_info["return"] = return_info
        #only get links for other flight options (done above) 
        else:
            continue
    return all_info

"""
dest = "SFO"
travelers = "1"
dep_date = "2022-08-06"
arr_date = "2022-08-08"


city = "New York, NY"
airport = find_airports(city)

print(find_flight_info(airport["name"], dest, travelers, dep_date, arr_date))
"""

