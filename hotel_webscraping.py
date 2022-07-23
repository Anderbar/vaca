#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 17:35:27 2022

@author: ananyayadav
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def close_popup(driver):
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

def wait_object(driver, xpath):
    return WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))


    
def get_more_info(driver):
    #open new window with more info
    wait_object(driver, '//div[@class = "FLpo-reviews"]')
    button = driver.find_element_by_xpath('//div[@class = "FLpo-reviews"]')
    button.click()
    
    time.sleep(1)
    
    #switch driver focus to new window
    curr = driver.current_window_handle
    other = driver.window_handles
    for x in other:
        if x != curr:
            driver.switch_to.window(x)
            break
    
    #Scroll up to the top of the page
    htmlelement= driver.find_element_by_tag_name('html')
    time.sleep(1)
    htmlelement.send_keys(Keys.HOME)
    time.sleep(0.5)
    
    #Retrieve info
    info_url = driver.current_url
    info_dict = {}
    info_dict.update({"url": info_url.replace("#reviews", "")})
    
    wait_object(driver, '//div[@class = "c3xth-price-info-wrapper"]')
    
    name = driver.find_element_by_xpath('//div[@class = "c3xth-title"]').text
    address = driver.find_element_by_xpath('//div[@class = "c3xth-address"]').text
    below_info = driver.find_element_by_xpath('//div[@class = "c3xth-info-below-address"]').text
    below_info = below_info.split("\n")
    price = driver.find_element_by_xpath('//div[@class = "c3xth-price-info-wrapper"]').text
    price = price.split("\n")
    info_dict.update({"name": name})
    info_dict.update({"address": address})
    info_dict.update({"cust_rating": below_info[0]})
    info_dict.update({"rating_level": below_info[1]})
    info_dict.update({"num_reviews": below_info[2]})
    info_dict.update({"price": price[0]})
    info_dict.update({"website": price[1]})

    driver.quit()
    return info_dict   


def get_started(stars, dest, dep_date, arr_date):
    #Launch Kayak website
    driver = webdriver.Chrome()
    driver.get("https://www.kayak.com/stays")
    time.sleep(1)

    close_popup(driver)

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
    #Create new url with city code and launch
    url = driver.current_url
    new_url = update_url(url, dep_date, arr_date, stars)
    time.sleep(3)
    driver.get(new_url)
    #Allow page to load
    time.sleep(15)
    
    return(get_more_info(driver))

stars = 4
dest = "New York, New York, USA"
dep_date = "2022-08-06"
arr_date = "2022-08-08"

info = get_started(stars, dest, dep_date, arr_date)
print(info)



