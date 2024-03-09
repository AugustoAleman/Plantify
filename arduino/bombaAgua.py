import serial
import dash
import dash_daq as daq
from dash import html, DiskcacheManager, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import time
import datetime


import ngrok

import sys

INPUT_FREQ = 19200

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def findPort():
    for p in range(1,8):
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


# @app.callback(
#     Output("outputState", "children"),
#     Input("activarBomba", "n_clicks")
    
# )
# def activateWaterPump(n_clicks):
#     pass
#     # Serial.

@app.callback(
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


# @app.callback(
#     Output('outputState', 'children'),
#     Input('readSerial', 'n_intervals')
# )
# def readSerial(n_intervals):
#     try:
            
#         for line in arduino.readline():
#             if line == 'b':
#                 print("b")
#                 arduino.flushInput()
#                 return line
#         print(line)
#         return line
#     except:
        # return "none"

#prevent initial callback
@app.callback(
    Output('outputState2', 'children'),
    [Input('interval-component', 'n_intervals'),
     Input('automatic-switch', 'value')]
)
def control_pump(n, automatic):
    if automatic:  # Check if automatic mode is enabled
        now = datetime.datetime.now()
        second_in_minute = now.second  # Get the current second within the minute

        if 0 <= second_in_minute < 30:  # First 30 seconds of the minute
            arduino.write('a'.encode())  # Turn on the water
            return "Automatic mode: Pump turned on"
        else:  # Last 30 seconds of the minute
            arduino.write('o'.encode())  # Turn off the water
            return "Automatic mode: Pump turned off"
    
    return "Manual mode: Control the pump using the first switch"


app.layout = dbc.Container([
    daq.ToggleSwitch(id = "activarBomba", value = False, color = "green"),
    # dcc.Interval(id='readSerial', interval=1),
    daq.ToggleSwitch(id="automatic-switch", value=False, color="blue", label="Automatic Mode"),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),  # Update every second

    html.P(id = "outputState"), 
    html.P(id = "outputState2")
])



if __name__ == '__main__':
    
    
    app.run_server(debug = True, port = 8050)