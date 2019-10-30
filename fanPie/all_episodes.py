import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def cmp(i):
    return int(i['episode'][:3]), len(i['episode']), int(i['episode'][-1:])

if __name__ == "__main__":

    if os.path.isfile('output.json'):
        os.remove('output.json')
    
    settings_file_path = 'fanPie.settings'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

    process = CrawlerProcess(get_project_settings())
    process.crawl('episodes')

    process.start()

    with open('output.json', 'r') as f:
        data = json.load(f)
    
    data.sort(key=cmp, reverse=True)

    with open('output.json', 'w+') as f:
        json.dump(data, f, ensure_ascii=False)
    
    