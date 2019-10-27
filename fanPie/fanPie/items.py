# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class FanpieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    episode = scrapy.Field(output_processor=TakeFirst())
    film = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field()
    hosts = scrapy.Field()
    shownotes = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    duration = scrapy.Field(output_processor=TakeFirst())
    pub_date = scrapy.Field(output_processor=TakeFirst())


if __name__ == "__main__":
    film = FanpieItem(episode=1, title="今年的金熊金狮金棕榈，这部是最好的。", hosts=['波米', '雷普利'])
    print(film['title'])
