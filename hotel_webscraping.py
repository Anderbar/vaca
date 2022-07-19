#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 17:35:27 2022

@author: ananyayadav
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

def close_popup():
        """ Close popups that appear on flight pages"""
        try:
            popUp_button = driver.find_elements_by_xpath('//button[contains(@id, "dialog-close") and contains(@class, "Button-No-Standard-Style close ")]')
            popUp_button[5].click()
            time.sleep(15)
        except:
            pass

def update_url(url, dep, arr, stars):
    l = url.split("/")
    l[5] = dep
    l[6] = arr
    new_url = "/".join(l) 
    new_url = new_url + "?sort=price_a&fs=stars=*" + str(stars)
    return new_url

#Launch Kayak website
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.kayak.com/stays")
time.sleep(1)

close_popup()

stars = 3
dest = "San Francisco, California"
dep_date = "2022-08-15"
arr_date = "2022-08-22"

#Only insert location into search option -> each location has unique code given by Kayak
#All other filters will be done through URL
elem = driver.find_element_by_xpath('//input[@class = "k_my-input"]')
elem.send_keys(dest)
time.sleep(1)
elem.send_keys(Keys.ARROW_DOWN)
time.sleep(1)
elem.send_keys(Keys.RETURN)
driver.find_element_by_xpath('//button[@type = "submit"]').click()
time.sleep(1)
url = driver.current_url
new_url = update_url(url, dep_date, arr_date, stars)
print(new_url)
time.sleep(10)


driver.quit()

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(new_url)
time.sleep(5)

price = driver.find_element_by_xpath('//div[@class = "zV27-price"]').text
name = driver.find_element_by_xpath('//div[@class = "FLpo-hotel-name"]').text
stars = driver.find_element_by_xpath('//div[@class = "FLpo-stars"]/div[1]').get_attribute("class")
rating = stars[1]
if "*" in price:
    new_price = price[:-1]
    price = new_price
    
print(price)
print(name)
print(stars[1])

driver.quit()


