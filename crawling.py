from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.ylnbujd.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

url = 'https://www.mangoplate.com/restaurants/3WFLmKTiqRLu'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url,headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

title = soup.select_one('body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > header > div.restaurant_title_wrap > span > h1').text
address = soup.select_one('body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > table > tbody > tr:nth-child(1) > td > span.Restaurant__InfoAddress--Text').text
category = soup.select_one('body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > table > tbody > tr:nth-child(3) > td > span').text
desc = soup.select_one('meta[property="og:description"]')['content']
img = soup.select_one('meta[property="og:image"]')['content']

doc = {
    "title": title,
    "address": address,
    "category": category,
    "desc": desc,
    "img": img
}

db.places.insert_one(doc)
