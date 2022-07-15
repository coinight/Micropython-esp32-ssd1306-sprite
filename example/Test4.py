from machine import Pin,SPI
from sh1106 import SH1106_SPI
from sprite import BinloaderFile,TextSelectUI
import time
from button import Button
spi = SPI(1,sck = Pin(5),mosi = Pin(11),baudrate=200000000)
display = SH1106_SPI(128,64,spi,Pin(6),res=Pin(7),cs = Pin(10),rotate=180)

TS1 = TextSelectUI()
TS1.SetText([
    'Clock','Setting','Weather','Game',
    'Every line can be long',
    'FileSystem',
    'balabala Can be long line','Music?'
    ])
TS1.draw(display)
display.show()
def nextIndex(p):
    display.fill(0)
    TS1.NextIndex()
    TS1.draw(display)
    display.show()
def lastIndex(p):
    display.fill(0)
    TS1.LastIndex()
    TS1.draw(display)
    display.show()
Button(4,nextIndex)
Button(8,lastIndex)
