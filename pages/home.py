import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
from dash import callback, dcc, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import serial
import sys

dash.register_page(__name__, path='/')

INPUT_FREQ = 19200


def findPort():
    for p in range(1,10):
        num = str(p)
        port_temp = 'COM' + num
        print(port_temp)

        try:
            serial.Serial(port_temp, INPUT_FREQ)
            # serial.Serial.close()
        except serial.SerialException:
            continue
        return port_temp
    
    print("No se encuentra el dispositivo")
    terminate()



def terminate():
    sys.exit()

port = findPort()
print("port:",port)
# port = 'COM8'
arduino = serial.Serial(port, INPUT_FREQ)
print("start app")

@callback(
    Output('outputState', 'children'),
    Input('activarBomba', 'value')
)
def activarBombeo(value):
    if value:
        print("bombeando")
        arduino.write('a'.encode())
    else:
        print("deteniendo")
        arduino.write('o'.encode())

    print("bombeando")
    return "none"

@callback(
    Output('outputState2', 'children'),
    [Input('interval-component', 'n_intervals'),
     Input('automatic-switch', 'value')]
)
def control_pump(n, automatic):
    if automatic:  # Check if automatic mode is enabled
        now = datetime.now()
        second_in_minute = now.second  # Get the current second within the minute

        if 0 <= second_in_minute < 30:  # First 30 seconds of the minute
            arduino.write('a'.encode())  # Turn on the water
            return "Automatic mode: Pump turned on"
        else:  # Last 30 seconds of the minute
            arduino.write('o'.encode())  # Turn off the water
            return "Automatic mode: Pump turned off"
    
    return "Manual mode: Control the pump using the first switch"


layout = html.Div([
    html.Div([

        # Barra de estado
        html.Div([
            html.Div([
                html.Div([
                    html.A('32'),
                    html.A('Dias'),
                ], className='status-bar-right-text'),
                html.Hr(className='status-bar-right-vertical-line'),
            ], className='status-bar-right'),

            html.Div([
                html.Div([
                    html.A('Estado del Sistema: Activo'),
                    html.A(['Último Riego: 14:45']),
                ], className='status-bar-left-text'),
                html.Div(html.Img(src='assets/src/load-button.png', className='load-button'), className='load-button-container')
            ], className='status-bar-left')
        ], className='status-bar'),

        # Cuadro Torre 
        html.Div([

            html.Div(html.Img(src='assets/src/aeroponic-tower.png', className='aero-image'), className='aero-image-container'),

            html.Div([
                html.Div([html.A('Eleva tu experiencia de cultivo con Aeroponia')], className='tower-description-top'),
                html.Div([
                    html.H3('Torre'),
                    html.A('Planta Baja')
                ], className='tower-description-bottom'),
            ], className='tower-description'),

            html.Div([
                
                daq.ToggleSwitch(id = "activarBomba", value = False, color = "green"),
                # dcc.Interval(id='readSerial', interval=1),
                daq.ToggleSwitch(id="automatic-switch", value=False, color="blue", label="Automatic Mode"),
                dcc.Interval(id='interval-component', interval=1000, n_intervals=0),  # Update every second

                html.P(id = "outputState"), 
                html.P(id = "outputState2"),

                html.Div(html.Img(src='assets/src/on-off-button.png', className='on-off-image'), className='aero-image-container'),

                html.Div([
                    dcc.Link(html.Button(['Ver Detalles', html.Img(src='assets/src/arrow.png', className='arrow-image')],
                                         className='tower-rounded-button'), href='/', className='tower-rounded-button-container')
                ])

            ], className='tower-buttons',
                style={'backgroundImage': 'url(\'assets/src/leafs.png\')', 'backgroundSize': 'cover'}),

        ], className='tower-container',
            style={'backgroundImage': 'url(\'assets/src/gray-background.png\')', 'backgroundSize': 'cover'}),

        # Guias de Cuidado
        html.Div([

            html.Div([html.H2('Guías De Cuidado')], className='section-title'),

            html.Div([

                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Lechuga'),
                            html.A('Lactuca sativa')
                        ], className='guide-box-text'),
                        dbc.Button("Detalles", id="open-modal-btn", color="primary", className="modal-button"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Guía de Cuidado - Lechuga"),
                                dbc.ModalBody([
                                    html.P("Las lechugas son plantas de rápido crecimiento que se cultivan comúnmente en climas frescos."),
                                    html.P("Informacion básica:"),
                                    html.Ul([
                                        html.Li("Germinación: Se recomienda germinar las semillas en un sustrato ligero y mantenerlo húmedo."),
                                        html.Li("Período de crecimiento: Las lechugas suelen estar listas para cosechar en 40-60 días."),
                                        html.Li("Luz: Prefieren la luz solar indirecta y sombra parcial."),
                                        html.Li("Riego: Mantenga el suelo uniformemente húmedo."),
                                        html.Li("Nutrientes: Use un fertilizante equilibrado durante el crecimiento."),
                                    ])
                                ]),
                                dbc.ModalFooter(
                                    dbc.Button("Cerrar", id="close-modal-btn", className="ml-auto")
                                ),
                            ],
                            id="modal",
                        ),
                    ], className='guide-box',
                        style={'backgroundImage': 'url(\'assets/src/lettuce.png\')', 'backgroundSize': 'cover'}),
                ], className='guide-container'),

                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Brócoli'),
                            html.A('Brassica oleracea')
                        ], className='guide-box-text'),
                        dbc.Button("Detalles", id="open-modal-btn-brocoli", color="primary", className="modal-button"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Guía de Cuidado - Brócoli"),
                                dbc.ModalBody([
                                    html.P("Información sobre el cultivo de brócoli:"),
                                    html.Ul([
                                        html.Li("Germinación: Siembre las semillas en un sustrato bien drenado y manténgalo húmedo."),
                                        html.Li("Período de crecimiento: El brócoli suele estar listo para la cosecha en 70-100 días."),
                                        html.Li("Luz: Necesita luz solar directa y al menos 6 horas de luz al día."),
                                        html.Li("Riego: Riegue de manera uniforme, evitando que el suelo se seque por completo."),
                                        html.Li("Nutrientes: Use un fertilizante equilibrado y rico en nitrógeno."),
                                    ])
                                ]),
                                dbc.ModalFooter(
                                    dbc.Button("Cerrar", id="close-modal-btn-brocoli", className="ml-auto")
                                ),
                            ],
                            id="modal-brocoli",
                        ),
                    ], className='guide-box',
                        style={'backgroundImage': 'url(\'assets/src/broccoli.png\')', 'backgroundSize': 'cover'}),
                ], className='guide-container'),

                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Espinaca'),
                            html.A('Spinacia oleracea')
                        ], className='guide-box-text'),
                        dbc.Button("Detalles", id="open-modal-btn-spinach", color="primary", className="modal-button"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Guía de Cuidado - Espinaca"),
                                dbc.ModalBody([
                                    html.P("Información sobre el cultivo de espinaca:"),
                                    html.Ul([
                                        html.Li("Germinación: Siembre las semillas en un sustrato bien drenado y manténgalo húmedo."),
                                        html.Li("Período de crecimiento: La espinaca suele estar lista para la cosecha en 40-50 días."),
                                        html.Li("Luz: Prefiere la luz solar directa y también puede crecer en sombra parcial."),
                                        html.Li("Riego: Mantenga el suelo húmedo, evitando el encharcamiento."),
                                        html.Li("Nutrientes: Fertilice con un abono balanceado durante el crecimiento."),
                                    ])
                                ]),
                                dbc.ModalFooter(
                                    dbc.Button("Cerrar", id="close-modal-btn-spinach", className="ml-auto")
                                ),
                            ],
                            id="modal-spinach",
                        ),
                    ], className='guide-box',
                        style={'backgroundImage': 'url(\'assets/src/spinach.png\')', 'backgroundSize': 'cover'}),
                ], className='guide-container'),

                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Arúgula'),
                            html.A('Eruca vesicaria sativa')
                        ], className='guide-box-text'),
                        dbc.Button("Detalles", id="open-modal-btn-arugula", color="primary", className="modal-button"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Guía de Cuidado - Arúgula"),
                                dbc.ModalBody([
                                    html.P("Información sobre el cultivo de arúgula:"),
                                    html.Ul([
                                        html.Li("Germinación: Siembre las semillas en un sustrato bien drenado y manténgalo húmedo."),
                                        html.Li("Período de crecimiento: La arúgula suele estar lista para la cosecha en 40-50 días."),
                                        html.Li("Luz: Prefiere la luz solar directa y también puede crecer en sombra parcial."),
                                        html.Li("Riego: Mantenga el suelo húmedo, evitando el encharcamiento."),
                                        html.Li("Nutrientes: Fertilice con un abono balanceado durante el crecimiento."),
                                    ])
                                ]),
                                dbc.ModalFooter(
                                    dbc.Button("Cerrar", id="close-modal-btn-arugula", className="ml-auto")
                                ),
                            ],
                            id="modal-arugula",
                        ),
                    ], className='guide-box',
                        style={'backgroundImage': 'url(\'assets/src/arugula.png\')', 'backgroundSize': 'cover'}),
                ], className='guide-container'),

            ], className='guides-container')

        ], className='guides'),

        html.Div([

            html.Div([html.H2('Tips de Mantenimiento')], className='section-title'),

            html.Div([

                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Mantenimiento Modular'),
                        ], className='guide-box-text'),
                        dbc.Button("Detalles", id="open-modal-btn-modular-maintenance", color="primary",
                                   className="modal-button"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Tips de Mantenimiento - Mantenimiento Modular"),
                                dbc.ModalBody([
                                    html.P("El sistema está diseñado para ser modular, lo que significa que si una pieza se daña, puede ser reemplazada por esa pieza en particular."),
                                    html.P("Consejos de mantenimiento:"),
                                    html.Ul([
                                        html.Li("Verifique regularmente todas las piezas del sistema."),
                                        html.Li("En caso de daño, sustituya solo la pieza afectada."),
                                    ])
                                ])
                            ],
                            id="modal-modular-maintenance",
                        ),
                    ], className='guide-box',
                        style={'backgroundImage': 'url(\'assets/src/modular.png\')', 'backgroundSize': 'cover'}),
                ], className='guide-container'),

                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Devolución por Créditos'),
                        ], className='guide-box-text'),
                        dbc.Button("Detalles", id="open-modal-btn-return-for-credits", color="primary",
                                   className="modal-button"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Tips de Mantenimiento - Devolución por Créditos"),
                                dbc.ModalBody([
                                    html.P("En caso de una pieza dañada, esta puede ser devuelta a Plantify a cambio de créditos en su tienda virtual."),
                                    html.P("Proceso de devolución:"),
                                    html.Ul([
                                        html.Li("Contáctenos para iniciar el proceso de devolución."),
                                        html.Li("Envíe la pieza dañada de vuelta."),
                                        html.Li("Reciba créditos para usar en nuestra tienda virtual."),
                                    ])
                                ])
                            ],
                            id="modal-return-for-credits",
                        ),
                    ], className='guide-box',
                        style={'backgroundImage': 'url(\'assets/src/return.png\')', 'backgroundSize': 'cover'}),
                ], className='guide-container'),

                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Limpieza Regular'),
                        ], className='guide-box-text'),
                        dbc.Button("Detalles", id="open-modal-btn-regular-cleaning", color="primary",
                                   className="modal-button"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Tips de Mantenimiento - Limpieza Regular"),
                                dbc.ModalBody([
                                    html.P("La limpieza regular es esencial para el mantenimiento del sistema aeropónico."),
                                    html.P("Consejos de limpieza:"),
                                    html.Ul([
                                        html.Li("Limpieza de boquillas y conductos."),
                                        html.Li("Verificación de obstrucciones."),
                                        html.Li("Desinfección del sistema periódicamente."),
                                    ])
                                ])
                            ],
                            id="modal-regular-cleaning",
                        ),
                    ], className='guide-box',
                        style={'backgroundImage': 'url(\'assets/src/cleaning.png\')', 'backgroundSize': 'cover'}),
                ], className='guide-container'),

                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Nutrientes Balanceados'),
                        ], className='guide-box-text'),
                        dbc.Button("Detalles", id="open-modal-btn-balanced-nutrients", color="primary",
                                   className="modal-button"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Tips de Mantenimiento - Nutrientes Balanceados"),
                                dbc.ModalBody([
                                    html.P("El suministro de nutrientes equilibrados es crucial para el crecimiento de las plantas."),
                                    html.P("Consejos sobre nutrientes:"),
                                    html.Ul([
                                        html.Li("Use un fertilizante equilibrado según las necesidades de las plantas."),
                                        html.Li("Monitoreo regular de los niveles de nutrientes."),
                                        html.Li("Ajuste de la fórmula de nutrientes según las etapas de crecimiento."),
                                    ])
                                ])
                            ],
                            id="modal-balanced-nutrients",
                        ),
                    ], className='guide-box',
                        style={'backgroundImage': 'url(\'assets/src/nutrients.png\')', 'backgroundSize': 'cover'}),
                ], className='guide-container'),

                # Add more Tip cards following the same structure

            ], className='guides-container')

        ], className='guides')

    ], className='main'),
], className='parent-container')

@callback(
    Output("modal", "is_open"),
    [Input("open-modal-btn", "n_clicks"), Input("close-modal-btn", "n_clicks")],
    [dash.dependencies.State("modal", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@callback(
    Output("modal-brocoli", "is_open"),
    [Input("open-modal-btn-brocoli", "n_clicks"), Input("close-modal-btn-brocoli", "n_clicks")],
    [dash.dependencies.State("modal-brocoli", "is_open")]
)
def toggle_modal_brocoli(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@callback(
    Output("modal-spinach", "is_open"),
    [Input("open-modal-btn-spinach", "n_clicks"), Input("close-modal-btn-spinach", "n_clicks")],
    [dash.dependencies.State("modal-spinach", "is_open")]
)
def toggle_modal_spinach(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@callback(
    Output("modal-arugula", "is_open"),
    [Input("open-modal-btn-arugula", "n_clicks"), Input("close-modal-btn-arugula", "n_clicks")],
    [dash.dependencies.State("modal-arugula", "is_open")]
)
def toggle_modal_arugula(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open