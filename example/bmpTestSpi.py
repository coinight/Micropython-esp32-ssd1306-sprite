from machine import Pin,SPI
from sh1106 import SH1106_SPI
from sprite import BinloaderFile,bmpdecode
import time
spi = SPI(1,sck = Pin(5),mosi = Pin(11),baudrate=200000000)
display = SH1106_SPI(128,64,spi,Pin(6),res=Pin(7),cs = Pin(10),rotate=180)
#一次解码后，后续直接打开2233_2.bin就行.
def test():
    t0 = time.ticks_us()
    p = bmpdecode('2233_2.bmp',limit=180,log=False,InvertColor=False)# 0.70
    print((time.ticks_us()-t0)/1000000)
    for i in range(p.h - display.h):
        p.cropDrawXY(0,0,0,p.w,i,i+64,display)
        display.show()
test()
# p.draw(display)
# print(p.w,p.h)
# 解码后上面不需要了
# p = BinloaderFile('2233_2.bin')
# p.draw(display)
# display.show()
# p.cropDrawXY(0,0,0,p.w,100,164,display)
# display.show()
# 0.658432
# 0.669671


