import scrapy
from scrapy.crawler import CrawlerProcess
import re


class OzonSpider(scrapy.Spider):
    name = 'stas'
    start_urls = ['https://www.ozon.ru/category/igrushki-i-igry-7108/']

    def parse(self, response, **kwargs):
        list = response.css('a.tile-hover-target.i3m')
        prices = response.css('span.ui-s5.ui-s8.ui-t0::text').getall()
        for i in range(len(list)):
            try:
                yield {
                    'name': re.sub('\/.*', '', list[i].css('span::text').get()).strip(),
                    'link': list[i].attrib['href'],
                    'price': re.sub('\u2009', '', prices[i])
                }
            except:
                yield {
                    'name': re.sub('\/.*', '', list[i].css('span::text').get()).strip(),
                    'link': list[i].attrib['href'],
                    'price': 'Нет в наличии'
                }
        try:
            next_page = response.css('a.ui-b3')[-1].attrib['href']
            yield response.follow(next_page, callback=self.parse)
        except:
            pass


process = CrawlerProcess()
process.crawl(OzonSpider)
process.start()
