from dash import html
from dash import dcc
import dash_uploader as du
import dash_bootstrap_components as dbc


def upload_view():
    upload_frame = [
        html.H3('Marking Tool v1.0', style={'text-align': 'center'}),
        html.Hr(),
        html.P('File upload area: '),
        du.Upload(id='upload',
                  text='Click or drag files here to upload!',
                  text_completed='Uploaded successfully：',
                  max_files=1000),
        html.Hr(),
        dbc.Row(
            [dbc.Col(dbc.Spinner(dcc.Dropdown(id='file-list-check', placeholder="Please select a json file")), width=6),
             dbc.Col(dbc.Button('Load selected file', id='load-btn', value=1,
                                style={'margin-right': '20px', 'background-color': '#008CBA',
                                       'border-color': '#008CBA'}), width=3),
             dbc.Col(dbc.Button('Translate selected file', id='translate-btn',
                                style={'margin-right': '20px', 'background-color': '#008CBA',
                                       'border-color': '#008CBA'}), width=3),
             dbc.Tooltip('选择一个文件进行加载！', target='load-btn', placement='top'),
             dbc.Tooltip('选择一个文件进行翻译！', target='translate-btn', placement='top')
             ]),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dbc.Spinner(dcc.Dropdown(id='file-trans-check',
                                                 placeholder="Just delete a json file which has been translated."),
                                    id='spinner_check'), width=6),
                dbc.Col(dbc.Button('Delete selected file', id='delete-btn',
                                   style={'margin-right': '20px', 'background-color': '#008CBA',
                                          'border-color': '#008CBA'}), width=3),
                dbc.Tooltip('删除已翻译的文件，慎用！', target='delete-btn', placement='top')
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dcc.Loading(dbc.Alert(id='notice-load'), type='default')),
                dbc.Col(dcc.Loading(dbc.Alert(id='do-trans'), type='default')),
                dbc.Col(dcc.Loading(dbc.Alert(id='do-delete'), type='default'))
            ]
        )
    ]
    return upload_frame


def change_page_view():
    page_view = [
        dbc.Label(id='save-label'),
        dbc.Button('Save', id='save-btn',
                   style={'margin': '20px', 'background-color': '#008CBA', 'border-color': '#008CBA',
                          'display': 'none'}),
        dbc.Button('Previous', id='pre-btn',
                   style={'margin': '20px', 'background-color': '#008CBA', 'border-color': '#008CBA',
                          'display': 'none'}),
        dbc.Button('Next', id='next-btn',
                   style={'margin': '20px', 'background-color': '#008CBA', 'border-color': '#008CBA',
                          'display': 'none'})
    ]
    return page_view
