# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from scrapy.loader import ItemLoader
from ..items import FanpieItem
import re

pattern = re.compile('[0-9]{3}')
index = 0

class filmSpider(scrapy.Spider):
    name = "film"
    start_urls = [
        'https://mp.weixin.qq.com/s/V6LfeY6Mki8VDyFYyfud2Q'
    ]

    def parse(self, response):
        urls = response.css('div.rich_media_content p')
        for i in urls:
            num = i.css('span::text').get()
            if num and pattern.match(num):
                print('num:', num)
                if i.css('a'):
                    url = i.css('a').attrib['href']
                    yield scrapy.Request(url, self.parse_article)
                

    def parse_article(self, response):
        l = ItemLoader(item=FanpieItem(), response=response)
        l.add_css('title', '.rich_media_title::text')
        yield l.load_item()
        # yield {'title': response.css('.rich_media_title::text').get()}

if __name__ == "__main__":
    pass