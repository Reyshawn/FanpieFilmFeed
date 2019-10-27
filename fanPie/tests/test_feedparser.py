import json
from lxml import etree, builder
import re

class FeedParser:
    def __init__(self, json):
        self.E = builder.ElementMaker(nsmap={
            'atom':'http://www.w3.org/2005/Atom',
            'itunes': "http://www.itunes.com/dtds/podcast-1.0.dtd"   
        })
        self.itunes = builder.ElementMaker(namespace='http://www.itunes.com/dtds/podcast-1.0.dtd')
        self.json = json

        self.build_rss()
        self.parse_items()

    def build_feed(self):
        self.rss = self.E(
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

    def _ele(self, tag):
        return self.E(tag, self.json[tag])
    
    def _itunes_ele(self, tag):
        return self.itunes(tag, self.json[tag])

    def parse_items(self):
        pass


class JsonParser:
    def __init__(self, path, other):
        with open(path)  as f:
            self._items = json.load(f)

        self._sort_items()
        self._complete_items(other)

        self._header = {
            'title': '反派影评',
            'link': 'https://fanpaiyingping.com',
            'pubDate': self._items[-1]['pub_date'],
            'generator': 'python',
            'language': 'zh-cn',
            'description': '若批评不自由，则赞美无意义。党同伐异，猛于炮火。',
            'author': '波米和他的朋友们',
            'image': 'https://is5-ssl.mzstatic.com/image/thumb/Podcasts113/v4/ab/77/d9/ab77d99d-50aa-5d43-9a15-0327d4840f6a/mza_1413129501713462604.jpg/939x0w.jpg',
            'name': 'reyshawn',
            'email': 'reshawnchang@gamil.com'
        }



        self._feed = None

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
        pass

    def save_file(self, path):
        with open(path, 'w+') as f:
            json.dump(self._feed, f, ensure_ascii=False)




def test_write_xml(output):
    with open('/Users/reyshawn/Desktop/rss.xml', 'wb+') as f:
        f.write(etree.tostring(output, xml_declaration=True, encoding='UTF-8'))


def test_build_xml():
    E = builder.ElementMaker(nsmap={
        'atom':'http://www.w3.org/2005/Atom',
        'itunes': "http://www.itunes.com/dtds/podcast-1.0.dtd"   
    })

    itunes = builder.ElementMaker(namespace='http://www.itunes.com/dtds/podcast-1.0.dtd')


    def get_item(title, link):
        return E.item(
            E.title(title),
            E.link(link)
        )

    rss = E.rss(
        E.channel(
            E.title('反派影评'),
            E.link('https://www.ximalaya.com/album/4127591/'),
            E.pubDate('Mon, 27 May 2019 17:10:26 GMT'),
            E.language('zh-cn'),
            E.descripttion('若批评不自由，则赞美无意义。党同伐异，猛于炮火。'),
            itunes.author('波米和他的朋友们'),
            itunes.image(href="https://fdfs.xmcdn.com/group48/M01/8F/6E/wKgKlVuJRsmCGvIUAACqlRzgjdM964.jpg"),
            get_item(
                '157《复仇者联盟4：终局之战》：你和银幕对暗号',
                'https://www.ximalaya.com/47283140/sound/180370476/'
            ),
            get_item(
                '128《影》（2小时版，5.7分）：标新立异还是徒有其表？',
                'https://www.ximalaya.com/47283140/sound/127187181/'
            )
        )
    )

    channel = rss.xpath('//channel')[0]
    channel.append(get_item(
        '126《曼蒂》（6分）：跟凯奇左手右手一个慢动作！',
        'https://www.ximalaya.com/47283140/sound/124142172/'
    ))
    

    rss.set('version', '2.0')
    rss.set('encoding', 'UTF-8')
    test_write_xml(rss)


def test_sort_items(data):
    def cmp(i):
        return int(i['episode'][:3]), len(i['episode']), int(i['episode'][-1:])

    data.sort(key=cmp, reverse=True)


# complete url and duration field
def test_complete_items(data, path):
    incomp = {}
    for i, item in enumerate(data):
        if item['url'] == '❌':
            incomp[item['episode']] = i
            print(item['episode'])

    root = etree.parse(path)
    items = root.xpath('//item')

    for i in items:
        title = i.find('title').text
        if title[:3] in incomp.keys():
            url = i.find('enclosure').attrib['url']
            num = incomp[title[:3]]
            data[num]['url'] = url

    with open('/Users/reyshawn/Desktop/allurl.json', 'w+') as f:
        json.dump(data, f, ensure_ascii=False)

def test_complete_dur(data, path):
    incomp = {}
    for i, item in enumerate(data):
        if item['duration'] == '❌':
            incomp[item['episode']] = i
            print(item['episode'])
    
    root = etree.parse(path)
    items = root.xpath('//item')

    for i in items:
        title = i.find('title').text
        if title[:3] in incomp.keys():
            dur = i.find('itunes:duration', namespaces=i.nsmap).text
            num = incomp[title[:3]]
            data[num]['duration'] = dur

    data[incomp['131 sep: 1']]['duration'] = '00:55:30'
    data[incomp['085']]['duration'] = '2:00:00'
    data[incomp['065 sep: 1']]['duration'] = '00:58:00'
    data[incomp['048 sep: 1']]['duration'] = '01:09:36'



    print('------------------------------')
    for i, item in enumerate(data):
        if item['duration'] == '❌':
            incomp[item['episode']] = i
            print(item['episode'])
    


def test_get_duration(data, path):
    sect = data[:]
    for i, item in enumerate(sect):
        t = re.search(r'(?:(节目)?总?时长：)(?P<t>[0-9]{2}:[0-9]{2}:[0-9]{2})', item['shownotes']['shownotes_original'])
        l = re.search(r'(?:(节目)?总?时长：)约?(?P<h>[0-9]{1,2})小?时(?P<m>[0-9]{1,2})?分?', item['shownotes']['shownotes_original'])
        if t:
            print(':  ', t['t'])
            print('episode: ', item['episode'])
        elif l:
            m = '0'+ l['m'] if l['m'] and len(l['m']) == 1 else l['m']
            x = l['h'] + ':' + m + ':00' if l['m'] else l['h'] + ':00:00'
            print(':  ', x)
            print('episode: ', item['episode'])


def test_parse_shownotes(data):
    def _format_scoring(s, hosts, item):
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
            print(item['episode'])
            return s
        res = []
        for i, p in enumerate(pos[1:]):
            res.append(s[st:p])
            st = p
        res.append(s[st:])

        if not ave:
            print('score', item['episode'])

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
        res = '本期片目\n\n'
        for i, item in enumerate(l):
            res += '『' + item['name'] + '』( ' + item['time'] + ' )\n'
        return res
    
    res = []
    for i, item in enumerate(data):
        hosts = item['hosts']
        scoring = _format_scoring(item['shownotes']['film_scoring'], hosts, item)
        outline = _format_outline(item['shownotes']['film_outline'])
        f_list = _format_list(item['shownotes']['film_list'])
        summary = scoring + '\n\n' + outline + '\n\n' + f_list
        tmp = {
            'episode': item['episode'],
            'title': item['title'],
            'summary': summary
        }
        res.append(tmp)

    with open('/Users/reyshawn/Desktop/summary.json', 'w+') as f:
        json.dump(res, f, ensure_ascii=False)

    

if __name__ == "__main__":
    with open('/Users/reyshawn/Desktop/summary.json', 'r') as f:
       data = json.load(f)
    
    # test_sort_items(data)
    # test_complete_dur(data, '/Users/reyshawn/Desktop/fanPie.rss')
    # JsonParser('/Users/reyshawn/Desktop/output.json', '/Users/reyshawn/Desktop/fanPie.rss')
    # test_parse_shownotes(data)

    sect = data[20:100]
    for i, item in enumerate(sect):
        print(item['summary'])