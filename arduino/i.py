import serial
import dash
from dash import html, DiskcacheManager
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import sys

conn = serial.Serial('COM5', 9600)


