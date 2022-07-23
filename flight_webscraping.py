#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 09:41:19 2022

@author: ananyayadav
"""

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import airportsdata
import geopy.distance
from geopy.geocoders import Nominatim

def find_airports(city, state):
    #find coordinates of starting location
    airports = airportsdata.load('IATA')
    geolocator = Nominatim(user_agent="Vaca")
    g_loc = geolocator.geocode(city + " " + state)
    loc_coords = (g_loc.latitude, g_loc.longitude)

    #search for international airports within 2.5 lat/lon from starting location   
    dict1 = {}     
    for x in airports.keys():
        if "International" in airports[x]['name']: 
            if airports[x]['lat'] >= (loc_coords[0] - 2.5) and airports[x]['lat'] <= (loc_coords[0] + 2.5):
                if airports[x]['lon'] >= (loc_coords[1] - 2.5) and airports[x]['lon'] <= (loc_coords[1] + 2.5):
                    airport_coords = (airports[x]['lat'], airports[x]['lon'])
                    dist = geopy.distance.geodesic(loc_coords, airport_coords).miles
                    dict1.update({dist: x})
    #create list of airports in order of distance from starting location
    airport_list = []
    for i in sorted(dict1.keys()):
        airport_list.append(dict1[i])
    print(airport_list)
    return airport_list
        

def make_flight_url(dep_loc, arr_loc, dep_date, arr_date):
    browser = "https://www.kayak.com/flights/" + dep_loc + "-" + arr_loc + "/" + dep_date + "/" + arr_date + "?sort=price_a&fs=stops=~0"
    return browser

#Close popups that appear in flight pages
def close_popup(driver):
        try:
            popUp_button = driver.find_elements_by_xpath('//button[contains(@id, "dialog-close") and contains(@class, "Button-No-Standard-Style close ")]')
            popUp_button[5].click()
            time.sleep(15)
        except:
            pass

#check if kayak was able to find results
def info_found(driver):
    try:
        wait_object(driver, '//div[@class = "col col-banner center"]')
        return False
    except:
        return True

#details for flight to travel destination (includes price)
def scrape_start_flight_data(driver):
    price = driver.find_element_by_xpath('//span[@class="price option-text"]/span[1]').text
    duration = driver.find_element_by_xpath('//div[@class="section duration allow-multi-modal-icons"]/div[1]').text
    airport_str = driver.find_element_by_xpath('//div[@class="section duration allow-multi-modal-icons"]/div[2]').text
    start_airport = format_airports(airport_str)[0]
    end_airport = format_airports(airport_str)[1]
    time = driver.find_element_by_xpath('//div[@class="section times"]/div[1]').text
    airline = driver.find_element_by_xpath('//div[@class="section times"]/div[2]').text
    return duration, start_airport, end_airport, time, airline, price


#details for flight to starting location (includes url to kayak options)
def scrape_end_flight_data(driver):
    duration = driver.find_element_by_xpath('//li[@class="flight "]//div[@class="section duration allow-multi-modal-icons"]/div[1]').text
    airport_str = driver.find_element_by_xpath('//li[@class="flight "]//div[@class="section duration allow-multi-modal-icons"]/div[2]').text
    start_airport = format_airports(airport_str)[0]
    end_airport = format_airports(airport_str)[1]
    time = driver.find_element_by_xpath('//li[@class="flight "]//div[@class="section times"]/div[1]').text
    airline = driver.find_element_by_xpath('//li[@class="flight "]//div[@class="section times"]/div[2]').text
    url = driver.current_url
    return duration, start_airport, end_airport, time, airline, url
    
#reformat string with airports information for a flight
def format_airports(airports):
    l = airports.split("\n")
    l.pop(1)
    return l

#chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument('window-size=1200x600')
#driver = webdriver.Chrome(options=chrome_options)

def wait_object(driver, xpath):
    return WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    
def get_info(dep_city, dep_state, arr_code, dep_date, arr_date):
    
    driver = webdriver.Chrome()
    airport_list = find_airports(dep_city, dep_state)
    for x in airport_list:
        driver.get(make_flight_url(x, arr_code, dep_date, arr_date))
        close_popup(driver)
        #kayak contain flight info, gather data and end loop
        if info_found(driver):
            flight1 = scrape_start_flight_data(driver)
            flight2 = scrape_end_flight_data(driver)
            print(flight1)
            print(flight2)
            driver.quit()
            break
        #kayak has no flights for this airport, look at next closest airport
        else:
            print("No Info Found")
            continue
        
#need full city and state
dep_city = "Shelton"
dep_state = "Connecticut"
arr_loc = "SFO"
dep_date = "2022-08-06"
arr_date = "2022-08-08"


get_info(dep_city, dep_state, arr_loc, dep_date, arr_date)







    

