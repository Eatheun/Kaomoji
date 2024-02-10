from random import randrange
import time
from customtkinter import *
from math import *

winW = 640;
winH = 480;
cvSc = 1.5
pad = 10;
buttSize = 50;
bubbles = [];
bubbCounter = 0;
        
class Bubbles(CTkCanvas):
    def __init__(self, master):
        super().__init__(master, width = int(winW * cvSc), height = int(winH * cvSc));
        self.place(x = 0, y = 0);
    
    def spawnBubb(self):
        self.oX = randrange(int(winW * cvSc));
        self.oY = randrange(int(winH * cvSc));
        self.bSz = 0;
        self.bubbInst();
        
    def bubbInst(self):
        mxSz = 50;
        if self.bSz > mxSz: return;
        off = (mxSz - self.bSz) >> 1;
        ofX = off + self.oX;
        ofY = off + self.oY;
        
        colour = "#";
        for i in range(3): colour += str(hex(randrange(0xef) + 0x10)).removeprefix("0x");
        
        self.create_oval(
            [
                (ofX, ofY),
                (self.bSz + ofX, self.bSz + ofY)
            ],
            fill = colour,
            width = 0,
            tags = (" ")
        );
        self.bSz += 4;
        newWin.after(5, self.bubbInst);

newWin = CTk();
newWin.minsize(width = winW, height = winH);
newWin.config(bg = "#f0f0f0");
# newWin.resizable(False, False);

bubbleCanv = Bubbles(newWin);

button = CTkButton(newWin, width = buttSize, height = buttSize, text = "Press\nme!", command = lambda: bubbleCanv.spawnBubb());
button.place(anchor = CENTER, x = winW / 2, y = winH / 2);

newWin.mainloop();
