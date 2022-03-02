import dash
import dash_bootstrap_components as dbc
import dash_uploader as du
import os

from dash import html, dcc
from dash.dependencies import Input, Output, State, MATCH

# 一下是导入自己写的库
from translator import google_trans
from file_IO import load, save
from file_view import upload_view, change_page_view
from configer import get_prepare_dir, get_finish_dir
from page_view import get_load_layout, generate_load_layout

# 全局变量
# EN_JSON_DATA = None  # eg.存储9篇文章
PREPARE_PATH = get_prepare_dir()
FINISH_PATH = get_finish_dir()
user_session = {'rows': None, 'en_json_data': None, 'title': None, 'trans_label': None, 'page_label': None,
                'pre_index': None, 'next_index': None, 'now_index': None}

# app 程序
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = 'Marking Tool v1.0'
app.config.suppress_callback_exceptions = True  # 消除：起始layout不含有id，似乎不起效果

du.configure_upload(app, PREPARE_PATH, use_upload_id=False)

app.layout = html.Div(
    [
        dbc.Container(
            upload_view()
        ),
        # 水平线
        html.Hr(),
        # fluid设置为True
        dbc.Container(
            [
                html.Div(id="index-lab", style={'float': 'left'}),
                html.Div(change_page_view(), style={'float': 'right'}),
                dcc.Loading(
                    dbc.Table(
                        [
                            html.Thead(html.Tr(html.Th(id='title', colSpan=12,
                                                       style={'text-align': 'center', 'vertical-align': 'middle'}))),
                            html.Tbody(id='rows')
                        ]
                    ), type='dot'
                )
            ],
            fluid=True
        )
    ]
)


@app.callback(
    [Output('rows', 'children'), Output('title', 'children'),
     Output('notice-load', 'children'), Output('notice-load', 'color'),
     Output('index-lab', 'children'),
     Output('save-btn', 'style'),
     Output('pre-btn', 'style'),
     Output('next-btn', 'style')
     ],
    [Input('load-btn', 'n_clicks'), Input('load-btn', 'value'),
     Input('pre-btn', 'n_clicks'), Input('next-btn', 'n_clicks'),
     Input('save-btn', 'n_clicks'), Input('save-btn', 'style')
     ],
    State('file-list-check', 'value'),
    prevent_initial_call=True  # 阻止初始回调
)
def load_article(load_n_clicks, load_value, pre_n_clicks, next_n_clicks, save_n_clicks, btn_style, file):
    global user_session
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'load-btn.n_clicks':
        load_value = int(load_value)
        if file is None:
            return dash.no_update, dash.no_update, 'Please select a file.', 'warning', dash.no_update, dash.no_update, dash.no_update, dash.no_update
        # 加载文件
        try:
            fin_list = os.listdir(FINISH_PATH)
            if file not in fin_list:
                return dash.no_update, dash.no_update, "You should translate file {0} first.".format(
                    file), 'danger', dash.no_update, dash.no_update, dash.no_update, dash.no_update
            en_data, user_session['rows'], user_session['en_json_data'], user_session['cn_json_data'] = get_load_layout(
                file, load_value - 1)
            user_session['trans_label'] = "File: {0}.".format(file)
            size = len(user_session['en_json_data']['data'])
            pre_index = size if load_value == 1 else load_value - 1
            next_index = 1 if load_value == size else load_value + 1
            user_session['page_label'] = dbc.Label('Page: {0}/{1}'.format(load_value, size))
            user_session['pre_index'] = pre_index
            user_session['next_index'] = next_index
            user_session['now_index'] = load_value
            user_session['title'] = user_session['en_json_data']['data'][user_session['now_index'] - 1]['title']
            btn_style['display'] = 'inline'
            return user_session['rows'], user_session['title'], user_session['trans_label'], 'success', user_session[
                'page_label'], btn_style, btn_style, btn_style
        except FileNotFoundError:
            return dash.no_update, dash.no_update, 'The file content is not in the correct format.', 'danger', dash.no_update, dash.no_update, dash.no_update, dash.no_update
    # 对于前进和后退按钮，直接从当前session读取数据，生成布局
    elif ctx.triggered[0]['prop_id'] == 'pre-btn.n_clicks':
        pre_value = user_session['pre_index']
        user_session['now_index'] = pre_value
        size = len(user_session['en_json_data']['data'])
        pre_index = size if pre_value == 1 else pre_value - 1
        next_index = 1 if pre_value == size else pre_value + 1
        user_session['page_label'] = dbc.Label('Page: {0}/{1}'.format(pre_value, size))
        user_session['pre_index'] = pre_index
        user_session['next_index'] = next_index
        user_session['title'] = user_session['en_json_data']['data'][user_session['now_index'] - 1]['title']
        user_session['rows'] = generate_load_layout(
            user_session['en_json_data']['data'][user_session['now_index'] - 1]['content'],
            user_session['cn_json_data']['data'][user_session['now_index'] - 1]['labels'],
            user_session['cn_json_data']['data'][user_session['now_index'] - 1]['content']
        )
        return user_session['rows'], user_session['title'], dash.no_update, dash.no_update, user_session[
            'page_label'], dash.no_update, dash.no_update, dash.no_update
    elif ctx.triggered[0]['prop_id'] == 'next-btn.n_clicks':
        next_value = user_session['next_index']
        user_session['now_index'] = next_value
        size = len(user_session['en_json_data']['data'])
        pre_index = size if next_value == 1 else next_value - 1
        next_index = 1 if next_value == size else next_value + 1
        user_session['page_label'] = dbc.Label('Page: {0}/{1}'.format(next_value, size))
        user_session['pre_index'] = pre_index
        user_session['next_index'] = next_index
        user_session['title'] = user_session['en_json_data']['data'][user_session['now_index'] - 1]['title']
        user_session['rows'] = generate_load_layout(
            user_session['en_json_data']['data'][user_session['now_index'] - 1]['content'],
            user_session['cn_json_data']['data'][user_session['now_index'] - 1]['labels'],
            user_session['cn_json_data']['data'][user_session['now_index'] - 1]['content']
        )
        return user_session['rows'], user_session['title'], dash.no_update, dash.no_update, user_session[
            'page_label'], dash.no_update, dash.no_update, dash.no_update
    elif ctx.triggered[0]['prop_id'] == 'save-btn.n_clicks':
        from file_IO import save
        save(user_session['en_json_data'], get_finish_dir(), file)
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


@app.callback(
    [Output({'type': 'text-content', 'index': MATCH}, 'style'),
     Output({'type': 'text-label', 'index': MATCH}, 'children'),
     Output({'type': 'text-label', 'index': MATCH}, 'style'),
     Output({'type': 'text-trans', 'index': MATCH}, 'style')
     ],
    [Input({'type': 'text-content', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'text-content', 'index': MATCH}, 'id'),
     Input({'type': 'text-content', 'index': MATCH}, 'style'),
     Input({'type': 'text-label', 'index': MATCH}, 'style'),
     Input({'type': 'text-trans', 'index': MATCH}, 'n_clicks')
     ],  # MATCH 表示特定的一个  ALL表示全部
    prevent_initial_call=True  # 阻止初始回调
)
def change_p_color(n_clicks, aid, style, lab_style, trans_click):
    ctx = dash.callback_context
    # print(ctx.triggered[0])
    global user_session
    article_index = user_session['now_index'] - 1
    if style['background-color'] == 'white':
        style['background-color'] = 'LightGreen'
        lab_style['background-color'] = 'LightGreen'
        upd_label = 'good'
        user_session['cn_json_data']['data'][article_index]['labels'][aid['index']] = 'good'  # 设置类别
    else:
        style['background-color'] = 'white'
        lab_style['background-color'] = 'white'
        user_session['cn_json_data']['data'][article_index]['labels'][aid['index']] = 'bad'  # 设置类别
        upd_label = 'bad'
    return style, '[{0}]: {1}'.format(aid['index'] + 1, upd_label), lab_style, style


@app.callback(
    Output('save-label', 'children'),
    Input('save-btn', 'n_clicks'),
    State('file-list-check', 'value'),
    prevent_initial_call=True  # 阻止初始回调
)
def save_json_data(n_clicks, file):
    global user_session
    # print(user_session['now_index'])
    # print(user_session['en_json_data']['data'][1]['labels'])
    # print(user_session['en_json_data']['data'][1]['title'])
    print('Save {0}'.format(file))
    from file_IO import save
    save(user_session['cn_json_data'], get_finish_dir(), file)
    return 'test'


# 翻译文件
@app.callback(
    [Output('do-trans', 'children'), Output('do-trans', 'color')],
    Input('translate-btn', 'n_clicks'),
    State('file-list-check', 'value'),
    prevent_initial_call=True  # 阻止初始回调
)
def translate_json_data(translate_n_clicks, file):
    if file is None:
        return 'Please select a file.', 'warning'
    try:
        # 检测是否已经被翻译
        fin_list = os.listdir(FINISH_PATH)
        if file in fin_list:
            return 'File has been translated.', 'success'
        json_data = load(PREPARE_PATH, file)
        for i in range(len(json_data['data'])):
            contents = json_data['data'][i]['content']
            for j in range(len(contents)):
                trans = contents[j]
                json_data['data'][i]['content'][j] = google_trans('en', 'zh', trans)
            if 'labels' not in json_data['data'][i].keys():  # 没有label标签，则新建
                json_data['data'][i]['labels'] = ['bad'] * (len(contents))
    except Exception as ex:
        print(ex)
        return 'The file content is not in the correct format.', 'danger'
    save(json_data, FINISH_PATH, file)
    return 'File {0} has been translated.'.format(file), 'success'


@app.callback(
    [Output('file-list-check', 'options'), Output('file-trans-check', 'options'), Output('do-delete', 'children'),
     Output('do-delete', 'color')],
    [Input('upload', 'isCompleted'), Input('delete-btn', 'n_clicks')],
    State('file-list-check', 'value'),
    State('file-trans-check', 'value'),
)
def render_file_list(isCompleted, delete_n_clicks, load_file, trans_file):
    cxt = dash.callback_context
    if cxt.triggered[0]['prop_id'] == 'delete-btn.n_clicks':  # 点击删除按钮
        if trans_file is None:
            return dash.no_update, dash.no_update, 'Please select a file.', 'warning'
        os.remove(os.path.join(FINISH_PATH, trans_file))
        print('Delete...{0}'.format(trans_file))
        return dash.no_update, [{'label': file, 'value': file} for file in
                                os.listdir(FINISH_PATH)], 'File{0} has been deleted.'.format(trans_file), 'success'
    else:
        if load_file is None or trans_file is None:
            return [{'label': file, 'value': file} for file in os.listdir(PREPARE_PATH)], [
                {'label': file, 'value': file} for file in os.listdir(FINISH_PATH)], dash.no_update, dash.no_update
        return [{'label': file, 'value': file} for file in os.listdir(PREPARE_PATH)], [{'label': file, 'value': file}
                                                                                       for file in os.listdir(
                FINISH_PATH)], dash.no_update, dash.no_update


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050, debug=True)
