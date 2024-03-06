import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
from dash import callback

dash.register_page(__name__, path='/')

layout = html.Div([
        html.H1('Holi esta es la pagina principal :)', className='title'),
])

