import json
import os


def load(f_dir, file):
    with open(os.path.join(f_dir, file), 'r', encoding='utf-8') as load_f:
        data = json.load(load_f)
        return data


def save(data, f_dir, file):
    # ensure_ascii=False 表示不要以ascii码格式写入文件
    with open(os.path.join(f_dir, file), 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(data, indent=4, ensure_ascii=False))


