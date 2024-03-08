import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
from dash import callback

dash.register_page(__name__, path='/')

layout = html.Div([
    html.Div([

        # Barra de estado
         html.Div([
             html.Div([
                 html.Div([
                     html.A('32'),
                     html.A('Dias'),
                 ], className= 'status-bar-right-text'),
                  html.Hr(className='status-bar-right-vertical-line'),
             ], className = 'status-bar-right'),
             
             html.Div([
                 html.Div([
                    html.A('Estado del Sistema: Activo'),
                    html.A(['Último Riego: 14:45']),
                 ], className= 'status-bar-left-text'),
                 html.Div(html.Img(src = 'assets/src/load-button.png', className='load-button'), className='load-button-container')
             ], className = 'status-bar-left')
        ], className = 'status-bar'),

        # Cuadro Torre 
        html.Div([

            html.Div(html.Img(src = 'assets/src/aeroponic-tower.png', className='aero-image'), className='aero-image-container'),

            html.Div([
                html.Div([ html.A('Eleva tu experiencia de cultivo con Aeroponia'),], className = 'tower-description-top'),
                html.Div([
                    html.H3('Torre'),
                    html.A('Planta Baja')
                ], className = 'tower-description-bottom'),
            ], className = 'tower-description'),

            html.Div([
                html.A('hola')
            ], className='tower-buttons', 
        style={'backgroundImage': 'url(\'assets/src/leafs.png\')', 
               'backgroundSize': 'cover'}),

        ], className='tower-container', 
        style={'backgroundImage': 'url(\'assets/src/gray-background.png\')', 
               'backgroundSize': 'cover'})

    ], className = 'main'),
    html.H1('Holi esta es la pagina principal :)', className='title'),
], className='parent-container')

