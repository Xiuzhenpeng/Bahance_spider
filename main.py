import requests
from bs4 import BeautifulSoup


import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


chrome_driver_path = r'D:\Download\Chrome Download\chromedriver-win64\chromedriver-win64\chromedriver.exe'
initial_url = 'https://www.behance.net/galleries/product-design/automotive-design'

chrome_service = Service(chrome_driver_path)

wd = webdriver.Chrome(service=chrome_service)
wd.implicitly_wait(30)

wd.get(initial_url)

elements = wd.find_elements(By.CSS_SELECTOR, '.ProjectCoverNeue-featureFlagsContainer-yme')

# for element in elements:
#     print(element)
print(len(elements))
wd.quit()
