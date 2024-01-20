import pyautogui as pag
import time
import random
import win32api as wapi, win32con as wcon
import pyperclip as clpbrd
import kaoCat as dat
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

################################-#-##-#-################################
################################  MAIN  ################################
################################-#-##-#-################################

# # gather necessary data, first index is for categories, second for Kaotype
# catInd = 0;
# typeInd = 0;

# # retrieve from the database
# category = "";
# for key in dat.all.keys():
#     category = key;
#     if (catInd := catInd - 1) < 0: break;
# kaoType = "";
# for key in dat.all[category].keys():
#     kaoType = key;
#     if (typeInd := typeInd - 1) < 0: break;

# # copy to clipboard
# copyKaoClpbrd(category, kaoType, dat.all[category][kaoType]);

# # click into Discord
# screenW = int(wapi.GetSystemMetrics(0)) >> 2;
# screenH = int(wapi.GetSystemMetrics(1)); screenH -= screenH / 20;
# click(int(screenW), int(screenH));

# # paste into message box
# paste(); pag.keyDown('enter'); pag.keyUp('enter');

def convert():
    initVal = entIntVal.get() * 2;
    outStr.set(initVal);

# make window
window = widg.Window(themename = "vapor");
window.title("顔ウィール");
window.geometry("800x600");

# words
titleLabel = widg.Label(master = window, text = "Select a Kaomoji:", font = ("Comic Sans MS Bold", 30));

# clickies
inputFrame = widg.Frame(master = window);
entIntVal = tk.IntVar();
entry = widg.Entry(master = inputFrame, textvariable = entIntVal);
button = widg.Button(master = inputFrame, text = "MEEEEEE!!!", command = convert);

# outies
outStr = tk.StringVar();
outputLabel = widg.Label(
    master = window,
    font = ("Comic Sans MS", 18),
    textvariable = outStr
);

# event
window.bind("<Any-KeyPress-Return>", lambda event: convert());

# packing
titleLabel.pack();
entry.pack(side = "left", padx = 20);
button.pack(side = "left");
inputFrame.pack(pady = 20);
outputLabel.pack();

# run Forest run
window.mainloop();
