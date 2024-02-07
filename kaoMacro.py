import time
from tkinter import *
import numpy as np
from math import *
from build.constants.constants import *
from build.helpers.circle import *
from build.setup.kaoCat import *

################################ STAGE 3 ################################

# Gets a random Kaomoji from all[category][kaoType] and copies it to the clipboard
def copyKaoClpbrd(category, kaoType):
    # check before
    if not category in all or not kaoType in all[category]: return;
    kaoNum = all[category][kaoType];
    
    # concatenating the giant relative path
    filepath = "./All Kaomojis" + "/" + category + "/" + kaoType + ".txt";
    with open(filepath, "r", encoding = "utf-8") as kaoFile:
        # find the Kaomoji, copy to clipboard, print for debugging
        kaomoji = "";
        for i in range(random.randrange(kaoNum)): kaomoji = kaoFile.readline();
        kaomoji = kaomoji.removesuffix("\n");
        clpbrd.copy(kaomoji);
        print(kaomoji);
        
        # retry if we somehow found a blank
        if kaomoji == "": copyKaoClpbrd(category, kaoType);

################################ STAGE 4 ################################

#### GLOBAL VARIABLES ####

lastClickX = 0;
lastClickY = 0;
publicWindow = ""; # gets assigned when a new KaoApp() is instanced

# Helper functions
def saveLastClickPos(event):
    global lastClickX, lastClickY;
    lastClickX = event.x;
    lastClickY = event.y;

def dragging(event):
	x = event.x - lastClickX + publicWindow.winfo_x();
	y = event.y - lastClickY + publicWindow.winfo_y();
	publicWindow.geometry("+%s+%s" % (x , y));

# fades window in/out
def fade(isIn):
    fadeIncr = (1 - winTrans) / steps;
    start = winTrans if isIn else 1;
    for i in range(steps):
        publicWindow.attributes("-alpha", start + (1 if isIn else -1) * (i + 1) * fadeIncr);
        time.sleep(0.02);

# binds window hovering to the section
def bindHover(widget):
    widget.bind("<Enter>", lambda event: fade(True));
    widget.bind("<Leave>", lambda event: fade(False));

################################ MAIN WINDOW ################################

# widgets and stuff
class KaoApp(Tk):
    def __init__(self):
        super().__init__();
        self.config(bg = transCol);

        global publicWindow;
        publicWindow = self;
        
        # collective info
        self.drawWinInfo();
        self.assignWinAttr();
        self.centreWin();
        
        # main body instance
        self.body = Section(self);
        body = self.body;
        bindHover(body);
        
        self.mainloop();
    
    # main info
    def drawWinInfo(self):
        self.geometry(winSize);
        self.iconbitmap("icon.ico");
    
    # assigns window attributes
    def assignWinAttr(self):
        self.overrideredirect(True);
        self.attributes("-alpha", winTrans);
        self.attributes("-topmost", True);
        self.attributes("-transparentcolor", transCol);
        
    # centres window on the screen
    def centreWin(self):
        displayXOff = int((self.winfo_screenwidth() - winW) / 2);
        displayYOff = int((self.winfo_screenheight() - winH) / 2);
        self.geometry(f'{winSize}+{displayXOff}+{displayYOff}');

class Section(Frame):
    def __init__(self, master):
        super().__init__(master);
        self.pack(pady = pad);
        
        self.dragButton = DragButton(self);
        
        self.circle = Circle(self);
        allCate = list(all.keys());
        self.circle.drawCircle(len(allCate), circAngOff, allCate);

class DragButton(Button):
    def __init__(self, master):
        super().__init__(master, font = (myFont, 12), text = "+", fg = outlineCol, bg = fillCol, activebackground = "#ffffff");
        self.pack();
        
        # assigns dragging to the window
        self.bind('<Button-1>', saveLastClickPos);
        self.bind('<B1-Motion>', dragging);

class Circle(Canvas):
    def __init__(self, master, w = canvW + pad * 2, h = canvH + pad * 2):
        super().__init__(master, width = w, height = h);
        self.pack(pady = pad);

    # draws a bunch of pie-sliced annuli in a circle
    def drawCircle(self, pcs, angleOff, values):
        if pcs == 0: return;
        self.delete("polygon", "centre"); # clears all the circles before
        
        # make input args locally accessible
        self.pcs = pcs;
        self.angleOff = angleOff;
        self.values = values;
        
        # draw!
        drawPolygons(self, values);
        drawCentre(self, publicWindow);

kaoWin = KaoApp();
