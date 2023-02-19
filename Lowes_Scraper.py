from selenium import webdriver
import pandas as pd
import numpy as np
import requests as r
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome('/Users/samsavage/Downloads/chromedriver 2',options=options)


def get_cats():
    driver.get('https://www.lowes.com/c/Departments')
    time.sleep(5)
    search = driver.execute_script("return document.querySelectorAll(\'[class*=\"backyard link size\"]\')")
    print(search[0].get_attribute("href"))
    links = []
    for link in search:
        try:
            if "https://www.lowes.com/pl" in link.get_attribute("href"):
                links.append(link.get_attribute("href"))
        except:
            continue
    time.sleep(5)
    driver.quit()
    return links



def meta_scrape(list):
    for i in list:
        time.sleep(10)
        driver.get(i)
        time.sleep(5)
        product_links = []
        time.sleep(2)
        products = driver.find_elements_by_xpath("//a[@href]")
        for product in products:
            try:
                if "https://www.lowes.com/pl/" in product.get_attribute("href"):
                    product_links.append(product.get_attribute("href"))
                    print(product_links)
            except:
                continue
    return product_links

links = get_cats()

for link in links:
    print(link)

print("department returned, scraping sublinks")


sub_links = meta_scrape(links)

for link in sub_links:
    print(link)

# print(sub_links)

        
            
    # images = driver.execute_script("return document.querySelectorAll('[class*=\"ImageHolderStyle\"]\')")
    # for i in images:
        # print(i.get_attribute('innerHTML'))
        # f = driver.find_element_by_class_name("")
        # print(i.get_attribute('src'))


    # for image in images:
    #     if "https://mobileimages.lowes.com/productimages/" in image.get_attribute("src"):
    #         product_links.append(image.get_attribute("src"))
    #         print(product_links)

