import time
from random import randrange as rndg
from tkinter import *
from math import *

winW = 800;
winH = 640;
sW = winW >> 1;
sH = winH >> 1;

class Slider(Label):
    def __init__(self, master):
        global sW, sH;
        super().__init__(master, width = sW, height = sH, text = "Hellooooo!!!");
        self.sX = sW;
        self.sY = sH;
        self.position();

    def bounce(self):
        if self.sY > 240:
            self.sY -= 3;
            self.position();
            wind.after(1, self.bounce);
        else:
            wind.after(1, self.recoil);

    def recoil(self):
        if self.sY < sH:
            self.sY += 3;
            self.position();
            wind.after(1, self.recoil);

    def position(self):
        self.place(anchor = "center", x = self.sX, y = self.sY);

class Bubbs(Canvas):
    def __init__(self, master):
        super().__init__(master, width = int(sW * 2), height = int(sH * 2));
        self.place(anchor = "center", x = sW, y = sH);
        self.bSize = 0;

    def sBubbWrap(self, x, y):
        self.x = x;
        self.y = y;
        self.bSize = 0;
        self.spawnBubb();

    def spawnBubb(self):
        if self.bSize < 80:
            self.create_oval([(self.x, self.y), (self.bSize + self.x, self.bSize + self.y)], fill = "red");
            self.bSize += 3;
            wind.after(5, self.spawnBubb);

wind = Tk();
wind.geometry(f'{winW}x{winH}');

bubbCanv = Bubbs(wind);
bubbCanv.bind("<Button>", lambda event: bubbCanv.sBubbWrap(rndg(winW), rndg(winH)));

# slidey = Slider(wind);
# slidey.bind("<Button>", lambda event: slidey.bounce());

wind.mainloop();
