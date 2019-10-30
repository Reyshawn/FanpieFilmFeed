import scrapy
from scrapy.loader import ItemLoader
from ..items import FanpieItem
from . import parse_response
import re

class filmSpider(scrapy.Spider):
    name = "episodes"
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json'
    }

    start_urls = [
        'https://mp.weixin.qq.com/s/V6LfeY6Mki8VDyFYyfud2Q'
    ]

    def parse(self, response):
        urls = response.css('div.rich_media_content p')
        for i in urls[1:]:
            title = re.sub(r'<[^>]*>', '', i.get()).strip()
            if title:
                num = title[:3]
                hosts_list = re.findall(r'（[^：]*?(?:嘉宾：?)([^）]*)）', title)
                film = re.sub(r'（[^：]*?(?:嘉宾：?)([^）]*)）', '', title[3:]).strip()

                hosts = []
                for host in hosts_list:
                    if '、' in host:
                        hosts += host.split('、')
                    else:
                        hosts.append(host)

                print('title:', title)
                if num == '111':
                    url = 'https://mp.weixin.qq.com/s/_phqvDLLqsI_4uJ7gSDoQw'
                    request = scrapy.Request(url, self.parse_article)
                    request.meta['episode'] = num
                    request.meta['film'] = film
                    request.meta['hosts'] = hosts
                    request.meta['link'] = url
                    yield request
                elif i.css('a'):
                    for j in range(len(i.css('a'))):
                        url = i.css('a')[j].attrib['href']
                        request = scrapy.Request(url, self.parse_article)
                        request.meta['episode'] = num if j == 0 else num + ' § ' + str(j)
                        request.meta['film'] = film
                        request.meta['hosts'] = hosts
                        request.meta['link'] = url
                        yield request
                

    def parse_article(self, response):
        l = ItemLoader(item=FanpieItem(), response=response)
        l.add_css('title', '.rich_media_title::text')
        l.add_value('episode', response.meta['episode'])
        l.add_value('film', response.meta['film'])
        l.add_value('hosts', response.meta['hosts'])
        l.add_value('link', response.meta['link'])

        parse_response(response, l)

        yield l.load_item()

if __name__ == "__main__":
    pass