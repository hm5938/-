from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests

client = MongoClient('mongodb+srv://test:sparta@cluster0.ylnbujd.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

driver = webdriver.Chrome('./chromedriver')

url = "http://matstar.sbs.co.kr/location.html"

driver.get(url)
time.sleep(5)

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')

places = soup.select("ul.restaurant_list > div > div > li > div > a")
print(len(places))

for place in places:
    title = place.select_one("strong.box_module_title").text
    address = place.select_one("div.box_module_cont > div > div > div.mil_inner_spot > span.il_text").text
    category = place.select_one("div.box_module_cont > div > div > div.mil_inner_kind > span.il_text").text
    comment = place.select_one("span.box_module_stitle").text.strip()
    img = place.select_one("img.box_module_image")["src"]
    doc = {
        "title": title,
        "address": address,
        "category": category,
        "comment": comment,
        "img": img
    }
    db.places.insert_one(doc)

