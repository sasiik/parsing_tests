import scrapy
from scrapy.crawler import CrawlerProcess


class LamodaSpider(scrapy.Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.i = 1

    name = 'stas'
    start_urls = ['https://www.lamoda.ru/c/4153/default-women/?is_new=1&sitelink=topmenuW&l=2']

    def parse(self, response, **kwargs):
        if response.css('div.x-product-card__card'):
            for elem in response.css('div.x-product-card__card'):
                name = elem.css('div.x-product-card-description__product-name::text').get()
                yield {
                    'name': name.strip(),
                    'brand': elem.css('div.x-product-card-description__brand-name::text').get(),
                    'price': elem.css('span::text').get(),
                    'link': elem.css('a').attrib['href'],
                }

            self.i += 1
            next_page = f'https://www.lamoda.ru/c/4153/default-women/?is_new=1&sitelink=topmenuW&l=2&page={self.i}'
            yield response.follow(next_page, callback=self.parse)


process = CrawlerProcess()
process.crawl(LamodaSpider)
process.start()
