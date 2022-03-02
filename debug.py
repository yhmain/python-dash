import os

from configer import get_prepare_dir, get_finish_dir
from file_IO import load


json_data = load(os.path.join(get_finish_dir(), 'labelSentences.json'))  # 加载文件
json_content = json_data['data'][0]['content']
json_num = json_data['data'][0]['sentencesNum']
json_labels = json_data['data'][0]['labels']
print(json_data['data'][0].keys())
