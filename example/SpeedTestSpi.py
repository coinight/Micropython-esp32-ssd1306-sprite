from machine import Pin,SPI
from sh1106 import SH1106_SPI
from sprite import BinloaderMem,BinloaderFile
import time
spi = SPI(1,sck = Pin(5),mosi = Pin(11),baudrate=200000000)
display = SH1106_SPI(128,64,spi,Pin(6),res=Pin(7),cs = Pin(10),rotate=180)
pic = BinloaderMem('big240.bin')
picFile = BinloaderFile('big240.bin')
print(picFile.w,picFile.h)
t0 = time.ticks_ms()
display.fill(1)
display.show()
display.fill(0)
display.show()
print('idel fps:',2/(time.ticks_ms() - t0)*1000)


t0 = time.ticks_ms()
pic.draw(display)
display.show()
pic.draw(display)
display.show()
print('Mem pic show fps:',2/(time.ticks_ms() - t0)*1000)


# print(len(display.buffer))
t0 = time.ticks_ms()
i = 0
while i<100:
    display.fill(0)
    pic.cropDrawX(50,0,0+i,128+i,display)
    display.show()
    i+=1
print('Mem cropX full fps:',100/(time.ticks_ms() - t0)*1000)


t0 = time.ticks_ms()
i = 0
while i<100:
    display.fill(0)
    pic.cropDrawXY(0,32,0+i,128+i,0+i,32+i,display)
    display.show()
    i+=1
print('Mem cropXY half fps:',100/(time.ticks_ms() - t0)*1000)


t0 = time.ticks_ms()
i = 0
while i<112:
    display.fill(0)
    pic.cropDrawXY(i,i%8,100,116,0,15,display)
    display.show()
    i+=1
print('Mem cropXY&Move Size16*16 fps:',112/(time.ticks_ms() - t0)*1000)

#######################################


t0 = time.ticks_ms()
pic.draw(display)
display.show()
pic.draw(display)
display.show()
print('File pic show fps:',2/(time.ticks_ms() - t0)*1000)


# print(len(display.buffer))
t0 = time.ticks_ms()
i = 0
while i<100:
    display.fill(0)
    pic.cropDrawX(50,0,0+i,128+i,display)
    display.show()
    i+=1
print('File cropX full fps:',100/(time.ticks_ms() - t0)*1000)


t0 = time.ticks_ms()
i = 0
while i<100:
    display.fill(0)
    pic.cropDrawXY(0,32,0+i,128+i,0+i,32+i,display)
    display.show()
    i+=1
print('File cropXY half fps:',100/(time.ticks_ms() - t0)*1000)


t0 = time.ticks_ms()
i = 0
while i<112:
    display.fill(0)
    pic.cropDrawXY(i,i%8,100,116,0,15,display)
    display.show()
    i+=1
print('File cropXY&Move Size16*16 fps:',112/(time.ticks_ms() - t0)*1000)

t0 = time.ticks_ms()
i = 0
while i<100:
    picFile.cropDrawXY(0,0,0+i,128+i,0,64,display,True)
    display.show()
    i+=1
print('File cropXY half with transform fps:',100/(time.ticks_ms() - t0)*1000)

