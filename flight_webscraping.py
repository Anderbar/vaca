#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 12:40:10 2022

@author: ananyayadav
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def make_flight_url(dep_loc, arr_loc, dep_date, arr_date):
    browser = "https://www.kayak.com/flights/" + dep_loc + "-" + arr_loc + "/" + dep_date + "/" + arr_date + "?sort=price_a&fs=stops=~0"
    return browser


def close_popup():
        """ Close popups that appear on flight pages"""
        try:
            popUp_button = driver.find_elements_by_xpath('//button[contains(@id, "dialog-close") and contains(@class, "Button-No-Standard-Style close ")]')
            popUp_button[5].click()
            time.sleep(15)
        except:
            pass

#details for flight to travel destination (includes price)
def scrape_start_flight_data():
    
    price = driver.find_element_by_xpath('//span[@class="price-text"]').text

    
    duration = driver.find_element_by_xpath('//div[@class="section duration allow-multi-modal-icons"]/div[1]').text
    airport_str = driver.find_element_by_xpath('//div[@class="section duration allow-multi-modal-icons"]/div[2]').text
    start_airport = format_airports(airport_str)[0]
    end_airport = format_airports(airport_str)[1]
    time = driver.find_element_by_xpath('//div[@class="section times"]/div[1]').text
    airline = driver.find_element_by_xpath('//div[@class="section times"]/div[2]').text
    return duration, start_airport, end_airport, time, airline, price


#details for flight to starting location
def scrape_end_flight_data():

    duration = driver.find_element_by_xpath('//li[@class="flight "]//div[@class="section duration allow-multi-modal-icons"]/div[1]').text
    airport_str = driver.find_element_by_xpath('//li[@class="flight "]//div[@class="section duration allow-multi-modal-icons"]/div[2]').text
    start_airport = format_airports(airport_str)[0]
    end_airport = format_airports(airport_str)[1]
    time = driver.find_element_by_xpath('//li[@class="flight "]//div[@class="section times"]/div[1]').text
    airline = driver.find_element_by_xpath('//li[@class="flight "]//div[@class="section times"]/div[2]').text
    return duration, start_airport, end_airport, time, airline
    

def format_airports(airports):
    l = airports.split("\n")
    l.pop(1)
    return l

#Inputs
dep_loc = "NYC"
arr_loc = "SFO"
dep_date = "2022-08-15"
arr_date = "2022-08-22"

#Launch Kayak website
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(make_flight_url(dep_loc, arr_loc, dep_date, arr_date))
time.sleep(1)

close_popup()


#div[@aria-label='Result number 1']

flight1 = scrape_start_flight_data()
flight2 = scrape_end_flight_data()

url = driver.current_url

print(flight1)
print(flight2)

#driver.quit()

#issues: nonstop, +1, # of travelers, city codes, links
#add ons-> options for flight (nonstop, 1 stop, 2 stop+), # of travelers

#city codes -> for final destination, manually input codes
#for starting, need to figure out how to get airports