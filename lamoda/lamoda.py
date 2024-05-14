import json
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

"""Works much worse that the JS version as it is able to extract much less data"""


class LamodaScraper:
    def __init__(self):
        self.base_url = 'https://www.lamoda.ru/c/4153/default-women/'
        self.params = {
            'is_new': 1,
            'sitelink': 'topmenuW',
            'l': 2
        }
        self.results = []
        self.pages_to_scrape = 1  # Set the number of pages to scrape

    def fetch(self, page):
        self.params['page'] = page
        response = requests.get(self.base_url, params=self.params)
        return response.text if response.status_code == 200 else None

    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        script_tags = soup.find_all('script')
        pattern = re.compile(r'header:\s*(\{.*?\})\s*,\s*settings:', re.DOTALL)
        for script in script_tags:
            if '__NUXT__' in script.text:
                match = pattern.search(script.text)
                if match:
                    nuxt_json = match.group(1).strip()
                    print(nuxt_json[:100])
                    print(nuxt_json[-100:])
                    return nuxt_json
            else:
                print("No JSON object found in the script.")

    def search_in_json(self, json_string):
        json_data = json.loads(json_string)
        print(json_data)

    def run(self):
        for i in range(1, self.pages_to_scrape + 1):
            html = self.fetch(i)
            if html:
                json_content = self.parse(html)
                self.search_in_json(json_content)

        # Save results to Excel
        df = pd.DataFrame(self.results)
        df.to_excel('lamoda/output/output.xlsx',
                    engine='openpyxl', index=False)
        print("Data saved to output.xlsx.")


# Usage
scraper = LamodaScraper()
scraper.run()
