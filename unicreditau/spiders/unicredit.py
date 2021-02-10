import scrapy
from scrapy.loader import ItemLoader
from ..items import UnicreditauItem
from scrapy.loader.processors import TakeFirst
import re
pattern = r'(\r)?(\n)?(\t)?(\xa0)?'

class UnicreditSpider(scrapy.Spider):
    name = 'unicredit'

    start_urls = ['https://www.bankaustria.at/ueber-uns-presse-presseinformationen.jsp']

    def parse(self, response):
        links = response.xpath('//div[@class="content-txt"]//li[@class="margin-bottom-medium"]/a/@href').getall()
        yield from response.follow_all(links,self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(UnicreditauItem())
        item.default_output_processor = TakeFirst()

        date = response.xpath('//div[@class="content-txt"]/span/text()').get()
        title = ''.join(response.xpath('//div[@class="content-txt"]/h2/text()').getall()).strip()
        content = (response.xpath('//div[@class="container"]//div[@class="content-txt"]/*[not (self::h2) and not (self::span)]//text()').getall())[:-6]
        content = re.sub(pattern, "",''.join(content).strip())


        item.add_value('date', date)
        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        return item.load_item()