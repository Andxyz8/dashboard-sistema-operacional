# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import subprocess, os


# external_stylesheets = ['paleta_estilos.css']

app = Dash(__name__)

app.layout = html.Div([
        html.Button(id='submit-button-state', n_clicks=0, children='Sistema (hardware e SO)', className='centered-element',),
        html.Div(id='separador-botoes', className='header-divider'),

        html.Button(id='submit-button-state', n_clicks=0, children='Processos/Threads', className='centered-element',),
        html.Div(id='separador-botoes', className='header-divider'),

        html.Button(id='submit-button-state', n_clicks=0, children='Sistemas de Arquivos', className='centered-element',),
        html.Div(id='separador-botoes', className='header-divider'),

        html.Button(id='submit-button-state', n_clicks=0, children='Memória', className='centered-element',),
        html.Div(id='separador-botoes', className='header-divider'),

        html.Button(id='submit-button-state', n_clicks=0, children='Terminal', className='centered-element',),
        #html.Div(id='output-state')
    ],
    className='container',
)


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
    #print(app.css.append_css(external_stylesheets))
    #print(app.css.get_all_css())
    app.run_server(debug=True)
