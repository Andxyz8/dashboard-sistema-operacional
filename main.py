# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import subprocess, os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Button(id='submit-button-state', n_clicks=0, children='Sistema (hardware e SO)'),
    html.Button(id='submit-button-state', n_clicks=0, children='Processos/Threads'),
    html.Button(id='submit-button-state', n_clicks=0, children='Sistemas de Arquivos'),
    html.Button(id='submit-button-state', n_clicks=0, children='Memória'),
    html.Button(id='submit-button-state', n_clicks=0, children='Terminal'),
    html.Div(id='output-state')
])


@app.callback(Output('output-state', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'))
              
            
def update_output(n_clicks, input1, input2):
    
    return u'''
        The Button has been pressed {} times,
        Input 1 is " {} ",
        and Input 2 is "{}"
    '''.format(n_clicks, input1, input2)


if __name__ == '__main__':
    app.run_server(debug=True)
