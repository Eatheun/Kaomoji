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

#### CONSTANTS ####
# text
myFont = "Comic Sans MS Bold"; # title font
fillCol = "turquoise4"; # fill colour of canvas polygons
outlineCol = "LightSteelBlue1"; # outline colour of canvas polygons
transCol = "#add123"; # transparent colour lol

# canvas metrics
circOutR = 160; # outer radius of canvas circle
circInR = 50; # inner radius of canvas circle cutout
c = circOutR; # centre of circle
circAngleOffset = 10; # gap between each polygon in the canvas circle

# tkinter
bordWidth = 3; # border width of the canvas
lineWeight = 8; # weight of the polygon outlines
winTrans = 0.3; # base transparency of window
steps = 5; # general steps to increment

# display port metrics
padding = 10; # general padding
canvH = circOutR * 2; # height of canvas
canvW = circOutR * 2; # width of canvas
winSize = f'{(canvW + (padding + bordWidth) * 2) * 2}x{canvH + 240}'; # window size

# Helper functions
lastClickX = 0;
lastClickY = 0;
publicWindow = "";
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

################################ MAIN WINDOW ################################

# widgets and stuff
class KaoApp(Tk):
    def __init__(self):
        super().__init__();
        
        self.drawWinInfo();
        self.assignWinAttr();
        self.centreWin();
        
        # top
        self.topFrame = TopSection(self);
        top = self.topFrame;
        top.closeButton.assignQuit(self);
        top.title.assignDragWin(self);
        
        # middle
        self.inCate = StringVar(value = "");
        self.inType = StringVar(value = "");
        self.middleFrame = MiddleSection(self);
        middle = self.middleFrame;
        middle.cateFrame.cateComb.assignStrVar(self.inCate);
        middle.typeFrame.typeComb.assignStrVar(self.inType);
        
        # bottom
        self.bottomFrame = BottomSection(self);
        
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
        self.config(bg = transCol);
        self.wm_attributes("-transparentcolor", transCol);
        
    # centres window on the screen
    def centreWin(self):
        displayXOff = int(self.winfo_screenwidth() / 2 - canvW);
        displayYOff = int(self.winfo_screenheight() / 2 - canvH);
        self.geometry(f'{winSize}+{displayXOff}+{displayYOff}');

class Section(Frame):
    def __init__(self, master, bkg = transCol):
        super().__init__(master, background = bkg);
        self.pack(pady = padding);
        
        self.bindHover(master);

    def bindHover(self, window):
        self.bind("<Enter>", lambda event: fade(True, window));
        self.bind("<Leave>", lambda event: fade(False, window));

################################ TOP ################################

class TopSection(Section):
    def __init__(self, master):
        super().__init__(master);
        
        self.closeButton = CloseButton(self);
        self.title = Title(self);

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
    
    # assigns dragging to the window
    def assignDragWin(self, window):
        global publicWindow;
        publicWindow = window;
        self.bind('<Button-1>', saveLastClickPos);
        self.bind('<B1-Motion>', dragging);

################################ MIDDLE ################################

class MiddleSection(Section):
    def __init__(self, master):
        super().__init__(master);
        self.pack(pady = padding);
        
        # draws the initial frames and the category circle
        self.cateFrame = CateFrame(self);
        self.typeFrame = TypeFrame(self);
        self.cateFrame.cateCirc.drawCircle(len((list(all.keys()))), circAngleOffset);
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
                circAngleOffset
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
        super().__init__(master);
        
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
    def __init__(self, master, w = canvW + padding * 2, h = canvH + padding * 2, bdw = bordWidth, rlf = "raised"):
        super().__init__(master, width = w, height = h, borderwidth = bdw, relief = rlf);
        self.pack(pady = padding);
    
    # draws the curved edges of each polygon
    def drawCircCurve(self, r, a1, a2):
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
    def drawCircLine(self, a1, a2):
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
        self.delete("polygon"); # clears all the circles before
        
        # basic metrics
        outOff = radians(min(angleOff, 180 / pcs));
        inOff = atan((circInR / circOutR) * (tan(outOff)));
        
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

class Combo(widg.Combobox):
    def __init__(self, master):
        super().__init__(master, font = (myFont, 8), width = 26, state = "readonly");
        self.pack(pady = padding);

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
        super().__init__(master, text = "Enter");
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
