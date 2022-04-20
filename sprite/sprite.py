# author：爱玩游戏的陆千辰
# https://space.bilibili.com/87690728
# describe：屏幕精灵控制，Binloader，水平扫描读取bin。
#                       BinloaderFast，直接缓存帧赋值，数据水平，字节垂直，数据反序bin。
#                       framebufPic，帧缓存
# add:移动xy有缺陷。
import framebuf


def getbin(inta: int, x: int) -> int:
    if x > 0:
        return (inta >> x) - (inta >> (x + 1)) * 2
    elif x == 0:
        return inta - (inta >> 1) * 2


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
                    # print("")
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
            # print(temp,end='')
            for i in range(8):
                if (
                        self.x + dx <= display.width and self.y + dy <= display.height and self.x + dx >= 0 and self.y + dy >= 0):
                    display.pixel(self.x + dx, self.y + dy, getbin(d, 7 - i))
                # print(self.x+dx, self.y+dy)
                dx += 1
                pixCounter += 1
                if pixCounter >= 8 * getPageLen(self.w):
                    pixCounter = 0
                    dx = 0
                    dy += 1
                    # print("")


class fframe:
    def setxy(self, x=None, y=None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y

    def cropX(self, fromx, tox):
        data = self.data
        self.cutdata = bytearray()
        self.cw = tox - fromx
        if self.cw > self.w - fromx:
            self.cw = self.w - fromx
        for i in range(getPageLen(self.h)):
            self.cutdata += data[fromx + i * self.w:tox + i * self.w]

    def cropY(self, fromy, toy):
        if fromy < 0:
            fromy = 0
        if toy > self.h:
            toy = self.h
        data = self.data
        self.cutdata = bytearray()
        self.ch = toy - fromy
        #print(toy,fromy,self.ch)
        if toy % 8 != 0:
            self.ch += 8-(toy%8)
            #print(self.ch)
        if fromy % 8 != 0:
            self.ch += fromy % 8
        y = getPageLen(fromy) - 1
        if fromy > 0 and fromy % 8 == 0:
            bis = 8
        else:
            bis = fromy % 8
        bis2 = (64-toy) % 8
        #print(fromy,y)
        while y < getPageLen(toy):
            #print(y, getPageLen(self.ch) - getPageLen(toy) + 1)
            for x in range(self.cw):
                #print(x,self.cw,y,x+self.cw*y)
                if self.ch > 8:
                    tempa = True
                    tempb = True
                    if y == getPageLen(fromy) - 1:
                        #print(bis)
                        self.cutdata.append((data[x+self.cw*y] >> bis << bis) & 0xff)
                        tempa = False
                    if y == getPageLen(toy) - 1:
                        #print("bis2",bis2,(data[x + self.cw * y] << bis2 >> bis2) & 0xff)
                        self.cutdata.append((data[x + self.cw * y] << bis2 & 0xff)>> bis2 )
                        tempb = False
                    if tempa and tempb:
                        #print(x + self.cw * y)
                        self.cutdata.append(data[x + self.cw * y])
                else:
                    self.cutdata.append((((data[x + self.cw * y] >> bis << bis) & 0xff)<< bis2 & 0xff) >> bis2)
            y += 1

    def cropdraw(self, display, has_transform: bool = None):
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
            if not has_transform:
                #print(i,":::",(i + 1) * self.cw)
                display.buffer[start + 128 * i:start + 128 * i + self.cw] = self.cutdata[i * self.cw:(i + 1) * self.cw]
            else:
                j = int(0)
                while j < self.cw:
                    display.buffer[start + 128 * i + j] = (display.buffer[start + 128 * i + j]) | (
                        self.cutdata[i * self.cw + j])
                    j += 1


class framebufPic(fframe):
    def __init__(self, display):
        self.display = display
        self.cutdata = None
        self.w = self.display.width
        self.h = self.display.height
        self.buffer = bytearray(self.display.pages * self.display.width)
        self.data = framebuf.FrameBuffer1(self.buffer, self.display.width, self.display.height)
        self.cw, self.ch = self.w, self.h
        self.x, self.y = 0, 0

    def show(self):
        tempbuffer = self.display.buffer
        self.display.buffer = self.buffer
        self.display.show()
        self.display.buffer = tempbuffer

    def draw(self, frame):
        # frame must be a display or frame //by kilo
        i = 0
        while i < len(frame.buffer):
            if (self.buffer[i] != 0):
                frame.buffer[i] = (frame.buffer[i]) | (self.buffer[i])
            i += 1


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

    def draw(self, display, has_transform: bool = None):
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
            if has_transform:
                j = int(0)
                while j < self.w:
                    display.buffer[start + 128 * i + j] = (display.buffer[start + 128 * i + j]) | (
                        self.data[i * self.w + j])
                    j += 1
            else:
                display.buffer[start + 128 * i:start + 128 * i + self.w] = self.data[i * self.w:(i + 1) * self.w]


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