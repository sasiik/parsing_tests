import bs4
import json
import requests
from bs4 import BeautifulSoup
from pandas import json_normalize


def fetch_table_data(url):
    # Get the page content
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')

    # Find the table by class
    table = soup.find('table', class_='toccolours sortable wikitable')
    if table is None or not isinstance(table, bs4.element.Tag):
        print("No table found with the specified class, or it's not a Tag.")
        return []

    # Find tbody within the table
    tbody = table.find('tbody')
    if tbody is None or not isinstance(tbody, bs4.element.Tag):
        print("No tbody found in the table, or it's not a Tag.")
        return []

    # Extract rows from the tbody
    rows = tbody.find_all('tr')[1:]  # Skip the header row
    data_list = []

    # Process each row
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 10:  # Check if there are enough columns
            data = {
                'name': cells[0].get_text(strip=True).replace('\xa0', '').replace('\n', ''),
                'ra': cells[2].get_text(strip=True).replace('\xa0', '').replace('\n', ''),
                'dec': cells[3].get_text(strip=True).replace('\xa0', '').replace('\n', ''),
                'dist': cells[5].get_text(strip=True).replace('\xa0', '').replace('\n', ''),
                'count': cells[10].get_text(strip=True).replace('\xa0', '').replace('\n', '')
            }
            data_list.append(data)
    with open("stars/output/res.json", "w", encoding='utf-8') as res:
        json.dump(data_list, res, ensure_ascii=False, indent=4)
    return data_list


url = 'https://en.wikipedia.org/wiki/List_of_multiplanetary_systems'
multiplanetary_systems = fetch_table_data(url)

df = json_normalize(multiplanetary_systems, sep='_')
df.to_excel('stars/output/output.xlsx', engine='openpyxl', index=True)
