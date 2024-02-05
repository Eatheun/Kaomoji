import time
import random
import pyperclip as clpbrd
from kaoCat import *
from tkinter import *
import ttkbootstrap as widg
import numpy as np
from math import *
import win32api as wapi, win32con as wcon

################################ STAGE 3 ################################

# Gets a random Kaomoji from all[category][kaoType] and copies it to the clipboard
def copyKaoClpbrd(category, kaoType):
    # check before
    if not category in all or not kaoType in all[category]: return;
    kaoNum = all[category][kaoType];
    
    # concatenating the giant relative path
    filepath = "./All Kaomojis" + "/" + category + "/" + kaoType + ".txt";
    with open(filepath, "r", encoding = "utf-8") as kaoFile:
        # find and grab the kaomoji
        kaomoji = "";
        for i in range(random.randrange(kaoNum)): kaomoji = kaoFile.readline();
        kaomoji = kaomoji.removesuffix("\n");
        
        # copy to clipboard and print for debugging
        clpbrd.copy(kaomoji);
        print(kaomoji);
        
        # retry if we somehow found a blank
        if kaomoji == "": copyKaoClpbrd(category, kaoType);

################################ STAGE 4 ################################

# CONSTANTS
myFont = "Comic Sans MS Bold"; # title font
padding = 10; # general padding
circOutR = 160; # outer radius of canvas circle
circInR = 50; # inner radius of canvas circle cutout
canvH = circOutR * 2; # height of canvas
canvW = circOutR * 2; # width of canvas
circAngleOffset = 10; # gap between each polygon in the canvas circle
bordWidth = 3; # border width of the canvas
lineWeight = 8; # weight of the polygon outlines
winSize = f'{(canvW + (padding + bordWidth) * 2) * 2}x{canvH * 2}'; # window size
winTrans = 0.3; # base transparency of window
fillCol = "turquoise4"; # fill colour of canvas polygons
outlineCol = "LightSteelBlue1"; # outline colour of canvas polygons
transCol = "#add123"; # transparent colour lol
steps = 5; # general steps to increment

# Helper functions
lastClickX = 0;
lastClickY = 0;
def saveLastClickPos(event):
    global lastClickX, lastClickY;
    lastClickX = event.x;
    lastClickY = event.y;

def dragging(event, window):
	x = event.x - lastClickX + window.winfo_x();
	y = event.y - lastClickY + window.winfo_y();
	window.geometry("+%s+%s" % (x , y));

def fade(isIn, window):
    fadeIncr = (1 - winTrans) / steps;
    start = winTrans if isIn else 1;
    for i in range(steps):
        window.attributes("-alpha", start + (1 if isIn else -1) * (i + 1) * fadeIncr);
        time.sleep(0.02);

# string variables
inCate, inType = "", "";

# widgets and stuff
class KaoApp(Tk):
    def __init__(self):
        super().__init__();
        
        # main info
        self.title("顔ウィール");
        self.geometry(winSize);
        self.minsize(width = 640, height = 640);
        self.iconbitmap("icon.ico");

        # attributes
        # self.overrideredirect(True);
        self.attributes("-alpha", winTrans);
        self.attributes("-topmost", True);
        self.config(bg = transCol);
        # self.wm_attributes("-transparentcolor", transCol);
        
        # centre and draw frames
        self.centreWin();
        self.createSections();
        
        # top
        top = self.topFrame;
        top.closeButton.assignQuit(self);
        top.title.assignDragWin();
        
        # middle
        global inCate, inType;
        inCate = StringVar(value = "");
        inType = StringVar(value = "");
        middle = self.middleFrame;
        
        # bottom
        bottom = self.bottomFrame;
        
        self.mainloop();
    
    def centreWin(self):
        displayXOff = int(self.winfo_screenwidth() / 2 - canvW);
        displayYOff = int(self.winfo_screenheight() / 2 - canvH);
        self.geometry(f'{winSize}+{displayXOff}+{displayYOff}');
    
    def createSections(self):
        self.topFrame = TopSection(self);
        self.middleFrame = MiddleSection(self);
        self.bottomFrame = BottomSection(self);

class Section(Frame):
    def __init__(self, master, bkg = transCol):
        super().__init__(master, background = bkg);
        self.pack(pady = padding);
        
        self.bindHover(master);

    def bindHover(self, window):
        self.bind("<Enter>", lambda event: fade(True, window));
        self.bind("<Leave>", lambda event: fade(False, window));
    
class TopSection(Section):
    def __init__(self, master):
        super().__init__(master);
        
        self.createCloseButton();
        self.createTitle();
    
    def createCloseButton(self):
        self.closeButton = CloseButton(self);
    
    def createTitle(self):
        self.title = Title(self);

class MiddleSection(Section):
    def __init__(self, master):
        super().__init__(master);
        
        self.createSubCircles();
        
    def createSubCircles(self):
        self.cateFrame = SubCircleSection(self, inCate);
        self.typeFrame = SubCircleSection(self, inType);

class BottomSection(Section):
    def __init__(self, master):
        super().__init__(master);

        self.createEnterButton();
        
    def createEnterButton(self):
        self.enterButton = EnterButton(self);
    
class CloseButton(Button):
    def __init__(self, master):
        super().__init__(master, text = "X");
        self.pack(side = "left");

    def assignQuit(self, window):
        self.config(command = lambda: window.quit());

class Title(Label):
    def __init__(self, master, txt = "Select a Kaomoji:", font = (myFont, 18)):
        super().__init__(master, text = txt, font = font);
        self.pack(side = "left");
        
    def assignDragWin(self):
        self.bind('<Button-1>', saveLastClickPos);
        self.bind('<B1-Motion>', dragging);
        
class SubCircleSection(Frame):
    def __init__(self, master, strVar, bkg = transCol):
        super().__init__(master, background = bkg)
        self.pack(side = "left");
        
        # draw the circles and comboboxes
        self.createCircComb(strVar);

    def createCircComb(self, strVar):
        self.circle = Circle(self);
        self.combobox = Combo(self, strVar);

class Circle(Canvas):
    def __init__(self, master, w = canvW + padding * 2, h = canvH + padding * 2, bdw = bordWidth, rlf = "raised"):
        super().__init__(master, width = w, height = h, borderwidth = bdw, relief = rlf);
        self.pack(pady = padding);
    
    # draws the curved edges of each polygon
    def drawCircCurve(self, c, r, a1, a2):
        angleDiff = (a2 - a1) / steps;
        curvePoints = list(map(
            lambda i: (
                (c + r * cos(a1 + i * angleDiff)) + padding,
                circOutR + r * sin(a1 + i * angleDiff) + padding
            ),
            range(steps + 1)
        ));
        self.create_line(
            curvePoints,
            fill = outlineCol,
            smooth = True,
            width = lineWeight,
            tags = ("polygon")
        );

    # draws the straight edges of each polygon
    def drawCircLine(self, c, a1, a2):
        pointPairs = [(circOutR, a1), (circInR, a2)];
        linePoints = list(map(
            lambda point: (
                c + point[0] * cos(point[1]) + padding,
                circOutR + point[0] * sin(point[1]) + padding
            ),
            pointPairs
        ));
        self.create_line(
            linePoints,
            fill = outlineCol,
            width = lineWeight,
            tags = ("polygon")
        );

    
    # draws a bunch of top-truncated triangles in a circle
    def drawCircle(self, pcs, angleOff):
        if pcs == 0: return;
        
        # basic metrics
        c = canvW / 2;
        radii = [circOutR, circInR];
        outOff = radians(min(angleOff, 180 / pcs));
        inOff = atan((radii[1] / radii[0]) * (tan(outOff)));
        
        # loop through angles as cosi + isini
        angles = np.linspace(90, 450, pcs + 1);
        for i in range(pcs):
            curr = radians(angles[i]);
            next = radians(angles[i] + 360 / pcs);
            order = [
                curr + inOff,
                next - inOff,
                next - outOff,
                curr + outOff
            ]; # order of the angles for each point
            
            # out/in curve
            self.drawCircCurve(circOutR, order[0], order[1]);
            self.drawCircCurve(circInR, order[2], order[3]);
            
            # curr/next side lines
            self.drawCircLine(order[1], order[2]);
            self.drawCircLine(order[0], order[3]);
            
        # draw centre self
        offSpace = sqrt(2 * (circInR ** 2) * (1 - cos(radians(2 * angleOff))));
        cCircOff = circInR - offSpace;
        p1, p2 = c - cCircOff + padding, c + cCircOff + padding
        self.create_oval(
            [(p1, p1), (p2, p2)],
            fill = fillCol,
            outline = outlineCol,
            width = lineWeight,
            tags = ("centre")
        );
    
    # clears and draws near circles
    def setDrawCircle(self, pcs, angleOff):
        self.delete("polygon");
        self.drawCircle(pcs, angleOff);

class Combo(widg.Combobox):
    def __init__(self, master, strVar):
        super().__init__(master, textvariable = strVar, font = (myFont, 8), width = 26, state = "readonly");
        self.pack(pady = padding);

    def setTypes(self, types):
        self.config(values = types);
        inType.set("");
    
    # whenever we select a category, we will:
    #   1. set the selectable values for the types combobox
    #   2. redraw the circle for said types combobox
    def bindDrawCircle(self, master): # ????????
        events = [
            lambda event: master.circle.setTypesCombVal(
                list(all[inCate.get()].keys())
            ),
            lambda event: setDrawCircle(
                typeCircle,
                len(typesComB["values"]),
                circAngleOffset
            )
        ];
        for event in events:
            catComB.bind("<<ComboboxSelected>>", event, add = "+");

class EnterButton(Button):
    def __init__(self, master):
        super().__init__(master, text = "Enter");
        self.pack();
    
kaoWin = KaoApp();
