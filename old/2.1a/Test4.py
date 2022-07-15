from machine import ADC,Pin
import time
from machine import Pin,I2C
from sh1106 import SH1106_I2C
from sprite import DataDisplayScreen
import time,math
i2c = I2C(0,scl = Pin(19),sda = Pin(18),freq=1100000)
display = SH1106_I2C(128,64,i2c,rotate=180)
adc = ADC(Pin(2),atten = ADC.ATTN_11DB)#0~4095
DDS = DataDisplayScreen(y = 63,delta = 3,height= 0.015625*3)#64/4096
while True:
    display.fill(0)
    temp = adc.read() - 18
    DDS+(temp)
#     print(adc.read())
    DDS.draw(display)
    display.text('%.2f'%(temp/100)+'v',0,0)
    display.show()
# while True:
#     print(adc.read())
#     time.sleep_ms(20)