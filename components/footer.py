import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def footer():

    footer_section = html.Div([
                    html.Div([
                        html.Div([
                            html.Div([html.Img(src='assets/src/plantify-logo-dark.png', className='footer-plantify-logo')], className=''),
                            html.P('¡Bienvenido a Plantify, tu destino para la revolución verde! Somos pioneros en sistemas de cultivo aeropónico modular, comprometidos con la sostenibilidad al utilizar materiales reciclados en la construcción de nuestras unidades. Descubre la innovación y la frescura en cada cosecha con Plantify. Convierte tu espacio en un oasis verde con nosotros.', className='footer-description'),
                        ], className='footer-description-container'),

                        html.Div([
                            
                            html.Div([
                                html.P('Navegación', className='footer-link-description'),
                                html.P('Inicio', className='footer-link-element'),
                                html.P('Sobre Nosotros', className='footer-link-element'),
                                html.P('Servicios', className='footer-link-element'),
                                html.P('Atributos', className='footer-link-element')
                            ], className='footer-link'),

                            html.Div([
                                html.P('Información', className='footer-link-description'),
                                html.P('Aviso legal', className='footer-link-element'),
                                html.P('Política de privacidad', className='footer-link-element'),
                                html.P('Centro de ayuda', className='footer-link-element'),
                                html.P('Preguntas frecuentes', className='footer-link-element')
                            ], className='footer-link'),

                            
                            html.Div([
                                html.P('Soporte', className='footer-link-description'),
                                html.P('+52 (55)-55-55-55', className='footer-link-element'),
                                html.P('soporte@plantify.mx', className='footer-link-element'),
                                html.P('Mario Pani 200, Lomas de Santa Fe, CDMX.', className='footer-link-element')
                            ], className='footer-link'),

                        ], className='footer-links')
                    ], className='footer-superior'),

                    html.Div([
                        html.Div([html.A('Copyright © 2023 - Todos los Derechos Reservados')], className = 'footer-copyright'),
                        html.Div([
                            html.Div([
                                html.Img(src='assets/src/1.png', className='footer-logo-image'),
                                html.Img(src='assets/src/2.png', className='footer-logo-image'),
                                html.Img(src='assets/src/3.png', className='footer-logo-image'),
                                html.Img(src='assets/src/4.png', className='footer-logo-image'),
                            ], className = 'footer-social-media-logos-container')
                        ], className = 'footer-social-media'),

                    ], className='footer-inferior')
                    ], className='footer')
    
    return footer_section