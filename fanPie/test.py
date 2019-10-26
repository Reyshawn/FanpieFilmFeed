import json
import re

# re = r'《([^》]*)》[ ]*?[(|（]?[^()（）]*?([0-9]{4})[)|）]?'


class NotesParser:
    
    def __init__(self, episode):
        episode['shownotes']['shownotes_original'] = episode['shownotes']['shownotes_original'].replace('&nbsp;', ' ')
        self._shownotes = episode['shownotes']['shownotes_original']
        list_pos_1 = ['本期节目重点提及', '本期片目', '节目提及', '本期节目重点提及的电影片单']
        list_pos_2 = ['往期节目', '若想下载', '安卓用户下载', '抽奖', '获奖', '本周热映新片', '本周新推送节目', '片子基本信息', '耳旁风', '立刻收听', '若批评不自由，则赞美无意义', '2018年其它']
        self._pos_1 = self.find_pos(list_pos_1, self._shownotes)
        self._pos_2 = self._pos_1 + self.find_pos(list_pos_2, self._shownotes[self._pos_1:])

        episode['shownotes']['film_list_range'] = (self._pos_1, self._pos_2)
        episode['shownotes']['film_list_original'] = self._shownotes[self._pos_1:self._pos_2]
        episode['shownotes']['film_list'] = self.pars_film_list(episode['shownotes']['film_list_original'])

        episode['shownotes']['film_outline'] = self.pars_outline(self._shownotes[:self._pos_1])
        episode['shownotes']['film_scoring'] = self.pars_scoring(self._shownotes)

    
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
        return section[self._out_pos:] if self._out_pos > -1 else '❌'


    def pars_scoring(self, section):
        sc_key = ['综合分数', '主播打分', '评分', '总分']
        if self._out_pos > -1:
            section = section[:self._out_pos]
        else:
            section = section[self._pos_1:self._pos_2]
        sc_pos = self.find_pos(sc_key, section)
        return section[sc_pos:] if sc_pos > -1 else '❌'

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


def parse_xml(data):
    pass



ORIGINAL_PATH = '/Users/reyshawn/Desktop/FanpieFilm/fanPie/output.json'
OUTPUT_PATH = '/Users/reyshawn/Desktop/output.json'


def load_data(path, output):
    with open(path, 'r') as f:
        data = json.load(f)
    
    for i in range(len(data)):
        # x = NotesParser(data[i])
        pass
    
    with open(output, 'w+') as f:
        json.dump(data, f, ensure_ascii=False)


def test_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    
    for i in range(len(data)):
        try:
            if data[i]['url'] == '':
                print(i)
                print(data[i]['episode'])
        except:
            print(i)
            print('episode', data[i]['episode'])

    # with open('/Users/reyshawn/Desktop/test.json', 'w+') as f:
    #     json.dump(res, f, ensure_ascii=False)

if __name__ == "__main__":
    # load_data(ORIGINAL_PATH, OUTPUT_PATH)
    # test_data(OUTPUT_PATH)
    pass