import pyautogui as pag
import time
import random
import win32api as wapi, win32con as wcon
import pyperclip as clpbrd
from kaoCat import *
import tkinter as tk
import ttkbootstrap as widg
import numpy as np
from math import *

################################ STAGE 3 ################################

# Gets a random Kaomoji and copies it to the clipboard
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

myFont = "Comic Sans MS Bold";
myResSize = "640x480";

# helper funkies
def drawWin():
    window = widg.Window(themename = "vapor");
    window.title("顔ウィール");
    window.geometry(myResSize);
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
def drawTriCircle(circle, pcs):
    cntr = 280;
    outR = 160;
    inR = 60;
    off = 6;
    
    for i in np.linspace(0, 360, pcs + 1):
        if i == 360: continue;
        curr = radians(i + off);
        next = radians(i + 360 / pcs - off);
        cosCur = cos(curr); cosNext = cos(next);
        sinCur = sin(curr); sinNext = sin(next);
        
        circle.create_polygon(
            cntr + outR * cosCur, outR + outR * sinCur,
            cntr + outR * cosNext, outR + outR * sinNext,
            cntr + inR * cosNext, outR + inR * sinNext,
            cntr + inR * cosCur, outR + inR * sinCur,
            fill = "red"
        );
    

################################-#-##-#-################################
################################  MAIN  ################################
################################-#-##-#-################################

# make window
window = drawWin();

# shapes
myCoord = (80, 0, 640 - (80 << 1), 100);
cateCircle = tk.Canvas(master = window);

# big title
titleLabel = widg.Label(master = window, text = "Select a Kaomoji:", font = (myFont, 18));

# clickies
entButt = widg.Button(master = window, text = "Enter");

# combos
inCate = tk.StringVar(value = "");
catComB = widg.Combobox(
    master = window,
    values = list(all.keys()),
    textvariable = inCate,
    font = (myFont, 8),
    state = "readonly"
);
inType = tk.StringVar(value = "");
typesComB = widg.Combobox(
    master = window,
    textvariable = inType,
    font = (myFont, 8),
    state = "readonly"
);

# events
catComB.bind(
    "<<ComboboxSelected>>",
    lambda event: setTypesCombVal(grabTypes(inCate.get()))
);
for event in ["<Button>", "<KeyPress-Return>"]: entButt.bind(
    sequence = event,
    func = lambda event: copyKaoClpbrd(inCate.get(), inType.get())
);

# packing order
titleLabel.pack();
cateCircle.pack();
catComB.pack(pady = 10);
typesComB.pack(pady = 10);
entButt.pack(pady = 10);

# these will change as we select the goodies
drawTriCircle(cateCircle, 9);

# run Forest run
window.mainloop();
