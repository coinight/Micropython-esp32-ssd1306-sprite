from machine import Pin,Timer
from time import ticks_ms,sleep_ms
#024
class Button:
    tim = Timer(2)
    def __init__(self,pin,irq = None,trigger=Pin.IRQ_FALLING,dt = 15):
        self.pin = Pin(pin,Pin.IN,pull = Pin.PULL_UP)
        self.pin.irq(self.call_back, trigger=Pin.IRQ_FALLING)
        if irq:
            self.irq = irq
        else:
            self.irq = lambda p:print(p.value())
#         self.value = 0
        self.lastClickTime = 0
        self.dt = dt
    def fixcall_back(self,tim):
        if(not self.pin.value()):
            self.irq(self.pin)
    def call_back(self,Pin):
        if(ticks_ms() - self.lastClickTime > self.dt ):
            Button.tim.init(period=20, mode=Timer.ONE_SHOT, callback=self.fixcall_back)
#             self.value = 1
        self.lastClickTime = ticks_ms()
    
# b = Button(8)
