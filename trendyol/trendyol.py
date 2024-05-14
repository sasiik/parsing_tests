import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse


class TrendyolSpider(scrapy.Spider):
    name = 'trendyol'
    start_urls = ['https://www.trendyol.com/erkek-spor-ayakkabi-x-g2-c109']

    def __init__(self):
        super(TrendyolSpider, self).__init__()
        self.i = 1
        self.results = []

    def parse(self, response: HtmlResponse, **kwargs):
        if self.i > 100:
            df = pd.DataFrame(self.results)
            df.to_excel('trendyol/output/output.xlsx',
                        engine='openpyxl', index=False)
            print("Data saved to output.xlsx.")
            return 0

        for elem in response.css('div.product-down'):
            output = {
                "name": ' '.join(elem.css('div.prdct-desc-cntnr *::text').getall()),
                "social_proof": ' '.join(elem.css('div.social-proof *::text').getall()),
                "ratings": ' '.join(elem.css('div.ratings *::text').getall()),
                "price": ' '.join(elem.css('div.price-promotion-container *::text').getall()),
                "offer": ' '.join(elem.css('div.badges-wrapper *::text').getall())
            }
            self.results.append(output)
            print(output)
        self.i += 1
        next_page = f'https://www.trendyol.com/erkek-spor-ayakkabi-x-g2-c109?pi={
            self.i}'
        yield response.follow(next_page, callback=self.parse)


process = CrawlerProcess()
process.crawl(TrendyolSpider)
process.start()
