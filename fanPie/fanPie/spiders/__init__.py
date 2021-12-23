# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import re

def parse_response(response, l):
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


def validate_item(l):
    '''validate that there is no empty field of the item
    Args:
        l (ItemLoader): https://docs.scrapy.org/en/latest/topics/loaders.html
    Returns:
        bool: the return value, if failed, it will raise a ValueError.
    '''
    check_list = [
        'episode',
        'film',
        'title',
        'hosts',
        'shownotes',
        'url',
        'duration',
        'pub_date',
        'link'
    ]

    for c in check_list:
        t = l.get_collected_values(c)
        if len(t) == 0 or t[0] == '':
            raise ValueError(f'Could not find {c} in ItemLoader')
    return True