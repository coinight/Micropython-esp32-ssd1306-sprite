from machine import Pin,SPI
from sh1106 import SH1106_SPI
from sprite import BinloaderFile,TextFullUI
import time,random
spi = SPI(1,sck = Pin(5),mosi = Pin(11),baudrate=200000000)
display = SH1106_SPI(128,64,spi,Pin(6),res=Pin(7),cs = Pin(10),rotate=180)
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