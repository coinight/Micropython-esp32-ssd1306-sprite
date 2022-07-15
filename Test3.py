from machine import Pin,SPI
from sh1106 import SH1106_SPI
from sprite import BinloaderFile,DataDisplayScreen
import time,math
spi = SPI(1,sck = Pin(5),mosi = Pin(11),baudrate=200000000)
display = SH1106_SPI(128,64,spi,Pin(6),res=Pin(7),cs = Pin(10),rotate=180)


DDS = DataDisplayScreen(delta = 3,height= 1)
#height= x
# max = 32/x min = -31/x
for i in range(300):
    display.fill(0)
    temp=(i%20)*math.sin(2*math.pi*i/10)
    display.text(str(int(temp)),0,0,1)
    DDS+temp
    DDS.draw(display)
    display.show()