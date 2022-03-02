import os

import dash_bootstrap_components as dbc
from dash import html

from configer import get_prepare_dir, get_finish_dir
from file_IO import load

# 颜色映射
color_map = {'good': 'LightGreen', 'bad': 'white'}


# 读取第index篇
def get_load_data_en(file, index=0):
    json_data = load(get_prepare_dir(), file)  # 加载文件
    return json_data, json_data['data'][index]


# 读取第index篇
def get_load_data_cn(file, index=0):
    json_data = load(get_finish_dir(), file)  # 加载文件
    return json_data, json_data['data'][index]


# 主！！！！！！！！！！！！！！！！！
def get_load_layout(file, index=0):
    cn_json_data, cn_data = get_load_data_cn(file, index)
    en_json_data, en_data = get_load_data_en(file, index)
    rows = generate_load_layout(en_data['content'], cn_data['labels'], cn_data['content'])
    return en_data, rows, en_json_data, cn_json_data


# content: 一篇文章的list内容
def generate_load_layout(content, content_label, translate):
    # 非good类型的类别全部默认为bad
    for j in range(len(content_label)):
        content_label[j] = 'bad' if content_label[j] != 'good' else 'good'
    rows = []
    for i in range(len(content)):
        # type 分组   动态加载颜色
        c = color_map[content_label[i]] if content_label[i] in color_map.keys() else 'white'
        row = html.Tr(
            [html.Td('[{0}]: {1}'.format(i + 1, content[i]), id={'type': 'text-content', 'index': i}, n_clicks=0,
                     style={'background-color': c, 'border': '1px solid', 'text-align': 'center', 'vertical-align': 'middle', 'width': "50%"}),
             html.Td('[{0}]: {1}'.format(i + 1, content_label[i]), id={'type': 'text-label', 'index': i}, n_clicks=0,
                     style={'background-color': c, 'border': '1px solid', 'text-align': 'center', 'vertical-align': 'middle', 'width': "6%"}),
             html.Td('[{0}]: {1}'.format(i + 1, translate[i]), id={'type': 'text-trans', 'index': i}, n_clicks=0,
                     style={'background-color': c, 'border': '1px solid', 'text-align': 'center', 'vertical-align': 'middle', 'width': "40%"})
             ])
        rows.append(row)
    return rows
