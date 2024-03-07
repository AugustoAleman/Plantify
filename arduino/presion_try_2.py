# Programa procesamiento e interpretación de datos cálculo presión
# Hecho para arduino UNO con módulo serial

import serial, pygame, sys, os, math
import numpy as np

PORT_INPUT = []
INPUT_FREQ = 9600

FPS = 3
WINDOWHEIGHT = 600 #DE PREFERENCIA UN NÚMERO DIVISIBLE ENTRE 10
WINDOWWIDTH = 1265  # 23*40 DE PREFERENCIA UN MÚLTIPLO DE 23
CIRCLESIZE = 20
HUNIT = WINDOWWIDTH/23
YUNIT = WINDOWHEIGHT/10

#Colors   R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (70, 70, 70)
YELLOW = (100, 99, 22)
BG_COLOR = DARK_GRAY


num_avg = [None for i in range(3)]

def Main():
    global FPSCLOCK, DISPLAYSURF, arduino, port, coords, font, slope, font_f, y_diff, counter, avg_coords, font_txt, iterations
    avg_coords = [0 for j in range(3)]
    
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Calculadora presión")
    
    
    port = findPort()
    arduino = serial.Serial (port, INPUT_FREQ)
    font = pygame.font.Font('Digital-7.ttf', 90)
    font_f = pygame.font.Font('20THCENT.TTF', 60)
    font_txt = pygame.font.Font('20THCENT.TTF', 30)
    
    coords = getCoords()
    slope, y_diff = matematicas()
    counter = 0
    iterations = 3
    
    
    
    while True:
        
        runApp()
           
def runApp():
    global counter, avg_coords
    for event in pygame.event.get():
        if event.type == 256:
            terminate()
            
    value = getData(arduino)

    y_2 = [0 for i in range(3)]
    
    for iter in range(3):
        y_temp = value[iter]*slope
        y_2[iter] = y_temp -  y_diff
        
    
    num_avg[counter] = y_2 
    counter +=1
    
    avg_coords[0].append(y_2[0])
    avg_coords[1].append(y_2[1])
    avg_coords[2].append(y_2[2])

    if counter == iterations:
        avg_temp[0] = np.average(avg_coords[0])
        avg_temp[1] = np.average(avg_coords[1])
        avg_temp[2] = np.average(avg_coords[2])
        
        Q = getFlux (avg_temp[1])
        print (Q)
        drawBoard(coords, avg_coords, Q)
        counter = 0    
    
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    
def terminate():
    pygame.quit()
    sys.exit()
    
####################################
####################################


def getCoords():
    #HORIZONTALY, 5 PER SQUARE, 2 PER GAP
    coord_list = [{} for i in range(3)]
    for i in range(3):
        
        coord_list[i]['x'] = HUNIT*4*i + HUNIT*((i*4)+1)
        coord_list[i]['y'] = YUNIT * 3
    ###print(coord_list)
    
    return coord_list

def drawBoard(coords, values, flujo):
    DISPLAYSURF.fill(BG_COLOR)
    texts = ['P positiva [Bar]', 'P diferencial [Bar]', 'P negativa [Bar]']
    T_COLOR = WHITE
    for m in range (len(coords)):
        
        #PRIMERO SE REDONDEAN VALORES DE VALUES
        
        value_temp = round(values[m], 2)
        
        pygame.draw.rect(DISPLAYSURF, GREEN, (coords[m]['x'], coords[m]['y'], 5*HUNIT, 2.5*YUNIT))
        
        voltText_temp = font.render(str(value_temp), True, BLACK, GREEN)
        voltText_temp_R = voltText_temp.get_rect()
        voltText_temp_R.center = (coords[m]['x']+(HUNIT*2.5),coords[m]['y']+(YUNIT*1.5)) 
        
        
        
        text1 = font_txt.render(texts[m], True, T_COLOR, DARK_GRAY)
        text1_R = text1.get_rect()
        
        text1_R.center = (coords[m]['x']+(HUNIT*2.5),coords[m]['y'])
                          
                          
        DISPLAYSURF.blit(voltText_temp, voltText_temp_R)
        DISPLAYSURF.blit(text1, text1_R)
    pygame.draw.rect(DISPLAYSURF, GREEN, (HUNIT*3.5,YUNIT*8, 14*HUNIT, 1.4*YUNIT))
    
    
    text_calc = 'Flujo hidraulico: ' + str(flujo) + ' [mL/s]'
    calcText = font_f.render(text_calc, True, BLACK, GREEN)
    calcText_R = voltText_temp.get_rect()
    calcText_R.topleft = ((HUNIT*4),(YUNIT*8)) 
    
    DISPLAYSURF.blit(calcText, calcText_R)
    
    for m in range (3):
        pass

    
def getData(arduino):
    
        
    data_temp = str(arduino.readline())
    
    voltMax, voltDiff, voltMin = data_temp.split(',')
    voltMax = voltMax.strip('b\'')
    voltDiff=voltDiff.strip(' ')
    
    voltMin=voltMin.strip('\\r\\n\'')
        
    voltMax = int(voltMax)
    voltDiff = int(voltDiff)
    voltMin = int(voltMin)
    
    div_rate = float(204.6)  #204.6 = 1023/5

    volts ={0:voltMax/div_rate, 1:voltDiff*0.5/div_rate, 2:voltMin/div_rate}
#Se usa idea que value va de 0-1023

    return volts

def findPort():
    for p in range(1, 8):
        num = str(p)
        port_temp = 'COM' + num
        
        try:
            serial.Serial(port_temp, INPUT_FREQ)
        
        except:
            continue
        return port_temp
        
    print('No se encuentra el dispositivo')
    terminate()            
        
def getFlux(P):
    Q = 1
    try:
        dP = P*100000

        dens = 1000
        A2 = math.pi * (0.005**2)
        A1 = math.pi * (0.007**2)
        Q = 1000*A2 * math.sqrt((dP/dens)*(1/(1-((A2**2)/((A1**2))))))
        print (Q)
        return round(Q, 3)
    except:
        print ('Sensores conectados al revés')
        return Q

    
    

def matematicas():
    voltage_div = 3
    RES = 830
    Amp_min = 0.004; Amp_max = 0.020
    
    V_min = (Amp_min * RES) - voltage_div; V_max = (Amp_max * RES) - voltage_div
    f_slope = 3/(V_max - V_min)
    y_diff = f_slope * V_max - 3
    return f_slope, y_diff
        

if __name__ == '__main__':
    Main()

