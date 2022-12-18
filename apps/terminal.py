from app import app
from dash import dcc, html
from dash.dependencies import Input, Output, State
import subprocess


def funcao(comando):
    qualquer = subprocess.run(comando, text=True, capture_output=True)

    return str(qualquer.stdout)

comando = ''

layout = html.Div([
        html.Div([
                html.Hr(),
                html.Center(
                    html.H1('Terminal'),
                ),
                html.Hr(),
            ],
            className='div-terminal-titulo',
        ),
        html.Div([
                html.Div(
                    html.Textarea(
                        id='comando-executar',
                        children='ls',
                        autoFocus=True,
                        className='terminal-textArea',
                    ),
                    className='terminal-div-textArea',
                ),
                html.Div(
                    children = [
                        html.Button(
                            'Executar',
                            id='execute-button',
                            n_clicks=0,
                            type='submit',
                            className='terminal-botaoExecutar',
                        ),
                    ],
                    className='terminal-div-botaoExecutar',
                ),
            ],
        ),
        html.Div(
            id='div-area-retorno',
            children=[
                funcao('pwd')
            ],
            className='terminal-area-retorno',
        ),
    ],
    className='terminal-div-viewport'
)


# add a click to the appropriate store.
@app.callback(
    Output(
        component_id='div-area-retorno', 
        component_property='children'
    ),
    [
        Input(
            component_id='comando-executar', 
            component_property='children'
        )
    ]
    ,
    State(
        component_id='execute-button',
        component_property='n_clicks'
    )
)
def on_click(comando, n_clicks_botao):
    return funcao(comando)