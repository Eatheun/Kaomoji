from textwrap import fill
import pyautogui as pag
import time
import random
import pyperclip as clpbrd
from pyscreeze import center
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
outR = int(min(320, pag.size()[1] / 4.5)); # outer radius of canvas circle, limited by screen res
inR = int(min(80, outR / 2)); # inner radius of canvas circle cutout, limited by outR
c = outR; # centre of circle
circAngOff = 5; # gap between each polygon in the canvas circle

# text
myFont = "Comic Sans MS Bold"; # title font
fillCol = "turquoise4"; # fill colour of canvas polygons
outlineCol = "LightSteelBlue1"; # outline colour of canvas polygons
transCol = "#ffffff"; # transparent colour lol
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
winSize = f'{(canvW + (pad + bordWidth) * 2) * 2}x{canvH + 240}'; # window size

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

def fade(isIn, window):
    fadeIncr = (1 - winTrans) / steps;
    start = winTrans if isIn else 1;
    for i in range(steps):
        window.attributes("-alpha", start + (1 if isIn else -1) * (i + 1) * fadeIncr);
        time.sleep(0.02);

def calcCircXY(r, a):
    return (
        c + r * cos(a) + pad, # X
        outR + r * sin(a) + pad # Y
    );

# binds window hovering to the section
def bindHover(widget):
    widget.bind("<Enter>", lambda event: fade(True, publicWindow));
    widget.bind("<Leave>", lambda event: fade(False, publicWindow));

# now we make the circles do something
def polygonDoSomething(event, circle):
    x = event.x - c - pad;
    y = event.y - outR - pad;
    auxAng = 180 if x > 0 else 0;
    dist = sqrt((x ** 2) + (y ** 2));
    if inR <= dist and dist <= outR:
        theta = (90 if x == 0 else degrees(atan(y / x))) + 90 + auxAng;
        index = floor(theta * circle.pcs / 360);
        print(f'{circle.values[index]}');

################################ MAIN WINDOW ################################

# widgets and stuff
class KaoApp(Tk):
    def __init__(self):
        super().__init__();

        global publicWindow;
        publicWindow = self;
        
        self.drawWinInfo();
        self.assignWinAttr();
        self.centreWin();
        
        # top
        self.topFrame = TopSection(self);
        top = self.topFrame;
        bindHover(top);
        
        top.closeButton.assignQuit(self);
        top.closeButton.bindDragWin();
        
        # middle
        self.middleFrame = MiddleSection(self);
        middle = self.middleFrame;
        bindHover(middle);
        
        self.inCate = StringVar(value = "");
        self.inType = StringVar(value = "");
        middle.cateFrame.cateComb.assignStrVar(self.inCate);
        middle.typeFrame.typeComb.assignStrVar(self.inType);
        
        # bottom
        self.bottomFrame = BottomSection(self);
        bottom = self.bottomFrame;
        bindHover(bottom);
        
        self.mainloop();
    
    # main info
    def drawWinInfo(self):
        self.title("顔ウィール");
        self.minsize(width = 640, height = 480);
        self.geometry(winSize);
        self.iconbitmap("icon.ico");
    
    # assigns window attributes
    def assignWinAttr(self):
        self.overrideredirect(True);
        self.attributes("-alpha", winTrans);
        self.attributes("-transparentcolor", transCol);
        self.attributes("-topmost", True);
        self.config(bg = transCol);
        
    # centres window on the screen
    def centreWin(self):
        displayXOff = int(self.winfo_screenwidth() / 2 - canvW);
        displayYOff = int(self.winfo_screenheight() / 2 - canvH);
        self.geometry(f'{winSize}+{displayXOff}+{displayYOff}');

class Section(Frame):
    def __init__(self, master):
        super().__init__(master);
        self.pack(pady = pad);

################################ TOP ################################

class TopSection(Section):
    def __init__(self, master):
        super().__init__(master);
        
        self.closeButton = CloseButton(self);

class CloseButton(Button):
    def __init__(self, master):
        super().__init__(master, font = (myFont, 12), text = "X", fg = outlineCol, bg = fillCol);
        self.pack(side = "left");

    # assigns window closure
    def assignQuit(self, window):
        self.config(command = lambda: window.quit());

    # assigns dragging to the window
    def bindDragWin(self):
        self.bind('<Button-1>', saveLastClickPos);
        self.bind('<B1-Motion>', dragging);

################################ MIDDLE ################################

class MiddleSection(Section):
    def __init__(self, master):
        super().__init__(master);
        self.pack(pady = pad);
        
        # draws the initial frames and the category circle
        self.cateFrame = CateFrame(self);
        self.typeFrame = TypeFrame(self);
        self.cateFrame.cateCirc.drawCircle(len((list(all.keys()))), circAngOff, list(all.keys()));
        self.bindDrawCircle();
    
    # sets values of the types combobox based on the category selected
    def setTypesCombVal(self, types):
        self.typeFrame.typeComb.config(values = types);
        publicWindow.inType.set("");

    # whenever we select a category, we will:
    #   1. set the selectable values for the types combobox
    #   2. redraw the circle for said types combobox
    def bindDrawCircle(self):
        typeCircRef = self.typeFrame.typeCirc;
        typeCombRef = self.typeFrame.typeComb;
        cateCombRef = self.cateFrame.cateComb;
        events = [
            lambda event: self.setTypesCombVal(
                list(all[publicWindow.inCate.get()].keys())
            ),
            lambda event: typeCircRef.drawCircle(
                len(typeCombRef["values"]),
                circAngOff,
                typeCombRef["values"]
            )
        ];
        for event in events:
            cateCombRef.bind("<<ComboboxSelected>>", event, add = "+");

class SubCircleSection(Frame):
    def __init__(self, master, bkg = transCol):
        super().__init__(master, background = bkg);
        self.pack(side = "left");

class CateFrame(SubCircleSection):
    def __init__(self, master):
        super().__init__(master, bkg = transCol);
        
        self.createCateCircComb();

    def createCateCircComb(self):
        self.cateCirc = Circle(self);
        self.cateComb = Combo(self);
        self.cateComb.config(values = list(all.keys()));

class TypeFrame(SubCircleSection):
    def __init__(self, master):
        super().__init__(master);

        self.createTypeCircComb();

    def createTypeCircComb(self):
        self.typeCirc = Circle(self);
        self.typeComb = Combo(self);

class Circle(Canvas):
    def __init__(self, master, w = canvW + pad * 2, h = canvH + pad * 2):
        super().__init__(master, width = w, height = h);
        self.pack(pady = pad);
    
        self.bindClickCanvas();
    
    # draw filled polygons
    def drawPolygon(self, angOrd, radOrd):
        polyCorners = list(map(
            lambda i: calcCircXY(radOrd[i], angOrd[i]),
            range(4)
        ));
        
        polyPoints = [];
        for i in range(4):
            polyPoints.append(polyCorners[i]);
            if i % 2 == 0:
                angSteps = int(90 / len(angOrd));
                a0 = angOrd[i]; a1 = angOrd[i + 1];
                step = (a1 - a0) / angSteps;
                polyPoints.append(list(map(
					lambda j: calcCircXY(radOrd[i], a0 + j * step),
					range(angSteps)
				)));
        
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
        newButt = Button(
            publicWindow,
            font = (myFont, 18),
            text = "X",
            fg = "#000000",
            bg = "#fffff0"
        );
        self.create_window(
            c + pad, c + pad,
            anchor = CENTER,
            window = newButt,
            tags = ("polygon")
        );

    # experimental binding
    def bindClickCanvas(self):
        self.bind("<Button>", lambda event: polygonDoSomething(event, self));

class Combo(widg.Combobox):
    def __init__(self, master):
        super().__init__(master, font = (myFont, 8), width = 26, state = "readonly");
        self.pack(pady = pad);

    # assigns a string variable to the combobox
    def assignStrVar(self, strVar):
        self.config(textvariable = strVar);

################################ BOTTOM ################################

class BottomSection(Section):
    def __init__(self, master):
        super().__init__(master);

        self.createEnterButton();
        
    def createEnterButton(self):
        self.enterButton = EnterButton(self);

class EnterButton(Button):
    def __init__(self, master):
        super().__init__(master, font = (myFont, 12), text = "Enter");
        self.pack();

        self.bindCopyKaomoji();
    
    # when the enter button is pressed, a Kaomoji will be copied to keyboard
    def bindCopyKaomoji(self):
        for action in ["<Button>", "<KeyPress-Return>"]: self.bind(
            sequence = action,
            func = lambda event: copyKaoClpbrd(publicWindow.inCate.get(), publicWindow.inType.get()),
            add = "+"
        );
    
kaoWin = KaoApp();
