from machine import Pin,I2C
from sh1106 import SH1106_I2C
from sprite import DataDisplayScreen
import time,math
i2c = I2C(0,scl = Pin(19),sda = Pin(18),freq=1100000)
display = SH1106_I2C(128,64,i2c,rotate=180)


DDS = DataDisplayScreen(delta = 3,height= 1)
#height= x
# max = 32/x min = -31/x
for i in range(300):
    display.fill(0)
    DDS+(i%20)*math.sin(2*math.pi*i/10)
    DDS.draw(display)
    display.show()