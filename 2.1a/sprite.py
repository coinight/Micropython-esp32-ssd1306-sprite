# author：爱玩游戏的陆千辰
# https://space.bilibili.com/87690728
# describe：屏幕精灵控制
#v0.2b
from sys import maxsize
import framebuf
import math

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

class __fframe:
    def draw(self, display, has_transform: bool = False):
        try:
            w = display.width
        except AttributeError:
            w = display.w
        deltaY = getPageLen(self.h)
        
        try:
            posx = clamp(self.x,0,display.width - self.w)
            posy = clamp(self.y,0,deltaY)
        except AttributeError:
            posx = clamp(self.x,0,display.w - self.w)
            posy = clamp(self.y,0,deltaY)
        start = posx + 128 * posy
        i = 0
        drawW = min(self.w,w)
        drawH = min(deltaY,display.pages)
        # maxSize = len(display.buffer)
        temp = start
        if has_transform:
            while i<drawH:
                j = 0
                while j < drawW:
                    display.buffer[temp+j] |= self.data[i * self.w + j]
                    j+=1
                i+=1
                temp += 128
            return
        else:
            while i<drawH:
                display.buffer[temp:temp+drawW] = self.data[i * self.w:i * self.w + drawW]
                i+=1
                temp += 128
            return
    def setxy(self, x=None, y=None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y
    def cropDrawX(self,posx,posy,fromx,tox,display):
        try:
            w,h = display.width,display.height
        except AttributeError:
            w,h = display.w,display.h
        if tox > self.w:
            tox = self.w
        temp = getPageLen(h)
        maxH = getPageLen(self.h)
        if maxH>temp:
            maxH = temp
        ax = clamp(posx,0,w - (tox - fromx))
        ay = clamp(getPageLen(posy),0,temp - maxH)
        start = ax + 128 * ay
        drawW = min(tox-fromx,w)
        if drawW > w:
            drawW = w
        i = 0
        temp = fromx 
        while i<maxH:
            display.buffer[start:start+drawW] = self.data[temp:temp + drawW]
            i+=1
            start += 128
            temp += self.w
    def cropDrawXY(self,posx,posy,fromx,tox,fromy,toy,display,has_transform: bool = False):
        try:
            w,h = display.width,display.height
        except AttributeError:
            w,h = display.w,display.h
        deltaY = getPageLen(toy - fromy)
        deltaX = tox - fromx
        temp = getPageLen(h)
        deltaY = min(temp,deltaY)
        deltaX = min(w,deltaX)
        posx = clamp(posx,0,w - deltaX)
        posy = clamp(posy,0,temp - deltaY)
        start = posx + 128 * posy
        i = 0
        di = getPageLen(fromy)
        temp = start
        temp2 = di * self.w + fromx
        # maxData = len(display.buffer)
        if has_transform:
            while i<deltaY:
                if temp2 + deltaX> len(self.data):
                    return
                j = 0
                while j<deltaX:
                    display.buffer[temp+j] |= self.data[temp2+ j]
                    j+=1
                i+=1
                temp += 128
                temp2 += self.w
            return
        else:
            while i<deltaY:
                if temp2 + deltaX> len(self.data):
                    return
                display.buffer[temp:temp+deltaX] = self.data[temp2:temp2+ deltaX]
                i+=1
                temp += 128
                temp2 += self.w
            return
class framebufPic(__fframe):
    def __init__(self, display):
        try:
            self.w = display.width
            self.h = display.height
        except AttributeError:
            self.w = display.w
            self.h = display.h
        self.buffer = bytearray(display.pages * self.w)
        self.data = framebuf.FrameBuffer1(self.buffer, self.w, self.h)
        self.x, self.y = 0, 0


class BinloaderMem(__fframe):
    def __init__(self, filename, x = 0, y= 0):
        self.x, self.y = x, y
        f = open(filename, "rb")
        temp = f.read(6)
        self.w = temp[2] + (temp[3] << 8)
        self.h = temp[4]
        self.data = f.read()
        f.close()
class BinloaderFile(__fframe):
    def __init__(self, filename, x =0, y =0):
        self.x, self.y = x, y
        self.f = open(filename, "rb")
        temp = self.f.read(6)
        self.w = temp[2] + (temp[3] << 8)
        self.h = temp[4]
    def draw(self, display, has_transform: bool = False):
        try:
            w = display.width
        except AttributeError:
            w = display.w
        deltaY = getPageLen(self.h)
        
        try:
            posx = clamp(self.x,0,display.width - self.w)
            posy = clamp(self.y,0,deltaY)
        except AttributeError:
            posx = clamp(self.x,0,display.w - self.w)
            posy = clamp(self.y,0,deltaY)
        start = posx + 128 * posy
        i = 0
        drawW = min(self.w,w)
        drawH = min(deltaY,display.pages)
        # maxSize = len(display.buffer)
        temp = start
        if has_transform:
            while i<drawH:
                j = 0
                self.f.seek(i * self.w+6)
                while j < drawW:
                    display.buffer[temp+j] |= int.from_bytes(self.f.read(1),'big')
                    j+=1
                i+=1
                temp += 128
            return
        else:
            while i<drawH:
                self.f.seek(i * self.w+6)
                display.buffer[temp:temp+drawW] = self.f.read(drawW)
                i+=1
                temp += 128
            return
    def cropDrawX(self,posx,posy,fromx,tox,display):
        try:
            w,h = display.width,display.height
        except AttributeError:
            w,h = display.w,display.h
        if tox > self.w:
            tox = self.w
        temp = getPageLen(h)
        maxH = getPageLen(self.h)
        if maxH>temp:
            maxH = temp
        ax = clamp(posx,0,w - (tox - fromx))
        ay = clamp(getPageLen(posy),0,temp - maxH)
        start = ax + 128 * ay
        drawW = min(tox-fromx,w)
        if drawW > w:
            drawW = w
        i = 0
        temp = fromx 
        while i<maxH:
            self.f.seek(temp+6)
            display.buffer[start:start+drawW] = self.f.read(drawW)# self.data[temp:temp + drawW]
            i+=1
            start += 128
            temp += self.w
    def cropDrawXY(self,posx,posy,fromx,tox,fromy,toy,display,has_transform: bool = False):
        try:
            w,h = display.width,display.height
        except AttributeError:
            w,h = display.w,display.h
        deltaY = getPageLen(toy - fromy)
        deltaX = tox - fromx
        temp = getPageLen(h)
        deltaY = min(temp,deltaY)
        deltaX = min(w,deltaX)
        posx = clamp(posx,0,w - deltaX)
        posy = clamp(posy,0,temp - deltaY)
        start = posx + 128 * posy
        i = 0
        di = getPageLen(fromy)
        temp = start
        temp2 = di * self.w + fromx
        # maxData = len(display.buffer)
        if has_transform:
            while i<deltaY:
                self.f.seek(temp2+6)
                j = 0
                while j<deltaX:
                    display.buffer[temp+j] |= int.from_bytes(self.f.read(1),'big')
                    j+=1
                i+=1
                temp += 128
                temp2 += self.w
            return
        else:
            while i<deltaY:
                self.f.seek(temp2+6)
                display.buffer[temp:temp+deltaX] = self.f.read(deltaX)
                i+=1
                temp += 128
                temp2 += self.w
            return
    def __del__(self):
        self.f.close()
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
    def __init__(self, x, y,w = 16,h = 6):
        self.w = w
        self.h = h
        self.texts = ['']*self.h
        self.isCenter = [False]*self.h
        self.__pointer = 0
        self.x, self.y = x, y

    def AddLine(self, t: str,isCenter = False):
        i = 0
        while i < len(t):
            if self.__pointer < self.h:
                self.texts[self.__pointer] = t[i:i + self.w]
                self.isCenter[self.__pointer] = isCenter
                self.__pointer += 1
                
            else:
                temp = self.__pointer -1
                del self.texts[0]
                self.texts.append(t[i:i + self.w])
                del self.isCenter[0]
                self.isCenter.append(isCenter)
            i += 16

    def clear(self):
        self.texts = ['']*self.h
        self.__pointer = 0

    def seek(self, p):
        self.__pointer = p
        return self.__pointer
    def tell(self):
        return self.__pointer
    def draw(self, display):
        i = 0
        while i < self.h:
            if(self.isCenter[min(self.h-1,i)]):
                 display.text(self.texts[i], 64-len(self.texts[i])*4, self.y + i * 10, 1) 
            else:
                display.text(self.texts[i], self.x, self.y + i * 10, 1)
            i += 1

class DataDisplayScreen:
    def __init__(self, delta=5, length=128, x=0, y=32,width = 1):
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




