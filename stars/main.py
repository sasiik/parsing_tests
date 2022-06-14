import requests
from bs4 import BeautifulSoup
import lxml
import json
from db import add_message

# req = requests.get('https://www.princeton.edu/~willman/planetary_systems/')

# with open('page.html', 'w', encoding='utf-8') as page:
# page.write(req.text)

with open('page.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

rows = soup.find_all('tr')

for item in rows[3:]:
    res = []
    for elem in item:
        if elem != '\n':
            res.append(elem.text.replace('\xa0', ''))

    star = res[0]
    planet_count = res[5]
    if res[1]:
        ra = res[1]
    else:
        ra = 'No information'

    if res[2]:
        dec = res[2]
    else:
        dec = 'No information'

    if res[3]:
        raddist = res[3]
    else:
        raddist = 'No information'
    add_message(star=star, planetcount=planet_count, ra=ra, dec=dec, raddist=raddist)
