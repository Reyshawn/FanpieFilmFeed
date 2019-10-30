import scrapy
from scrapy.loader import ItemLoader

if __name__ != "__main__":
    from ..items import FanpieItem
from . import parse_response
import re
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class updateSpider(scrapy.Spider):
    name = 'episode'
    # start_urls = ['https://mp.weixin.qq.com/s/uF0GiJbi4A5WBxq5iUPuqQ']

    def __init__(self, url='', episode='', film='', hosts=[]):
        self.start_urls = [url]
        self._episode = episode
        self._film = film
        self._hosts = hosts.split(',')

    def parse(self, response):
        
        l = ItemLoader(item=FanpieItem(), response=response)
        l.add_css('title', '.rich_media_title::text')

        l.add_value('episode', self._episode)
        l.add_value('film', self._film)
        l.add_value('hosts', self._hosts)
        l.add_value('link', self.start_urls[0])

        parse_response(response, l)

        yield l.load_item()


if __name__ == "__main__":
    import sys
    import os
    base_path = os.path.abspath('./') # add parent directory
    sys.path.append(base_path)

    from fanPie.fanPie.items import FanpieItem
    process = CrawlerProcess(get_project_settings())
    process.crawl(updateSpider)
    process.start()
