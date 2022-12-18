# Importanto página inicial do dash
from app import app
from app import server
from app import primeira_vez

# Importando as páginas
from apps import sistema_hardware
from apps import sistema_arquivos
from apps import processos_threads
from apps import infos_memoria
from apps import terminal

from dash import dcc, html
from dash.dependencies import Input, Output, State


app.layout = html.Div([
        dcc.Location(id='url',refresh=False),
        html.A(
            href='/',
            children=html.Button(
                id='botao-inicio',
                n_clicks=0,
                children='Início',
            ),
            className='horizontal-divider',
        ),
        html.A(
            href='/apps/sistema_hardware.py',
            children=html.Button(
                id='botao-sistema-hardware',
                n_clicks=0,
                children='Sistema (hardware e SO)',
            ),
            className='horizontal-divider',
        ),
        html.A(
            href='/apps/processos_threads.py',
            children=html.Button(
                id='botao-processos-threads',
                n_clicks=0,
                children='Processos/Threads',
            ),
            className='horizontal-divider',
        ),
        html.A(
            href='/apps/sistema_arquivos.py',
            children=html.Button(
                id='botao-sistema-arquivos',
                n_clicks=0,
                children='Sistemas de Arquivos',
            ),
            className='horizontal-divider',
        ),
        html.A(
            href='/apps/infos_memoria.py',
            children=html.Button(
                id='botao-infos-memoria',
                n_clicks=0,
                children='Memória',
            ),
            className='horizontal-divider',
        ),
        html.A(
            href='/apps/terminal.py',
            children=html.Button(
                id='botao-terminal',
                n_clicks=0,
                children='Terminal',
            ),
            className='horizontal-divider',
        ),
        html.Div(id='page-content', children=[])
    ],
    # className='container',
)


@app.callback(
    Output(
        component_id='page-content',
        component_property='children'
    ),
    [
        Input(
            component_id='url',
            component_property='pathname'
        )
    ]
)
def update_output(pathname):
    if(pathname == '/apps/sistema_hardware.py'):
        app.primeira_vez = False
        return sistema_hardware.layout

    if(pathname == '/apps/processos_threads.py'):
        app.primeira_vez = False
        return processos_threads.layout

    if(pathname == '/apps/sistema_arquivos.py'):
        app.primeira_vez = False
        return sistema_arquivos.layout

    if(pathname == '/apps/infos_memoria.py'):
        app.primeira_vez = False
        return infos_memoria.layout

    if(pathname == '/apps/terminal.py'):
        app.primeira_vez = False
        return terminal.layout
        
    if(pathname == '/' and primeira_vez == False):
        app.primeira_vez = True
        return app.layout


if __name__ == '__main__':
    app.run_server(debug=True)