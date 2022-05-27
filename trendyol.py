import scrapy
from scrapy.crawler import CrawlerProcess


class OzonSpider(scrapy.Spider):
    name = 'stas'
    start_urls = ['https://www.trendyol.com/erkek-spor-ayakkabi-x-g2-c109']

    def __init__(self):
        super(OzonSpider, self).__init__()
        self.i = 1

    def parse(self, response, **kwargs):
        global i
        for a in response.css('div.prdct-desc-cntnr-wrppr'):
            yield {
                'name': a.css('span::attr(title)').getall()[0] + ' ' + a.css('span::attr(title)').getall()[1],
                'price': a.css('div.prc-box-dscntd::text').get()

            }
        self.i += 1
        next_page = f'https://www.trendyol.com/erkek-spor-ayakkabi-x-g2-c109?pi={self.i}'
        yield response.follow(next_page, callback=self.parse)


process = CrawlerProcess()
process.crawl(OzonSpider)
process.start()
