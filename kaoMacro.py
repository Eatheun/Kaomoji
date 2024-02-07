import pyautogui as pag
import time
import random
import pyperclip as clpbrd
from kaoCat import *
from tkinter import *
import numpy as np
from math import *

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

#### CONSTANTS ####

# canvas metrics
outR = int(min(360, pag.size()[1] / 3.5)); # outer radius of canvas circle, limited by screen res
inR = int(min(100, outR / 2)); # inner radius of canvas circle cutout, limited by outR
c = outR; # centre of circle
circAngOff = 5; # gap between each polygon in the canvas circle

# text
myFont = "Comic Sans MS Bold"; # title font
fillCol = "turquoise4"; # fill colour of canvas polygons
outlineCol = "LightSteelBlue1"; # outline colour of canvas polygons
transCol = "#f0f0f0"; # transparent colour lol
baseFontSize = outR / 18;

# tkinter
bordWidth = 3; # border width of the canvas
lineWeight = 6; # weight of the polygon outlines
winTrans = 0.3; # base transparency of window
steps = 5; # general steps to increment

# display port metrics
pad = 10; # general padding
canvH = outR * 2; # height of canvas
canvW = outR * 2; # width of canvas
winW = (canvW + pad * 2) * 2 # width of window
winH = canvH + 136 # width of window
winSize = f'{winW}x{winH}'; # window size

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

# calculates circle coordinates
def calcCircXY(r, a):
    return (
        c + r * cos(a) + pad, # X
        outR + r * sin(a) + pad # Y
    );

# now we make the circles do something, 0 for categories, 1 for types
currFrame = 0;
vals = ["", ""];
currList = list(all.keys());

# selects category/kaoType if warranted
def selectVal(x, y, circle):
    global currFrame, vals, currList;
    auxAng = 180 if x > 0 else 0; # translating angles of any magnitude
    invX = 90 if y < 0 else 270; # factors in invalid X values
    theta = (invX if x == 0 else degrees(atan(y / x))) + 90 + auxAng; # calculates theta of mouse
    index = floor(theta * circle.pcs / 360); # calculates index to the circle's values
    
    # set the values and change the frame
    vals[currFrame] = circle.values[index];
    if currFrame == 0:
        currList = list(all[vals[0]].keys());
    else:
        currList = list(all.keys());
        copyKaoClpbrd(vals[0], vals[1]);
    circle.drawCircle(len(currList), circAngOff, currList);
    currFrame = (currFrame + 1) % 2;

# checks if we clicked on the circle
def interactCircle(event, circle, cCircOff):
    x = event.x - c - pad;
    y = event.y - outR - pad;
    dist = sqrt((x ** 2) + (y ** 2));
    if inR <= dist and dist <= outR:
        selectVal(x, y, circle); # selects the value
    elif 0 <= dist and dist <= cCircOff:
        publicWindow.quit(); # quits if we selected the centre

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
    
    # draw filled polygons
    def drawPolygon(self, angOrd, radOrd):
        polyCorners = list(map(lambda i: calcCircXY(radOrd[i], angOrd[i]), range(4)));
        polyPoints = [];
        for i in range(4):
            polyPoints.append(polyCorners[i]);
            if i % 2 == 0:
                angSteps = int(90 / len(angOrd));
                a0 = angOrd[i]; a1 = angOrd[i + 1];
                step = (a1 - a0) / angSteps;
                polyPoints.append(list(map(lambda j: calcCircXY(radOrd[i], a0 + j * step),range(angSteps))));
        
        # base fill
        self.create_polygon(
			polyPoints,
			fill = fillCol,
			width = lineWeight,
			outline = outlineCol,
			tags = ("polygon")
        );

    # draws a bunch of pie-sliced annuli in a circle
    def drawCircle(self, pcs, angleOff, values):
        if pcs == 0: return;
        self.delete("polygon", "centre"); # clears all the circles before
        
        # offset metrics, making some of them locally accessible
        self.pcs = pcs;
        self.angleOff = angleOff;
        self.values = values;
        inOff = radians(min(angleOff, 180 / pcs));
        outOff = atan((inR / outR) * (tan(inOff)));
        
        # loop through angles as cosi + isini
        angles = np.linspace(90, 450, pcs + 1);
        for i in range(pcs):
            # current and next angle of each polygon
            curr = radians(angles[i]);
            next = curr + radians(360 / pcs);
            
            # order angles and radii for each corresponding point, with offsets
            angOrd = [curr + outOff, next - outOff, next - inOff, curr + inOff];
            radOrd = [outR, outR, inR, inR];
            
            # draw fill first
            self.drawPolygon(angOrd, radOrd);

            # # overlaying current value as text
            midRad = (outR + inR) / 2;
            midAng = (curr + next) / 2;
            tag = values[i].replace(" ", "\n");
            self.create_text(
                calcCircXY(midRad, midAng),
                anchor = CENTER,
                font = (myFont, floor((4 / pcs) * baseFontSize)),
                fill = outlineCol,
                text = tag,
                tags = ("polygon")
            );

        # draw centre
        offSpace = sqrt(2 * (inR ** 2) * (1 - cos(radians(2 * angleOff))));
        cCircOff = inR - offSpace;
        p1, p2 = c - cCircOff + pad, c + cCircOff + pad;
        self.create_oval(
            [(p1, p1), (p2, p2)],
            fill = fillCol,
            outline = outlineCol,
            width = lineWeight,
            tags = ("centre")
        );
        self.create_text(
            [(c + pad, c + pad)],
            anchor = CENTER,
            font = (myFont, 18),
            text = "X",
            fill = outlineCol,
            tags = ("centre")
        );
        
        # binds the circle selecting to the circle
        self.bind("<Button>", lambda event: interactCircle(event, self, cCircOff));

kaoWin = KaoApp();
