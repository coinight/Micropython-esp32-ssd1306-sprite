# author：爱玩游戏的陆千辰
# https://space.bilibili.com/87690728
# describe：屏幕精灵控制，Binloader，水平扫描读取bin。
#                       BinloaderFast，直接缓存帧赋值，数据水平，字节垂直，数据反序bin。
#                       framebufPic，帧缓存
#v0.2a 
from sys import maxsize
import framebuf


def getbin(inta: int, x: int) -> int:
    if x > 0:
        return (inta >> x) - (inta >> (x + 1)) * 2
    elif x == 0:
        return inta - (inta >> 1) * 2

def clamp(a,min,max):
    if max < min:
        return min
    if a<min:
        return min
    elif a>max:
        return max
    else:
        return a
def getPageLen(num: int) -> int:
    if (num == (num >> 3) << 3):
        return int(num >> 3)
    else:
        return int(num >> 3) + 1


class BinloaderFromFile:
    def __init__(self, filename, x, y):
        self.f = open(filename, "rb")
        temp = self.f.read(6)
        self.w = temp[2] + (temp[3] << 8)
        self.h = temp[4]
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
                if (
                        self.x + dx <= display.width and self.y + dy <= display.height and self.x + dx >= 0 and self.y + dy >= 0):
                    display.pixel(self.x + dx, self.y + dy, getbin(int.from_bytes(temp, "big"), 7 - i))
                dx += 1
                pixCounter += 1
                if pixCounter >= 8 * getPageLen(self.w):
                    pixCounter = 0
                    dx = 0
                    dy += 1
            temp = self.f.read(1)

    def close(self):
        self.f.close()


class BinloaderFromMem:
    def __init__(self, filename, x, y):
        self.f = open(filename, "rb")
        temp = self.f.read(6)
        self.w = temp[2] + (temp[3] << 8)
        self.h = temp[4]
        self.data = self.f.read()
        self.x, self.y = x, y
        self.f.close()

    def setPos(self, x, y):
        self.x, self.y = x, y

    def draw(self, display):
        dx, dy = 0, 0
        pixCounter = 0
        for d in self.data:
            for i in range(8):
                if (self.x + dx <= display.width and self.y + dy <= display.height and self.x + dx >= 0 and self.y + dy >= 0):
                    display.pixel(self.x + dx, self.y + dy, getbin(d, 7 - i))
                dx += 1
                pixCounter += 1
                if pixCounter >= 8 * getPageLen(self.w):
                    pixCounter = 0
                    dx = 0
                    dy += 1


class fframe:
    def setxy(self, x=None, y=None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y
    def cropDrawX(self,posx,posy,fromx,tox,display):
        if tox > self.w:
            tox = self.w
        temp = getPageLen(display.height)
        maxH = getPageLen(self.h)
        if maxH>temp:
            maxH = temp
        ax = clamp(posx,0,display.width - (tox - fromx))
        ay = clamp(getPageLen(posy),0,temp - maxH)
        start = ax + 128 * ay
        drawW = (tox-fromx)
        if drawW > display.width:
            drawW = display.width
        i = 0
        while i<maxH:
            display.buffer[start + 128 * i:start + 128 * i+drawW] = self.data[i * self.w:i * self.w + drawW]
            i+=1
    def cropDrawXY(self,posx,posy,fromx,tox,fromy,toy,display,has_transform: bool = False):
        deltaY = getPageLen(toy - fromy)
        deltaX = tox - fromx
        temp = getPageLen(display.height)
        if deltaY > temp:
            deltaY = temp
        if deltaX > display.width:
            deltaX = display.width
        posx = clamp(posx,0,display.width - deltaX)
        posy = clamp(posy,0,temp - deltaY)
        start = posx + 128 * posy
        i = 0
        di = getPageLen(fromy)
        maxData = len(display.buffer)
        if has_transform:
            while i<deltaY:
                temp = start + 128 * i
                temp2 = di * self.w + fromx
                if temp2 + deltaX> len(self.data):
                    return
                j = 0
                while j<deltaX:
                    display.buffer[temp+j] = self.data[temp2+ j] | display.buffer[temp+j]
                    j+=1
                
                i+=1
                di+=1
            return
        else:
            while i<deltaY:
                temp = start + 128 * i
                if di * self.w + deltaX + fromx> len(self.data):
                    return
                display.buffer[temp:temp+deltaX] = self.data[di * self.w + fromx:di * self.w + fromx+ deltaX]
                i+=1
                di+=1
            return
class framebufPic(fframe):
    def __init__(self, display):
        self.display = display
        self.width = self.display.width
        self.height = self.display.height
        self.buffer = bytearray(self.display.pages * self.display.width)
        self.data = framebuf.FrameBuffer1(self.buffer, self.display.width, self.display.height)
        self.x, self.y = 0, 0

    def show(self):
        tempbuffer = self.display.buffer
        self.display.buffer = self.buffer
        self.display.show()
        self.display.buffer = tempbuffer

    def draw(self, display, has_transform: bool = False):
        deltaY = getPageLen(self.height)
        posx = clamp(self.x,0,display.width - self.width)
        posy = clamp(self.y,0,deltaY)
        start = posx + 128 * posy
        i = 0
        maxSize = len(display.buffer)
        if has_transform:
            while i<deltaY:
                temp = start + 128 * i
                if(temp+self.width > maxSize):
                    return
                j = 0
                while j < self.width:
                    display.buffer[temp+j] = self.cutdata[i * self.width + j] | display.buffer[temp+j]
                    j+=1
                
                i+=1
            return
        else:
            while i<deltaY:
                temp = start + 128 * i
                if(temp+self.w > maxSize):
                    return
                display.buffer[temp:temp+self.w] = self.cutdata[i * self.w:i * self.w + self.w]
                i+=1
            return


class BinloaderFast(fframe):
    def __init__(self, filename, x, y):
        self.x, self.y = x, y
        f = open(filename, "rb")
        temp = f.read(6)
        self.w = temp[2] + (temp[3] << 8)
        self.h = temp[4]
        self.data = f.read()
        self.cutdata = self.data
        self.cw, self.ch = self.w, self.h
        f.close()

    def draw(self, display, has_transform: bool = False):
        deltaY = getPageLen(self.h)
        posx = clamp(self.x,0,display.width - self.w)
        posy = clamp(self.y,0,deltaY)
        start = posx + 128 * posy
        i = 0
        maxSize = len(display.buffer)
        if has_transform:
            while i<deltaY:
                temp = start + 128 * i
                if(temp+self.w > maxSize):
                    return
                j = 0
                while j < self.w:
                    display.buffer[temp+j] = self.cutdata[i * self.w + j] | display.buffer[temp+j]
                    j+=1
                
                i+=1
            return
        else:
            while i<deltaY:
                temp = start + 128 * i
                if(temp+self.w > maxSize):
                    return
                display.buffer[temp:temp+self.w] = self.cutdata[i * self.w:i * self.w + self.w]
                i+=1
            return


class rhombus8:
    def __init__(self, x: int, y: int, r: int, width: int = None, select: int = None):
        #       *2
        #    *1    *3
        #  *0    C   *4
        #    *7    *5
        #       *6
        # draw_rhombus8_box(display,68,32,20,5,0xf0)  //Old
        self.data = [(x - r, y),
                     (x - (r >> 1), y - (r >> 1)),
                     (x, y - r),
                     (x + (r >> 1), y - (r >> 1)),
                     (x + r, y),
                     (x + (r >> 1), y + (r >> 1)),
                     (x, y + r),
                     (x - (r >> 1), y + (r >> 1)),
                     ]

        self.select = select
        self.r = r
        self.x = x
        self.y = y
        self.t = "        "
        if width is None:
            self.width = self.r >> 1
        else:
            self.width = width

    def setxy(self, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def setText(self, t: str):
        self.t = t

    def setSelect(self, s):
        self.select = s

    def draw(self, display):
        if self.select is None:
            for i in range(8):
                display.rect(self.x + self.data[i][0] - self.width, self.y + self.data[i][1] - self.width,
                             self.width << 1,
                             self.width << 1, 1)
                if self.t[i] != " ":
                    display.text(self.x + self.t[i], self.y + self.data[i][0] - (self.width - 2),
                                 self.data[i][1] - (self.width - 2), 1)
        else:
            for i in range(8):
                if getbin(self.select, i):
                    display.fill_rect(self.x + self.data[i][0] - self.width, self.y + self.data[i][1] - self.width,
                                      self.width << 1,
                                      self.width << 1, 1)
                    if self.t[i] != " ":
                        display.text(self.x + self.t[i], self.y + self.data[i][0] - (self.width - 2),
                                     self.data[i][1] - (self.width - 2),
                                     0)
                else:
                    display.rect(self.x + self.data[i][0] - self.width, self.y + self.data[i][1] - self.width,
                                 self.width << 1,
                                 self.width << 1, 1)
                    if self.t[i] != " ":
                        display.text(self.t[i], self.x + self.data[i][0] - (self.width - 2),
                                     self.y + self.data[i][1] - (self.width - 2),
                                     1)


class TextFullUI:
    def __init__(self, x, y):
        self.w = 16
        self.h = 6
        self.texts = ['', '', '', '', '', '']
        self.pointer = 0
        self.x, self.y = x, y

    def AddLine(self, t: str):
        i = 0
        while i < len(t):
            if self.pointer < self.h:
                self.texts[self.pointer] = t[i:i + 16]
                self.pointer += 1
            else:
                del self.texts[0]
                self.texts.append(t[i:i + 16])
            i += 16

    def clear(self):
        self.texts = ['', '', '', '', '', '']
        self.pointer = 0

    def seek(self, p):
        self.pointer = p
        return self.pointer

    def draw(self, display):
        i = 0
        while i < self.h:
            if self.texts[i] != '':
                display.text(self.texts[i], self.x, self.y + i * 10, 1)
            i += 1

class DataDisplayScreen:
    def __init__(self, delta=5, length=0, x=0, y=32,width = 1):
        self.data = []
        self.len = length
        self.delta = delta if delta > 1 else 1
        self.height = 1
        self.x = x
        self.y = y
        self.width = width
    def __add__(self, other):
        if len(self.data)*self.delta >= self.len > 0:
            self.data.pop(0)
        self.data.append(other)
        return self
    def AutoHeight(self):
        self.height = min(abs((self.y-1)/max(self.data)),abs((63-self.y)/min(self.data)))
    def draw(self, display):
        if len(self.data) <= 1:
            return
        i = 0
        while i < len(self.data) - 1:
            display.line(self.x+ i*self.delta,round(-self.data[i]*self.height)+self.y,
                         self.x+(i+1)*self.delta,round(-self.data[i+1]*self.height)+self.y,
                         self.width)
            i += 1
def DataScale(data,scale):
    re = []
    inv = False
    if scale == 0:
        return re
    if scale < 0:
        scale = - scale
        inv = True
    scale = len(data)/(scale*len(data))
    i = 0
    while  math.ceil(i) < len(data):
        re.append(data[math.ceil(i)])
        i += scale
    if inv:
        re.reverse()
    return re



