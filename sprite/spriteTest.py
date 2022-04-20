from machine import I2C,Pin
import sprite,sh1106
led0 = Pin(13,Pin.OUT,value = 0)
led1 = Pin(12,Pin.OUT,value = 0)
i2c = I2C(0,scl = Pin(18),sda = Pin(19))
display = sh1106.SH1106_I2C(128,64,i2c)
def clear():
    display.fill(0)
    display.show()
clear()
logo = sprite.BinloaderFast("logo.bin",0,0)
def cy(i):
    display.fill(0)
    logo.cropY(i,logo.h)
    logo.cropdraw(display)
    display.show()
def cyD(i):
    display.fill(0)
    logo.cropY(1,i)
    logo.cropdraw(display)
    display.show()
def cx(i):
    display.fill(0)
    logo.cropX(i,logo.w)
    logo.cropdraw(display)
    display.show()
def cxR(i):
    display.fill(0)
    logo.cropX(0,i)
    logo.cropdraw(display)
    display.show()
def testY(speed):
    i = 0
    while i < logo.h:
        cy(i)
        i+=speed
def testY2(speed):
    i = 1
    while i < logo.h+1:
        cyD(i)
        i+=speed
def testX(speed):
    i = 0
    while i < logo.w+ 1:
        cx(i)
        i+=speed
def testX2(speed):
    i = 0
    while i < logo.w+ 1:
        cxR(i)
        i+=speed