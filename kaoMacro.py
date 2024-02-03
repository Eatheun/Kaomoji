from xmlrpc.client import boolean
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
myFont = "Comic Sans MS Bold"; # title font
padding = 10; # general padding
circOutR = 240; # outer radius of canvas circle
circInR = 80; # inner radius of canvas circle cutout
canvH = circOutR * 2; # height of canvas
canvW = circOutR * 2; # width of canvas
circAngleOffset = 10; # gap between each polygon in the canvas circle
bordWidth = 3; # border width of the canvas
lineWeight = 8; # weight of the polygon outlines
winSize = f'{(canvW + (padding + bordWidth) * 2) * 2}x{canvH * 2}'; # window size
winTrans = 0.3; # base transparency of window
fillCol = "turquoise4"; # fill colour of canvas polygons
outlineCol = "LightSteelBlue1"; # outline colour of canvas polygons
steps = 5; # general steps to increment

# helper funkies
def drawWin():
    # drawing the main window
    window = widg.Window();
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

def centreWin(window):
	displayXOff = int(window.winfo_screenwidth() / 2 - canvW);
	displayYOff = int(window.winfo_screenheight() / 2 - canvH);
	window.geometry(f'{winSize}+{displayXOff}+{displayYOff}');
	return window;

def fade(isIn: boolean):
    fadeIncr = (1 - winTrans) / steps;
    start = winTrans if isIn else 1;
    for i in range(steps):
        kaoWin.attributes("-alpha", start + (1 if isIn else -1) * (i + 1) * fadeIncr);
        time.sleep(0.02);

# sets values of the types combobox based on the category selected
def setTypesCombVal(types):
    typesComB.config(values = types);
    inType.set("");

# initiates a new circle canvas
def circleInit(frame):
    return Canvas(
        frame,
        width = canvW + padding * 2,
        height = canvH + padding * 2,
        borderwidth = bordWidth,
        relief = "raised"
    );

# draws the curved edges of each polygon
def drawCircCurve(circle, cntr, radius, ang1, ang2):
    angleDiff = (ang2 - ang1) / steps;
    curvePoints = list(map(
        lambda i: (
            (cntr + radius * cos(ang1 + i * angleDiff)) + padding,
            circOutR + radius * sin(ang1 + i * angleDiff) + padding
        ),
        range(steps + 1)
    ));
    circle.create_line(
        curvePoints,
        fill = outlineCol,
        smooth = True,
        width = lineWeight,
        tags = ("polygon")
    );

# draws the straight edges of each polygon
def drawCircLine(circle, cntr, ang1, ang2):
    pointPairs = [(circOutR, ang1), (circInR, ang2)];
    linePoints = list(map(
        lambda point: (
            cntr + point[0] * cos(point[1]) + padding,
            circOutR + point[0] * sin(point[1]) + padding
        ),
        pointPairs
    ));
    circle.create_line(
        linePoints,
        fill = outlineCol,
        width = lineWeight,
        tags = ("polygon")
    );

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
        order = [
            curr + inOff,
            next - inOff,
            next - outOff,
            curr + outOff
        ]; # order of the angles for each point
        
		# out/in curve
        drawCircCurve(circle, cntr, circOutR, order[0], order[1]);
        drawCircCurve(circle, cntr, circInR, order[2], order[3]);
        
		# curr/next side lines
        drawCircLine(circle, cntr, order[1], order[2]);
        drawCircLine(circle, cntr, order[0], order[3]);
        
	# draw centre circle
    offSpace = sqrt(2 * (circInR ** 2) * (1 - cos(radians(2 * angleOff))));
    cntrCircOff = circInR - offSpace;
    p1, p2 = cntr - cntrCircOff + padding, cntr + cntrCircOff + padding
    circle.create_oval(
		[(p1, p1), (p2, p2)],
		fill = fillCol,
		outline = outlineCol,
		width = lineWeight,
		tags = ("centre")
    );

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
	cateFrame.pack(side = "left");
	cateCircle.pack(pady = padding); catComB.pack(pady = padding);
	typeFrame.pack(side = "left");
	typeCircle.pack(pady = padding); typesComB.pack(pady = padding);

def packBottomFrame():
	bottomFrame.pack(pady = padding);
	entButt.pack();

# makes the entire kaoWin opaque/transparent when mouse enters/leaves
def bindHover(frame):
	frame.bind("<Enter>", lambda event: fade(True));
	frame.bind("<Leave>", lambda event: fade(False));

# dragging the kaoWin around
lastClickX = 0;
lastClickY = 0;
def saveLastClickPos(event):
    global lastClickX, lastClickY;
    lastClickX = event.x;
    lastClickY = event.y;

def dragging(event):
	x = event.x - lastClickX + kaoWin.winfo_x();
	y = event.y - lastClickY + kaoWin.winfo_y();
	kaoWin.geometry("+%s+%s" % (x , y));

################################-#-##-#-################################
################################  MAIN  ################################
################################-#-##-#-################################

################################ WINDOW ################################

# make window
kaoWin = drawWin();
kaoWin = centreWin(kaoWin);

################################ FRAMES ################################

# framing
topFrame = Frame(kaoWin, bg = "#add123"); bindHover(topFrame);
middleFrame = Frame(kaoWin, bg = "#add123"); bindHover(middleFrame);
bottomFrame = Frame(kaoWin, bg = "#add123"); bindHover(bottomFrame);

################################ CLOSE BUTTON ################################

# close kaoWin button
closeButt = widg.Button(topFrame, text = "X", command = lambda: kaoWin.quit());

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
cateCircle = circleInit(cateFrame);
typeCircle = circleInit(typeFrame);

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
        list(all[inCate.get()].keys())
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
kaoWin.mainloop();
