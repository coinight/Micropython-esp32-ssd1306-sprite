from machine import I2C,Pin
import math
import sprite,sh1106,random,time
import _thread as thread
import micropython
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

def ddsThread(name,dds,display):
    global GlobalThreads
    lock.acquire()
    GlobalThreads[name] = True
    lock.release()
    i = 0
    while GlobalThreads[name]:
        #dds.height = math.sin(i/10)*3
        display.fill(0)
        #data= random.randint(-32,32)
        data = 10*math.sin(i/4)
        lock.acquire()
        dds+data
        dds.draw(display)
        display.show()
        lock.release()
        time.sleep_ms(20)
        i += 1
    del GlobalThreads[name]
if __name__ == "__main__":
    lock = thread.allocate_lock()
    GlobalThreads = {}
    dds = sprite.DataDisplayScreen(delta=1,length = 128)
    #dds+5+13+19+0+(-5)+7
    #dds.draw(display)
    display.show()
    thread.start_new_thread(ddsThread,("dds",dds,display))
