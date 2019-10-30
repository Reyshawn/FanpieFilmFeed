# Update the new episode


import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from fanPie.spiders import episode

if __name__ == "__main__":

    settings_file_path = 'fanPie.settings'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

    process = CrawlerProcess(get_project_settings())

    process.crawl('episode', url='https://mp.weixin.qq.com/s/uF0GiJbi4A5WBxq5iUPuqQ', episode='011', film='少年的你', hosts='熊阿姨,萝贝贝,波米')
    process.start()