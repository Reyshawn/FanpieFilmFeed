# Update the new episode

import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def is_latest(**kwargs):
    pass

if __name__ == "__main__":

    settings_file_path = 'fanPie.settings'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

    process = CrawlerProcess(get_project_settings())

    with open('output.json', 'r') as f:
        output = json.load(f)
    
    # episode = int(output[0]['episode']) + 1
    # episode = f"{episode:03d}" # '001' '012' '174' format

    if os.path.isfile('latest.json'):
        os.remove('latest.json')

    kwargs = {
        'url':'https://mp.weixin.qq.com/s/RrWqF4bt-Gb3swPP_xyJJQ',
        'episode': '180 § 1', # episode
        'film': '爱尔兰人',
        'hosts': '荡科长,雷普利,波米'
    }

    process.crawl('episode', **kwargs)
    process.start()

    with open('latest.json', 'r') as f:
        latest = json.load(f)

    output = latest + output

    with open('output.json', 'w+') as f:
        json.dump(output, f, ensure_ascii=False)

    # clear the lastest.json content
    os.remove('latest.json')