from dash import dcc, html
from dash.dependencies import Input, Output

def funcao():
    pass

layout = html.Div([
    html.P(funcao()),
    html.Br(),
    html.P('Na tela do Sistema Hardware e SO'),
])