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

for i in range(150):
    dds+round(10*math.sin(i/4))
dds.draw(display)
display.show()

def DataScale(data,scale):
    re = []
    inv = False
    if scale == 0:
        return re
    if scale < 0:
        scale = - scale
        inv = True
    scale = len(data)/(scale*len(data))
    i = 0
    while  math.ceil(i) < len(data):
        re.append(data[math.ceil(i)])
        i += scale
    if inv:
        re.reverse()
    return re
        
def test(i):
    global dds,display,d
    display.fill(0)
    dds.data = DataScale(d,i)
    dds.draw(display)
    display.show()

d = dds.data
for i in range(100):
    test(math.sin(i/10))