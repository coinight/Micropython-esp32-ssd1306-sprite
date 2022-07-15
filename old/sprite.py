# author：爱玩游戏的陆千辰
# https://space.bilibili.com/87690728
# describe：屏幕精灵控制，Binloader，水平扫描读取bin。
#                       BinloaderFast，直接缓存帧赋值，数据水平，字节垂直，数据反序bin。
#                       framebufPic，帧缓存
# add:移动xy有缺陷。
import framebuf

@micropython.viper
def getbin(inta: int, x: int) -> int:
    if x > 0:
        return (inta >> x) - (inta >> (x + 1)) * 2
    elif x == 0:
        return inta - (inta >> 1) * 2


def getPageLen(num: int) -> int:
    if (num % 8) == 0:
        return int(num / 8)
    else:
        return int(num / 8) + 1


def initDisplay(scl, sda, hardware=None):
    # hardware指定硬件i2c，不指定则软件
    import ssd1306
    if hardware == None:
        from machine import Pin, SoftI2C
        i2c = SoftI2C(scl=Pin(scl), sda=Pin(sda), freq=160000000)
    else:
        from machine import Pin, I2C
        i2c = I2C(hardware, scl=Pin(scl), sda=Pin(sda), freq=800000)
    display = ssd1306.SSD1306_HardI2C(128, 64, i2c)
    return display


class BinloaderFromFile:
    def __init__(self, filename, x, y):
        self.f = open(filename, "rb")
        temp = self.f.read(6)
        self.w = temp[2]+(temp[3]<<8)
        self.h = temp[4]+(temp[5]<<8)
        self.dataP = 6
        self.x, self.y = x, y

    def setPos(self, x, y):
        self.x, self.y = x, y

    def draw(self, display):
        dx, dy = 0, 0
        pixCounter = 0
        self.f.seek(self.dataP)
        temp = self.f.read(1)
        while (temp != b""):
            for i in range(8):
                if(self.x+dx<=display.width and self.y+dy<=display.height and self.x+dx>=0 and self.y+dy>=0):
                    display.pixel(self.x + dx, self.y + dy, getbin(int.from_bytes(temp, "big"), 7 - i))
                dx += 1
                pixCounter += 1
                if pixCounter >= 8 * getPageLen(self.w):
                    pixCounter = 0
                    dx = 0
                    dy += 1
                    # print("")
            temp = self.f.read(1)

    def close(self):
        self.f.close()


class BinloaderFromMem:
    def __init__(self, filename, x, y):
        self.f = open(filename, "rb")
        temp = self.f.read(6)
        self.w = temp[2]+(temp[3]<<8)
        self.h = temp[4]+(temp[5]<<8)
        self.data = self.f.read()
        self.x, self.y = x, y
        self.f.close()

    def setPos(self, x, y):
        self.x, self.y = x, y

    def draw(self, display):
        dx, dy = 0, 0
        pixCounter = 0
        for d in self.data:
            # print(temp,end='')
            for i in range(8):
                if(self.x+dx<=display.width and self.y+dy<=display.height and self.x+dx>=0 and self.y+dy>=0):
                    display.pixel(self.x + dx, self.y + dy, getbin(d, 7 - i))
                # print(self.x+dx, self.y+dy)
                dx += 1
                pixCounter += 1
                if pixCounter >= 8 * getPageLen(self.w):
                    pixCounter = 0
                    dx = 0
                    dy += 1
                    # print("")


class framebufPic:
    def __init__(self, display):
        self.display = display
        self.buffer = bytearray(self.display.pages * self.display.width)
        self.framebuf = framebuf.FrameBuffer1(self.buffer, self.display.width, self.display.height)

    def show(self):
        tempbuffer = self.display.buffer
        self.display.buffer = self.buffer
        self.display.show()
        self.display.buffer = tempbuffer


class BinloaderFast:
    def __init__(self, filename, x, y):
        self.x, self.y = x, y
        f = open(filename, "rb")
        temp = f.read(6)
        self.w = temp[2]+(temp[3]<<8)
        self.h = temp[4]
        self.data = f.read()
        self.cutdata=None
        self.cw,self.ch=self.w,self.h
        f.close()

    def setxy(self, x=None, y=None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y

    def cropX(self, fromx,tox):
        self.cutdata =bytearray()
        self.cw = tox-fromx
        if self.cw > self.w-fromx:
            self.cw = self.w-fromx
        for i in range(getPageLen(self.h)):
            self.cutdata += self.data[fromx+i*self.w:tox+i*self.w]
    def cropY(self,fromy,toy):
        pass
    #没写完
    def cropdraw(self,display):
        if self.x <= 0:
            ax = 0
        elif self.x + self.cw > display.width:
            ax = display.width - self.cw
        else:
            ax = self.x
        if self.y <= 0:
            ay = 0
        elif self.y + self.ch > display.height:
            ay = getPageLen(display.height) - getPageLen(self.ch)
        else:
            ay = self.y
        start = ax + 128 * ay
        for i in range(getPageLen(self.ch)):
            display.buffer[start + 128 * i:start + 128 * i + self.cw] = self.cutdata[i * self.cw:(i + 1) * self.cw]
    def draw(self, display):
        if self.x <= 0:
            ax = 0
        elif self.x + self.w > display.width:
            ax = display.width - self.w
        else:
            ax = self.x
        if self.y <= 0:
            ay = 0
        elif self.y + self.h > getPageLen(self.h):
            ay = getPageLen(display.height) - getPageLen(self.h)
        else:
            ay = self.y
        start = ax + 128 * ay
        for i in range(getPageLen(self.h)):
            display.buffer[start + 128 * i:start + 128 * i + self.w] = self.data[i * self.w:(i + 1) * self.w]




