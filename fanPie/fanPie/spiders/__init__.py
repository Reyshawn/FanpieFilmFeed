# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from scrapy.loader import ItemLoader
from ..items import FanpieItem
import re

index = 0

class filmSpider(scrapy.Spider):
    name = "film"
    start_urls = [
        'https://mp.weixin.qq.com/s/V6LfeY6Mki8VDyFYyfud2Q'
    ]

    def parse(self, response):
        urls = response.css('div.rich_media_content p')
        for i in urls[1:]:
            title = re.sub(r'<[^>]*>', '', i.get()).strip()
            if title:
                num = title[:3]
                sep = title.find('（')
                film = title[4:sep].strip()

                hosts_strip = re.search(r'(?:嘉宾：)([^）]*)', title[sep:])
                hosts = hosts_strip[1].split('、') if hosts_strip else ['波米']

                print('title:', title)
                if i.css('a'):
                    url = i.css('a').attrib['href']
                    request = scrapy.Request(url, self.parse_article)
                    request.meta['episode'] = num
                    request.meta['film'] = film
                    request.meta['hosts'] = hosts
                    yield request
                

    def parse_article(self, response):
        l = ItemLoader(item=FanpieItem(), response=response)
        l.add_css('title', '.rich_media_title::text')
        l.add_value('episode', response.meta['episode'])
        l.add_value('film', response.meta['film'])
        l.add_value('hosts', response.meta['hosts'])
        
        st = response.text.find(r'<div class="rich_media_content')
        main = response.text[st:]
        ed = main.find(r'</div>')
        main = main[:ed]
        shownotes = re.sub(r'<[^>]*>', '', main).strip() if ed!=-1 and response.status==200 else ''

        shownotes = {'shownotes_original': shownotes}

        l.add_value('shownotes', shownotes)
        yield l.load_item()

if __name__ == "__main__":
    pass