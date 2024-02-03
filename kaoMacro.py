import pyautogui as pag
import time
import random
import win32api as wapi, win32con as wcon
import pyperclip as clpbrd
from kaoCat import *
from tkinter import *
import ttkbootstrap as widg
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

# a bunch of metrics and constants
myFont = "Comic Sans MS Bold";
padding = 10;
circOutR = 240;
circInR = 80;
canvH = circOutR * 2;
canvW = circOutR * 2;
circAngleOffset = 10;
winSize = str(canvW * 2) + "x" + str(canvH * 2);
winTrans = 0.2;

# helper funkies
def drawWin():
    # drawing the main window
    window = widg.Window(themename = "vapor");
    window.title("顔ウィール");
    window.geometry(winSize);
    window.minsize(width = 640, height = 640);
    window.iconbitmap("icon.ico");
    window.overrideredirect(True);
    
    # changing attributes
    window.attributes("-alpha", winTrans);
    window.attributes("-topmost", True);
    window.config(bg = "#add123");
    window.wm_attributes("-transparentcolor", "#add123");
    return window;

fadeSteps = 4;
fadeIncr = (1 - winTrans) / fadeSteps;

def fadeIn():
    for i in range(fadeSteps):
        window.attributes("-alpha", winTrans + (i + 1) * fadeIncr);
        time.sleep(0.01);

def fadeOut():
    for i in range(fadeSteps):
        window.attributes("-alpha", 1 - i * fadeIncr);
        time.sleep(0.01);

# grabs all the kaoTypes from a category
def grabTypes(cate):
    types = [];
    if cate in all:
        for kaoType in all[cate]: types.append(kaoType);
    return types;

# sets values of the types combobox based on the category selected
def setTypesCombVal(types):
    typesComB.config(values = types);
    inType.set("");

# does something special when a specific polygon is selected
def polygonAction(polygon):
    print(str(polygon));

# draws a bunch of top-truncated triangles in a circle
def drawCircle(circle, pcs, angleOff, overlayText):
    if pcs == 0: return;
    
    # basic metrics
    cntr = canvW / 2;
    radii = [circOutR, circInR];
    outOff = radians(min(angleOff, 180 / pcs));
    inOff = atan((radii[1] / radii[0]) * (tan(outOff)));
    
    # loop through angles as cosi + isini
    angles = np.linspace(90, 450, pcs + 1);
    for i in range(pcs):
        curr = radians(angles[i]);
        next = radians(angles[i] + 360 / pcs);
        pointOrder = [
            curr + inOff,
            next - inOff,
            next - outOff,
            curr + outOff
        ]; # order of the angles for each point
        
        # calculate the points of the polygon
        polygonPoints = [];
        for j in range(4): # 4 points
            currRad = radii[j > 1]; # cheaty cheaty
            polygonPoints.append(
                (
                    cntr + currRad * cos(pointOrder[j]), # x value
                    radii[0] + currRad * sin(pointOrder[j]) # y value
                )
            );
        
        # draw it
        specialTag = overlayText[i];
        circle.create_polygon(
            polygonPoints,
            fill = "turquoise4",
            disabledfill = "#add123",
            outline = "LightSteelBlue1",
            width = 2,
            tags = ("polygon", "hello" + str(i))
        );
        circle.tag_bind("hello" + str(i), "<Button>", lambda event: polygonAction(i));

# clears and draws near circles
def setDrawCircle(circle, pcs, angleOff, overlayText):
    circle.delete("polygon");
    drawCircle(circle, pcs, angleOff, overlayText);

# packing helpers
# top
def packTopFrame():
	topFrame.pack(pady = padding);
	closeButt.pack(side = "left");
	titleLabel.pack(side = "left");

# middle
def packMiddleFrame():
	middleFrame.pack(pady = padding);
	cateFrame.pack(padx = padding, side = "left");
	cateCircle.pack(pady = padding); catComB.pack(pady = padding);
	typeFrame.pack(padx = padding, side = "left");
	typeCircle.pack(pady = padding); typesComB.pack(pady = padding);

def packBottomFrame():
	bottomFrame.pack(pady = padding);
	entButt.pack();

# makes the entire window opaque/transparent when mouse enters/leaves
def bindHover(frame):
	frame.bind("<Enter>", lambda event: fadeIn());
	frame.bind("<Leave>", lambda event: fadeOut());

# dragging the window around
lastClickX = 0;
lastClickY = 0;
def saveLastClickPos(event):
    global lastClickX, lastClickY;
    lastClickX = event.x;
    lastClickY = event.y;

def dragging(event):
	x = event.x - lastClickX + window.winfo_x();
	y = event.y - lastClickY + window.winfo_y();
	window.geometry("+%s+%s" % (x , y));

################################-#-##-#-################################
################################  MAIN  ################################
################################-#-##-#-################################

################################ WINDOW ################################

# make window
window = drawWin();

################################ FRAMES ################################

# framing
topFrame = Frame(window); bindHover(topFrame);
middleFrame = Frame(window, bg = "#add123"); bindHover(middleFrame);
bottomFrame = Frame(window, bg = "#add123"); bindHover(bottomFrame);

################################ CLOSE BUTTON ################################

# close window button
closeButt = widg.Button(topFrame, text = "X");
closeButt.bind("<Button>", lambda event: window.quit());

################################ TITLE ################################

# title
titleLabel = widg.Label(
    topFrame,
    text = "Select a Kaomoji:",
    font = (myFont, 18)
);
titleLabel.bind('<Button-1>', saveLastClickPos);
titleLabel.bind('<B1-Motion>', dragging);

################################ CIRCLES + COMBOBOX ################################

# frames for the circles and the comboboxs
cateFrame = Frame(middleFrame, bg = "#add123");
typeFrame = Frame(middleFrame, bg = "#add123");

# circles
cateCircle = Canvas(cateFrame, width = canvW, height = canvH, bg = "#add123");
typeCircle = Canvas(typeFrame, width = canvW, height = canvH, bg = "#add123");

# C-C-C-C-COMBOOOBOOOOOOX
inCate = StringVar(value = "");
catComB = widg.Combobox(
    cateFrame,
    values = list(all.keys()),
    textvariable = inCate,
    font = (myFont, 8),
    width = 26,
    state = "readonly"
);
inType = StringVar(value = "");
typesComB = widg.Combobox(
    typeFrame,
    textvariable = inType,
    font = (myFont, 8),
    width = 26,
    state = "readonly"
);

# whenever we select a category, we will:
#   1. set the selectable values for the types combobox
#   2. redraw the circle for said types combobox
events = [
    lambda event: setTypesCombVal(
        grabTypes(inCate.get())
    ),
    lambda event: setDrawCircle(
        typeCircle,
        len(typesComB["values"]),
        circAngleOffset,
        typesComB["values"]
    )
];
for event in events:
    catComB.bind("<<ComboboxSelected>>", event, add = "+");

################################ ENTER BUTTON ################################

# enter button
entButt = widg.Button(bottomFrame, text = "Enter");

# when entered, copies a Kaomoji to the clipboard
for action in ["<Button>", "<KeyPress-Return>"]: entButt.bind(
    sequence = action,
    func = lambda event: copyKaoClpbrd(inCate.get(), inType.get())
);

################################ AFTERMATH ################################

# packing order
packTopFrame();
packMiddleFrame();
packBottomFrame();

# draw the circles
setDrawCircle(
    cateCircle,
    len(catComB["values"]),
    circAngleOffset,
    list(all.keys())
);

# run Forest run
window.mainloop();
