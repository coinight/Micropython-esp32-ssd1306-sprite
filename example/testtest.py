
class TextSelectUI:
    def __init__(self, x=0, y=0,w = 16,h = 6,deltaY = 9):
        self.x, self.y = x, y
        self.selectIndex = 0
        self.text= []
        self.data = []
        self.deltaY = deltaY
        self.selectH = 1
        self.w = w
        self.h = h
        self.start = 0
        self.nowLine = 0
        # self.end = self.start + self.h
    def SetText(self,data):
        self.text = []
        self.data = []
        
        for d in data:
            if(len(d))<self.w:
                self.text.append(d)
                self.data.append(1)
            else:
                i = 0
                CeilLen = 0
                while i <len(d):
                    self.text.append(d[i:i+min(len(d)-i,self.w)])
                    i += self.w
                    CeilLen += 1
                self.data.append(CeilLen)
    def NextIndex(self):
        self.selectIndex += 1
        # 返回
        if(self.selectIndex >= len(self.data)):
            self.selectIndex = 0
            self.start = 0
            self.nowLine = 0
            return
        self.nowLine += self.data[self.selectIndex]
        if(self.nowLine>self.start+self.h):
            self.start = self.nowLine-self.h
        print(self.start,self.nowLine)
    def LastIndex(self):
        self.nowLine -= self.data[self.selectIndex]
        self.selectIndex -= 1
        # 返回
        if(self.selectIndex < 0):
            self.selectIndex = len(self.data) - 1
            self.nowLine = len(self.text) - 1
            self.start = self.nowLine - self.h
            return
        if(self.nowLine<self.start):
            self.start = self.nowLine - self.data[self.selectIndex] + 1
        print(self.start,self.nowLine)
    def draw(self, display):
        loop = 0 # 能画几行
        start = self.start # 行数开始
        while loop <= self.h:
            print(loop+start)
            display.text(self.text[loop+start], self.x, self.y + loop *self.deltaY, 1)
            if(loop+start == self.nowLine):
                display.fill_rect(120, self.y + loop *self.deltaY,8,8,1)
            loop += 1
