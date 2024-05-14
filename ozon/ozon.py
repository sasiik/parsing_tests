import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import os
import re


class OzonScraper:
    def __init__(self):
        self.base_url = 'https://www.ozon.ru/category/igrushki-i-igry-7108/'
        self.results = []
        cookie = os.getenv("COOKIES")
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'fi-FI,fi;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
            'Cookie': cookie,
            'Priority': 'u=1, i',
            'Purpose': 'sw-prefetch',
            'Referer': 'https://www.ozon.ru/st/service-worker/1.0.43.js',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

    def fetch_page(self, url):
        import chardet
        response = requests.get(url, headers=self.headers)
        return response.text if response.status_code == 200 else None

    def parse(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.select('a.tile-hover-target.vi8.iv9')
        prices = soup.select('div.c305-a0')

        for item, price in zip(items, prices):
            name_item = item.select_one('span')
            if isinstance(name_item, Tag):
                name = re.sub(r'\/.*', '', name_item.text).strip()
            link = item['href']
            price_text = price.text.replace('\u2009', '').split('₽')
            if len(price_text) < 3:
                for _ in range(0, 3-len(price_text)):
                    price_text.append('No info')
            data = {
                'name': name,
                'link': link,
                'new_price': price_text[0],
                'old_price': price_text[1],
                'bonus': price_text[2]
            }
            print(data)
            self.results.append(data)

    def scrape(self):
        i = 1
        current_url = self.base_url

        while i < 100:
            html_content = self.fetch_page(current_url)
            if not html_content:
                break

            self.parse(html_content)

            # Update this to detect the next page URL correctly based on the website's navigation structure
            soup = BeautifulSoup(html_content, 'html.parser')
            next_page_href = soup.select_one(
                'a.en4.b213-a0.b213-b6.b213-b1')
            if next_page_href:
                next_page_href = next_page_href.get('href')
            next_page = self.base_url + f'?page={i}'
            print("Next page: " + next_page)

            current_url = next_page
            i += 1

        # Convert to DataFrame and save as Excel
        df = pd.DataFrame(self.results)
        df.to_excel('ozon/output/output.xlsx', engine='openpyxl', index=False)


# Usage
scraper = OzonScraper()
scraper.scrape()
