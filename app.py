# -*- coding: utf-8 -*-
from dash import Dash

# external_stylesheets = ['paleta_estilos.css']

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{
        'name':'viewport',
        #'content':'widht=device-width, initian-scale=1.0'
    }]
)

primeira_vez = True
server = app.server
