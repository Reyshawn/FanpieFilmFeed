import json
import re

# re = r'《([^》]*)》[ ]*?[(|（]?[^()（）]*?([0-9]{4})[)|）]?'


class NotesParser:
    
    def __init__(self, episode):
        self._shownotes = episode['shownotes'][0]
        list_pos_1 = ['本期节目重点提及', '本期片目', '节目提及']
        list_pos_2 = ['往期节目', '下载', '抽奖', '获奖', '本周热映新片', '本周新推送节目', '片子基本信息', '耳旁风', '立刻收听', '若批评不自由，则赞美无意义']
        self._pos_1 = self.find_pos(list_pos_1, self._shownotes)
        self._pos_2 = self._pos_1 + self.find_pos(list_pos_2, self._shownotes[self._pos_1:])

        episode['film_list_range'] = (self._pos_1, self._pos_2)
        episode['film_list_original'] = self._shownotes[self._pos_1:self._pos_2]
        episode['film_list'] = self.pars_film_list(episode['film_list_original'])

        episode['film_outline'] = self.pars_outline(self._shownotes[:self._pos_1])
        episode['film_scoring'] = self.pars_scoring(self._shownotes[:self._out_pos])

    
    # find the beginning position of some sections, film list, outline, scoring
    def find_pos(self, key_words, section):
        pos = len(section)
        for word in key_words:
            k = section.find(word)
            pos = k if k > -1 and k < pos else pos
        return pos if pos < len(section) else -1


    def pars_outline(self, section):
        out_key = ['本期节目流程', '节目流程']
        self._out_pos = self.find_pos(out_key, section)
        return section[self._out_pos:] if self._out_pos > -1 else ''


    def pars_scoring(self, section):
        sc_key = ['综合分数', '主播打分', '评分', '总分']
        sc_pos = self.find_pos(sc_key, section)
        return section[sc_pos:] if sc_pos > -1 else ''

    def pars_film_list(self, section):
        pattern = r'《([^》]*)》[^《》]*?\(?[^)]*?([0-9]{4}|[0-9]{4}-[0-9]{4})[^)]*?\)?'
        
        matches = re.findall(pattern, section)
        res = []
        for name, time in matches:
            tmp = {}
            tmp['name'] = name
            tmp['time'] = time
            res.append(tmp)
        return res




def parse_film_shownotes(episode):
    """parse film shownotes

    Args:
        item: str

    Returns:
        no return value
    """
    shownotes = episode['shownotes'][0]
    st = ['本期节目重点提及', '本期片目', '节目提及']
    ed = ['往期节目', '下载', '抽奖', '获奖', '本周热映新片', '本周新推送节目', '片子基本信息', '耳旁风', '立刻收听', '若批评不自由，则赞美无意义']
    start = len(shownotes)

    # get the position of film list
    for st_key in st:
        k = shownotes.find(st_key)
        start = k if k > -1 and k < start else start
    shownotes = shownotes[start:]
    end = len(shownotes)
    for ed_key in ed:
        k = shownotes.find(ed_key)
        end = k if k > -1 and k < end else end
    shownotes = shownotes[:end]
    film_list_range = (start, start+end)
    res = {}
    
    episode['film_list_original'] = shownotes
    episode['film_list_range'] = film_list_range

    # get film list from shortened string
    pattern = r'《([^》]*)》[^《》]*?\(?[^)]*?([0-9]{4}|[0-9]{4}-[0-9]{4})[^)]*?\)?'
    matches = re.findall(pattern, shownotes)
    res = []
    for name, time in matches:
        tmp = {}
        tmp['name'] = name
        tmp['time'] = time
        res.append(tmp)
    episode['film_list'] = res

    # get the outline of the episode
    outline_index = episode['shownotes'][0][:start].find('本期节目流程')
    if outline_index > -1:
        episode['film_outline'] = episode['shownotes'][0][outline_index:start]
    else :
        episode['film_outline'] = '❌'

    # get the scoring of the spisode
    sc = ['综合分数', '主播打分', '评分', '总分']
    sc_index = len(episode['shownotes'][0])
    for sc_key in sc:
        k =  episode['shownotes'][0][:outline_index].find(sc_key)
        sc_index = k if k > -1 and k < sc_index else sc_index
    if sc_index > -1:
        episode['film_scoring'] = episode['shownotes'][0][sc_index:outline_index]
    else :
        episode['film_scoring'] = '❌'




ORIGINAL_PATH = '/Users/reyshawn/Desktop/FanpieFilm/fanPie/output.json'
OUTPUT_PATH = '/Users/reyshawn/Desktop/output.json'


def load_data(path, output):
    with open(path, 'r') as f:
        data = json.load(f)
    
    for i in range(len(data)):
        x = NotesParser(data[i])
    
    with open(output, 'w+') as f:
        json.dump(data, f, ensure_ascii=False)


def test_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    
    res = []
    for i in range(len(data)):
        tmp = {}
        tmp['episode'] = data[i]['episode']
        tmp['outline'] = data[i]['film_outline']
        res.append(tmp)

    with open('/Users/reyshawn/Desktop/outline.json', 'w+') as f:
        json.dump(res, f, ensure_ascii=False)

if __name__ == "__main__":
    load_data(ORIGINAL_PATH, OUTPUT_PATH)
    # test_data(OUTPUT_PATH)
    
    

    