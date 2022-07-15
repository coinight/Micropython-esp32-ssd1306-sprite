from machine import Pin,I2C
from sh1106 import SH1106_I2C
from sprite import TextFullUI
import time,random
i2c = I2C(0,scl = Pin(3),sda = Pin(2),freq=1100000)
display = SH1106_I2C(128,64,i2c,rotate=180)
l = ['hello1','hello2','hello3','hello4','Center','NoCenter','hello8']
t = TextFullUI(0,0)
for i in range(100):
    display.fill(0)
    temp = random.choice(l)
    if(temp != 'Center'):
        temp2 = random.randint(0,1)
    else:
        temp2 = True
    t.AddLine(temp,temp2)
    t.draw(display)
    display.show()
    time.sleep_ms(50)