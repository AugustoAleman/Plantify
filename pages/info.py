import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from dash import callback

dash.register_page(__name__, path='/informacion')

layout = html.Div([
    html.H2('Información sobre la Torre Aeropónica', className='info-title'),
    html.Div([
        html.P('Aquí puedes encontrar información detallada sobre cómo funciona la torre aeropónica, '
               'los beneficios de utilizar esta tecnología para el cultivo de plantas, y consejos para '
               'maximizar tu rendimiento.', className='info-text'),
    ], className='info-section'),

    # Implementación de un Acordeón usando html.Details
    html.Div([
        html.Details([
            html.Summary('¿Qué es la aeroponía?'),
            html.P('La aeroponía es un sistema de cultivo en el aire...'),
        ]),
        html.Details([
            html.Summary('¿Cómo puedo empezar?'),
            html.P('Para comenzar con la aeroponía...'),
        ]),
        # Agrega más detalles según sea necesario
    ], className='faq-section'),

    # Galería de imágenes usando html.Img dentro de un contenedor
    html.Div([
        html.H3('Galería', className='gallery-title'),
        html.Img(src='assets/img1.jpg', className='image-gallery'),
        html.Img(src='assets/img2.jpg', className='image-gallery'),
        html.Img(src='assets/img3.jpg', className='image-gallery'),
        # Agrega más imágenes según sea necesario
    ], className='gallery-section'),
    


    # Formulario de contacto
    html.Div([
        html.H3('Contáctanos', className='contact-title'),
        html.Form([
            dcc.Input(placeholder='Nombre', type='text', className='contact-input'),
            dcc.Input(placeholder='Correo electrónico', type='email', className='contact-input'),
            dcc.Textarea(placeholder='Tu mensaje', className='contact-textarea'),
            html.Button('Enviar', type='submit', className='contact-submit'),
        ], className='contact-form'),
    ], className='contact-section'),

], className='main-info-page')
