import json
from lxml import etree, builder
import re
import os

class FeedParser:
    def __init__(self, json):
        self.E = builder.ElementMaker(nsmap={
            'atom':'http://www.w3.org/2005/Atom',
            'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
            'content': 'http://purl.org/rss/1.0/modules/content/'
        })
        self.itunes = builder.ElementMaker(namespace='http://www.itunes.com/dtds/podcast-1.0.dtd')
        self.content = builder.ElementMaker(namespace='http://purl.org/rss/1.0/modules/content/')
        self.json = json

        self.build_feed()
        self.parse_items()

    def build_feed(self):
        self.rss = self.E.rss(
            self.E.channel(
                self._ele('title'),
                self._ele('link'),
                self._ele('pubDate'),
                self._ele('generator'),
                self._ele('language'),
                self._ele('description'),
                self._itunes_ele('author'),
                self._itunes_ele('image'),
                self.itunes.owner(
                    self._itunes_ele('name'),
                    self._itunes_ele('email')
                ),
                self._itunes_ele('type')
            )
        )


    def _ele(self, tag):
        return self.E(tag, self.json[tag])
    
    def _itunes_ele(self, tag):
        return self.itunes(tag, self.json[tag])

    def parse_items(self):
        channel = self.rss.xpath('//channel')[0]
        for i, item in enumerate(self.json['items']):
            episode = self.E.item(
                self.E.title(item['title']),
                self.E.link(item['link']),
                self.E.pubDate(item['pubDate']),
                self.E.guid(item['guid']),
                
                self.itunes.episodeType('full'),
                self.itunes.image(url=item['image']),
                self.E.enclosure(url=item['enclosure'], type="audio/mpeg"),
                self.itunes.duration(item['duration']),
                self.E.description(item['description']),
                self.content.encoded(etree.CDATA(item['description']))
            )
            channel.append(episode)

    def save(self, path):
        with open(path, 'wb+') as f:
            f.write(etree.tostring(self.rss, xml_declaration=True, encoding='UTF-8'))

class JsonParser:
    def __init__(self, path, other):
        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(__file__), path)
        with open(path)  as f:
            self._items = json.load(f)

        self._sort_items()
        self._complete_items(other)
        self._parse_shownotes()
        new_items = self._build_items()

        self._feed = {
            'title': '反派影评',
            'link': 'https://fanpaiyingping.com',
            'pubDate': self._items[-1]['pub_date'],
            'generator': 'python',
            'language': 'zh-cn',
            'description': '若批评不自由，则赞美无意义。党同伐异，猛于炮火。',
            'author': '波米和他的朋友们',
            'image': 'https://raw.githubusercontent.com/Reyshawn/FanpieFilmFeed/master/fanPie/assets/939x0w.jpg',
            'name': 'reyshawn',
            'email': 'reshawnchang@gamil.com',
            'type': 'TV & Film',
            'items': new_items
        }

    # sort items by episode number
    def _sort_items(self):
        def cmp(i):
            return int(i['episode'][:3]), len(i['episode']), int(i['episode'][-1:])

        self._items.sort(key=cmp, reverse=True)
    
    # complete items by other rss file, mainly url, duration, image
    def _complete_items(self, path):
        incomp_url = {}
        incomp_dur = {}
        for i, item in enumerate(self._items):
            if item['url'] == '❌':
                incomp_url[item['episode']] = i

            if item['duration'] == '❌':
                incomp_dur[item['episode']] = i
        
        root = etree.parse(path)
        items = root.xpath('//item')

        for i in items:
            title = i.find('title').text
            if title[:3] in incomp_url.keys():
                url = i.find('enclosure').attrib['url']
                num = incomp_url[title[:3]]
                self._items[num]['url'] = url
            
            if title[:3] in incomp_dur.keys():
                dur = i.find('itunes:duration', namespaces=i.nsmap).text
                num = incomp_dur[title[:3]]
                self._items[num]['duration'] = dur

        self._items[incomp_dur['131 sep: 1']]['duration'] = '00:55:30'
        self._items[incomp_dur['085']]['duration'] = '02:00:00'
        self._items[incomp_dur['065 sep: 1']]['duration'] = '00:58:00'
        self._items[incomp_dur['048 sep: 1']]['duration'] = '01:09:36'

    def _parse_shownotes(self):
        def _format_scoring(s, hosts):
            patterns = [
                r'(《[^》]*?》([\(|（][^\)]*?[\)|）])?)(综合)?(平均)?总?分数?[：|:]约?(?P<score>[0-9\.]*)分?',
                r'[(综合)|(平均)|总]分数?[：|:]约?(?P<score>[0-9\.]*)分?'
            ]
            if s == '❌':
                return s
            end_s = re.search(r'[(|（]?音频后期制作', s)
            if end_s:
                end = s[end_s.span()[0]:]
                s = s[:end_s.span()[0]]
            else:
                end = ''

            if '波米' not in hosts:
                hosts.append('波米')

            for pattern in patterns:
                ave = re.search(pattern, s)
                if ave and ave['score']:
                    s = re.sub(pattern, '', s)
                    break
                
            s = s.replace('&amp;', '&')
            s = s.replace('（以下广告，由微信平台自动插入，我们编辑文章时看不到内容，每位读者看到的也并不相同）', '')

            if not ave:
                print('exception:', s)

            pos = []
            for host in hosts:
                if s.find(host) > -1:
                    pos.append(s.find(host))

            pos.sort()
            try:
                st = pos[0]
            except:
                # print(item['episode'])
                return s
            res = []
            for i, p in enumerate(pos[1:]):
                res.append(s[st:p])
                st = p
            res.append(s[st:])

            scoring = '\n'.join(res) + '\n' + end + '\n\n'
            return scoring + '平均分: ' + ave['score'] if ave else scoring

        def _format_outline(s):
            s = s.split('；')
            s = '; \n'.join(s)
            s = s.replace('&lt;', '<')
            s = s.replace('&gt;', '>')
            s = s.replace('&amp;', '&')
            s = re.sub(r'(下载完整节目)?(收听节目)?请点击(文末)?\"阅读原文\"按钮。', '', s)
            s = s.replace('（以下广告，由微信平台自动插入，我们编辑文章时看不到内容，每位读者看到的也并不相同）', '')

            return s

        def _format_list(l):
            res = '<h2>本期片目</h2>\n<ul>\n'
            for i, item in enumerate(l):
                res += '<li>『' + item['name'] + '』( ' + item['time'] + ' )</li>\n'
            return res + '</ul>\n'

        for i, item in enumerate(self._items):
            hosts = item['hosts']
            scoring = _format_scoring(item['shownotes']['film_scoring'], hosts)
            outline = _format_outline(item['shownotes']['film_outline'])
            f_list = _format_list(item['shownotes']['film_list'])
            summary = scoring + '\n\n' + outline + '\n\n' + f_list
            item['summary'] = summary

    def _build_items(self):
        res = []
        for i, item in enumerate(self._items):
            tmp = {}
            tmp['title'] = 'Episode ' + item['episode'] + ' | ' + item['title']
            tmp['link'] = item['url']
            tmp['guid'] = 'fanpie_' + re.search(r'\/([\_\-a-zA-Z0-9]*)\.mp3', item['url'])[1]
            tmp['pubDate'] = item['pub_date']
            tmp['author'] = ', '.join(item['hosts'])
            tmp['enclosure'] = item['url']
            tmp['duration'] = item['duration']
            tmp['image'] = 'https://raw.githubusercontent.com/Reyshawn/FanpieFilmFeed/master/fanPie/assets/939x0w.jpg'
            tmp['description']= item['summary']
            res.append(tmp)
        return res

    def save(self, path):
        with open(path, 'w+') as f:
            json.dump(self._feed, f, ensure_ascii=False)

    def feed(self):
        return self._feed


if __name__ == "__main__":
    a = JsonParser('output.json', '/Users/reyshawn/Desktop/fanPie_ximalaya.rss')
    feed = a.feed()
    xml = FeedParser(feed)
    xml.save('fanPieFilm.rss')