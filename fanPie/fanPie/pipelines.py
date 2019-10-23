# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class FanpiePipeline(object):

    def open_spider(self, spider):
        print('start the pipeline!!!!!!')
    
    def close_spider(self, spider):
        print('close the pipeline⚠️')

    def process_item(self, item, spider):

        item['title'] = item['title'][0].strip()
        print('item:       ', item)
        return item
