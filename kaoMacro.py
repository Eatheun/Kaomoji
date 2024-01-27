import pyautogui as pag
import time
import random
import win32api as wapi, win32con as wcon
import pyperclip as clpbrd
from kaoCat import *
import tkinter as tk
import ttkbootstrap as widg

################################ STAGE 3 ################################

# wtf do you think this does
def click(x, y):
	wapi.SetCursorPos((x, y));
	wapi.mouse_event(wcon.MOUSEEVENTF_LEFTDOWN, 0, 0);
	time.sleep(0.1);
	wapi.mouse_event(wcon.MOUSEEVENTF_LEFTUP, 0, 0);

# Gets a random Kaomoji and copies it to the clipboard
def copyKaoClpbrd(category, kaoType, kaoNum):
    # concatenating the giant relative path
    filepath = "./All Kaomojis" + "/" + category + "/" + kaoType + ".txt";
    with open(filepath, "r", encoding = "utf-8") as kaoFile:
        kaomoji = "";
        for i in range(random.randrange(kaoNum)): kaomoji = kaoFile.readline();
        clpbrd.copy(kaomoji);

# CRTL + V
def paste():
    pag.keyDown('ctrl');
    pag.keyDown('v');
    pag.keyUp('v');
    pag.keyUp('ctrl');

# retrieves the category and Kaotype for the user
def retrieveData(catInd, typeInd):
    category = "";
    for key in all.keys():
        category = key;
        if (catInd := catInd - 1) < 0: break;
    kaoType = "";
    for key in all[category].keys():
        kaoType = key;
        if (typeInd := typeInd - 1) < 0: break;

    return category, kaoType;

################################ STAGE 4 ################################

def drawWin():
    window = widg.Window(themename = "vapor");
    window.title("顔ウィール");
    window.geometry("800x600");
    return window;

################################-#-##-#-################################
################################  MAIN  ################################
################################-#-##-#-################################

# # gather necessary data, first index is for categories, second for Kaotype
# catInd = 0;
# typeInd = 0;
# category, kaoType = retrieveData(catInd, typeInd);

# # copy to clipboard
# copyKaoClpbrd(category, kaoType, all[category][kaoType]);

# # click into Discord
# screenW = int(wapi.GetSystemMetrics(0));
# screenH = int(wapi.GetSystemMetrics(1));
# click(int(screenW >> 2), int(screenH * 19 / 20));

# # paste into message box
# paste(); pag.keyDown('enter'); pag.keyUp('enter');

# helper funkies
def grabTypes(cate):
    types = [];
    if cate in all:
        for kaoType in all[cate]: types.append(kaoType);
    return types;

def grabCate(strVar):
    return strVar.get();

def setTypesCombVal(typesComB, types):
    typesComB.config(values = types);

# make window
window = drawWin();

# big title
titleLabel = widg.Label(master = window, text = "Select a Kaomoji:", font = ("Comic Sans MS Bold", 30));

# combos
inCate = tk.StringVar(); inCate.set("");
catComB = widg.Combobox(master = window, values = list(all.keys()), textvariable = inCate);
typesComB = widg.Combobox(master = window);

# events
typesComB.bind(
    "<Enter>",
    lambda event: setTypesCombVal(
        typesComB,
        grabTypes(inCate.get())
    )
);

# packing
titleLabel.pack();
catComB.pack(pady = 10);
typesComB.pack(pady = 10);

# run Forest run
window.mainloop();
