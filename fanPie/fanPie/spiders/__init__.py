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
    name = "all_episodes"
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
                    yield request
                elif i.css('a'):
                    for j in range(len(i.css('a'))):
                        url = i.css('a')[j].attrib['href']
                        request = scrapy.Request(url, self.parse_article)
                        request.meta['episode'] = num if j == 0 else num + ' § ' + str(j)
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

        url = re.search(r'http://image\.kaolafm\.net/mz/audios/[0-9]*/[0-9a-z\-]*\.mp3', response.text)
        url = url[0] if url else '❌'
        l.add_value('url', url)

        d_1 = re.search(r'(?:(节目)?总?时长：)(?P<t>[0-9]{2}:[0-9]{2}:[0-9]{2})', shownotes['shownotes_original'])
        d_2 = re.search(r'(?:(节目)?总?时长：)约?(?P<h>[0-9]{1,2})小?时(?P<m>[0-9]{1,2})?分?', shownotes['shownotes_original'])
        if d_1:
            duration = d_1['t']
        elif d_2:
            m = '0'+ d_2['m'] if d_2['m'] and len(d_2['m']) == 1 else d_2['m']
            duration = '0' + d_2['h'] + ':' + m + ':00' if d_2['m'] else '0' + d_2['h'] + ':00:00'
        else:
            duration = '❌'
        l.add_value('duration', duration)

        pub_date = re.search(r'[a-z]="([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))";', response.text)
        pub_date = pub_date[1] if pub_date else '❌'
        l.add_value('pub_date', pub_date)

        yield l.load_item()

if __name__ == "__main__":
    pass