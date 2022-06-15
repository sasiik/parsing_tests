import requests
from bs4 import BeautifulSoup
import time
import lxml
import json
from db import add_message

req = requests.get('https://en.wikipedia.org/wiki/List_of_multiplanetary_systems')

with open('page.html', 'w', encoding='utf-8') as page:
    page.write(req.text)

with open('page.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

tablerows = soup.find('table', class_='toccolours sortable wikitable').find('tbody').find_all('tr')

for row in tablerows[1:]:
    res = []
    for elem in row.find_all('td'):
        res.append(elem.text.replace('\xa0', '').replace('\n', ''))
    name = res[0]
    ra = res[2]
    dec = res[3]
    dist = res[5]
    count = res[10]
    add_message(star=name, ra=ra, dec=dec, raddist=dist, planetcount=count)
