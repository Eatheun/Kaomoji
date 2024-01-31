import pyautogui as pag
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
winSize = "640x480";
paddingY = 10;
circOutR = 120;
circInR = 30;
canvH = circOutR * 2 + paddingY;
canvW = 300;
circAngleOffset = 10;

# helper funkies
def drawWin():
    window = widg.Window(themename = "vapor");
    window.title("顔ウィール");
    window.geometry(winSize);
    return window;

# grabs all the kaoTypes from a category
def grabTypes(cate):
    types = [];
    if cate in all:
        for kaoType in all[cate]: types.append(kaoType);
    return types;

# grabs the category selected in the combobox
def grabCate(strVar):
    return strVar.get();

# sets values of the types combobox based on the category selected
def setTypesCombVal(types):
    typesComB.config(values = types);
    inType.set("");

# draws a bunch of top-truncated triangles in a circle
def drawCircle(circle, pcs, angleOff):
    if pcs == 0: return circle;
    
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
        
        polygonPoints = [];
        for i in range(4): # 4 points
            currRad = radii[i > 1]; # cheaty cheaty
            polygonPoints.append(
                (
                    cntr + currRad * cos(pointOrder[i]), # x value
                    radii[0] + currRad * sin(pointOrder[i]) # y value
                )
            );
        
        circle.create_polygon(
            polygonPoints,
            fill = "turquoise4",
            outline = "LightSteelBlue1",
            width = 5,
            tags = ("polygon")
        );
    
    return circle;

# clears and draws near circles
def setDrawCircle(circle, pcs, angleOff):
    circle.delete("polygon");
    circle = drawCircle(circle, pcs, angleOff);

################################-#-##-#-################################
################################  MAIN  ################################
################################-#-##-#-################################

# make window and title
window = drawWin();
titleLabel = widg.Label(
    master = window,
    text = "Select a Kaomoji:",
    font = (myFont, 18)
);

# circles
cateCircle = Canvas(master = window, width = canvW, height = canvH);
typeCircle = Canvas(master = window, width = canvW, height = canvH);
entButt = widg.Button(master = window, text = "Enter");

# C-C-C-C-COMBOOOBOOOOOOX
inCate = StringVar(value = "");
catComB = widg.Combobox(
    master = window,
    values = list(all.keys()),
    textvariable = inCate,
    font = (myFont, 8),
    state = "readonly"
);
inType = StringVar(value = "");
typesComB = widg.Combobox(
    master = window,
    textvariable = inType,
    font = (myFont, 8),
    state = "readonly"
);

# packing order
titleLabel.pack();
cateCircle.pack(); typeCircle.pack();
catComB.pack(pady = paddingY);
typesComB.pack(pady = paddingY);
entButt.pack(pady = paddingY);

# when entered, copies a Kaomoji to the clipboard
for action in ["<Button>", "<KeyPress-Return>"]: entButt.bind(
    sequence = action,
    func = lambda event: copyKaoClpbrd(inCate.get(), inType.get())
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
        circAngleOffset
    )
];
for event in events:
    catComB.bind("<<ComboboxSelected>>", event, add = "+");

# draw the circles
setDrawCircle(
    cateCircle,
    len(catComB["values"]),
    circAngleOffset
);

# run Forest run
window.mainloop();
