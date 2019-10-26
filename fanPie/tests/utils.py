import json

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


if __name__ == "__main__":
    pass