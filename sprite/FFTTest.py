from machine import I2C,Pin
import math
import sprite,sh1106,random,time
import _thread as thread
import micropython
from FFT import DFT,FFT
pi = micropython.const(3.141593)
e = micropython.const(2.718282)
def init():
    global led0,led1,i2c,display,dds
    led0 = Pin(13,Pin.OUT,value = 0)
    led1 = Pin(12,Pin.OUT,value = 0)
    i2c = I2C(0,scl = Pin(18),sda = Pin(19))
    display = sh1106.SH1106_I2C(128,64,i2c)
    display.fill(0)
    
    dds = sprite.DataDisplayScreen(delta=1,length = 128)
    
init()

#dds.draw(display)

def FFF(freq):
    display.fill(0)
    for i in range(150):
        dds+(10*math.sin(i*freq))
    dds.AutoHeight()
    FFT(dds.data)
    i = 0
    while i <len(dds.data):
        try:
            dds.data[i] =(dds.data[i].imag**2+dds.data[i].real ** 2)**0.5
        except AttributeError:
            pass
        #print(dds.data[i])
        i+=1
    dds.AutoHeight()
    dds.draw(display)
    display.show() 
    i =0
    m = [(0,0),(0,0)]
    while i <int(len(dds.data)/2):
        if(dds.data[i]>m[0][1]):
            m[1] = m[0]
            m[0] = (i,dds.data[i])
        elif dds.data[i]>m[1][1]:
            m[1] = (i,dds.data[i])
        i+=1
    print(m[0][0]/128,m[1][0]/128,freq/2/pi)

