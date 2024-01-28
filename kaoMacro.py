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
def drawCircle(circle, pcs):
    if pcs == 0: return circle;
    
    # basic metrics
    cntr = 60;
    outR = 28;
    inR = 8;
    off = 2;
    
    # loop through angles as cosi + isini
    angles = np.linspace(90, 450, pcs + 1);
    for i in range(pcs):
        curr = radians(angles[i] + off);
        next = radians(angles[i] + 360 / pcs - off);
        cosCur = cos(curr); cosNext = cos(next);
        sinCur = sin(curr); sinNext = sin(next);
        
        circle.create_polygon(
            cntr + outR * cosCur, outR + outR * sinCur,
            cntr + outR * cosNext, outR + outR * sinNext,
            cntr + inR * cosNext, outR + inR * sinNext,
            cntr + inR * cosCur, outR + inR * sinCur,
            fill = "red",
            tags = ("polygon")
        );
    
    return circle;

def setDrawCircle(circle, pcs):
    circle.delete("polygon");
    circle = drawCircle(circle, pcs);

################################-#-##-#-################################
################################  MAIN  ################################
################################-#-##-#-################################

# make window
window = drawWin();

# circles
cateCircle = Canvas(master = window, width = 120, height = 60);
typeCircle = Canvas(master = window, width = 120, height = 60);

# big title
titleLabel = widg.Label(master = window, text = "Select a Kaomoji:", font = (myFont, 18));

# clickies
entButt = widg.Button(master = window, text = "Enter");

# combos
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

# sets the values of the types combobox to the types of the category selected
catComB.bind(
    "<<ComboboxSelected>>",
    lambda event: setTypesCombVal(grabTypes(inCate.get()))
);

# when entered, copies a Kaomoji to the clipboard
for event in ["<Button>", "<KeyPress-Return>"]: entButt.bind(
    sequence = event,
    func = lambda event: copyKaoClpbrd(inCate.get(), inType.get())
);

# experimental circle production
catComB.bind(
    "<<ComboboxSelected>>",
    lambda event: setDrawCircle(
        typeCircle,
        len(typesComB["values"])
    ),
    add = "+"
);

# packing order
titleLabel.pack();
cateCircle.pack(); typeCircle.pack();
catComB.pack(pady = 10);
typesComB.pack(pady = 10);
entButt.pack(pady = 10);

# draw the circles
setDrawCircle(
    cateCircle,
    len(catComB["values"])
);

# run Forest run
window.mainloop();
