import pyautogui as pag

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
