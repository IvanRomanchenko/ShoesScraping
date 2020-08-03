from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ShoesScraping.items import Shoes


class SelfySpider(CrawlSpider):
    name = 'selfy'
    allowed_domains = ['selfy.com.ua']
    start_urls = ['https://selfy.com.ua/vsya-obuv-selfy/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//h4/a')), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('/vsya-obuv-selfy/'), restrict_xpaths=("//ul[@class='pagination']/li/a"), restrict_text='>'), follow=True),
    )

    def parse_item(self, response):
        item = Shoes()
        item['name'] = response.xpath("//div[@class='col-sm-4']/h1/text()").get()
        item['price'] = response.xpath("//li[@class='price']/h2/text()").get()
        item['season'] = response.xpath("//tbody/tr[1]/td[2]/text()").get()
        item['sex'] = response.xpath("//tbody/tr[2]/td[2]/text()").get()
        item['size'] = response.xpath("//tbody/tr[3]/td[2]/text()").get()
        item['type'] = response.xpath("//tbody/tr[4]/td[2]/text()").get()
        return item
