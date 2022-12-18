from app import app
from dash import dcc, html
from dash.dependencies import Input, Output, State
import subprocess


def executa_comando_terminal(comando):
    comando_executado = subprocess.run(
        args=comando,
        shell=True,
        capture_output=True,
        universal_newlines=True
    )
    print(comando_executado.stdout)
    return comando_executado.stdout


layout = html.Div(
    [
        html.Div(
            [
                html.Hr(),
                html.Center(
                    html.H1('Terminal'),
                ),
                html.Hr(),
            ],
            className='div-terminal-titulo',
        ),
        html.Div(
            [
                html.Div(
                    dcc.Input(
                        id='input-comando',
                        value='',
                        type='text',
                        debounce=True,
                        autoFocus=True,
                        className='terminal-textArea',
                    ),
                    className='terminal-div-input',
                ),
                html.Div(
                    children = [
                        html.Button(
                            'Executar',
                            id='execute-button',
                            className='terminal-botao-executar',
                        ),
                    ],
                    className='terminal-div-botao-executar',
                ),
            ],
        ),
        html.Div(
            [
                dcc.Textarea(
                    id='text-area-retorno',
                    value='',
                    disabled='true',
                    className='terminal-area-retorno',
                ),
                
            ],
            className='terminal-div-retorno',
        )
    ],
    className='terminal-div-viewport'
)


# add a click to the appropriate store.
@app.callback(
    [
        Output(
            component_id='text-area-retorno', 
            component_property='value'
        ),
        Output(
            component_id='input-comando', 
            component_property='value'
        ),
    ],
    [
        Input(
            component_id='input-comando', 
            component_property='value'
        )
    ]
)
def on_click(comando):
    if (not comando == ''):
        return executa_comando_terminal(comando), ''
    return '', ''
