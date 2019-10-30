import scrapy
from scrapy.loader import ItemLoader

from ..items import FanpieItem
from . import parse_response, validate_item
import re


class updateSpider(scrapy.Spider):
    name = 'episode'
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'latest.json'
    }
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

        validate_item(l)

        yield l.load_item()


if __name__ == "__main__":
    pass
