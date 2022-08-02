#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 12:07:09 2022

@author: ananyayadav
"""

import requests
import json


city = "San Diego"
state = "California"

url = "https://hotels4.p.rapidapi.com/locations/v2/search"

querystring = {"query": city + ", " + state,"locale":"en_US","currency":"USD"}

headers = {
	"X-RapidAPI-Key": "33625dbcd4msh979bc32938b510ep171a83jsn49d99e321daf",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

res = json.loads(response.text)
print(res)

dest_id = ""
#loop through all city results and find destination id of matching location
for x in res["suggestions"][0]["entities"]:
    if x["type"] == "CITY" and x["name"] == city:
        dest_id = x["destinationId"]
        break
        
    
print(dest_id)





def find_hotel(dest_id, dep_date, arr_date, stars):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": dest_id,"pageNumber":"1","pageSize":"1","checkIn": dep_date,"checkOut": arr_date,"adults1":"1","starRatings": stars,"sortOrder":"PRICE","locale":"en_US","currency":"USD"}

    headers = {
	"X-RapidAPI-Key": "33625dbcd4msh979bc32938b510ep171a83jsn49d99e321daf",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)

    #fill in hotel info
    hotel_info = {}
    path = res["data"]["body"]["searchResults"]["results"][0]
    hotel_info["name"] = path["name"]
    hotel_info["stars"] = path["starRating"]
    hotel_info["address"] = path["address"]["streetAddress"]
    hotel_info["city"] = path["address"]["locality"]
    hotel_info["state"] = path["address"]["region"]
    hotel_info["zip"] = path["address"]["postalCode"]
    hotel_info["cust_rating"] = path["guestReviews"]["rating"]
    hotel_info["tot_reviews"] = path["guestReviews"]["total"]
    hotel_info["price_per_night"] = path["ratePlan"]["price"]["current"]
    hotel_info["total_price"] = path["ratePlan"]["price"]["fullyBundledPricePerStay"]
    tourist_spots = path["landmarks"]
    hotel_info["attractions"] = tourist_spots
    return hotel_info


ny_id = "1506246"
sfo_id = "1483250"
dep_date = "2022-08-06"
arr_date = "2022-08-08"
stars = "4,5"

print(find_hotel(sfo_id, dep_date, arr_date, stars))

#*****get all ids for destinations*****