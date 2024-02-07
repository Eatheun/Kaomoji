from ..constants.constants import *
from ..setup.kaoCat import *
from tkinter import *
import numpy as np
from math import *
import random
import pyperclip as clpbrd

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

# calculates circle coordinates
def calcCircXY(r, a):
    return (
        c + r * cos(a) + pad, # X
        outR + r * sin(a) + pad # Y
    );

# now we make the circles do something, 0 for categories, 1 for types
currFrame = 0;
vals = ["", ""];
currList = list(all.keys());

# selects category/kaoType if warranted
def selectVal(x, y, circle):
    global currFrame, vals, currList;
    auxAng = 180 if x > 0 else 0; # translating angles of any magnitude
    invX = 90 if y < 0 else 270; # factors in invalid X values
    theta = (invX if x == 0 else degrees(atan(y / x))) + 90 + auxAng; # calculates theta of mouse
    index = floor(theta * circle.pcs / 360); # calculates index to the circle's values
    
    # set the values and change the frame
    vals[currFrame] = circle.values[index];
    if currFrame == 0:
        currList = list(all[vals[0]].keys());
    else:
        currList = list(all.keys());
        copyKaoClpbrd(vals[0], vals[1]);
    circle.drawCircle(len(currList), circAngOff, currList);
    currFrame = (currFrame + 1) % 2;

# checks if we clicked on the circle
def interactCircle(event, circle, cCircOff, window):
    x = event.x - c - pad;
    y = event.y - outR - pad;
    dist = sqrt((x ** 2) + (y ** 2));
    if inR <= dist and dist <= outR:
        selectVal(x, y, circle); # selects the value
    elif 0 <= dist and dist <= cCircOff:
        window.quit(); # quits if we selected the centre

# calculate the polygon points
def calcPolyPoints(angOrd, radOrd):
    polyCorners = list(map(lambda i: calcCircXY(radOrd[i], angOrd[i]), range(4)));
    polyPoints = [];
    for i in range(4):
        polyPoints.append(polyCorners[i]);
        if i % 2 == 0:
            angSteps = int(90 / len(angOrd));
            a0 = angOrd[i]; a1 = angOrd[i + 1];
            step = (a1 - a0) / angSteps;
            polyPoints.append(list(map(lambda j: calcCircXY(radOrd[i], a0 + j * step),range(angSteps))));
    return polyPoints;

# draw filled polygons
def drawPolygons(self, values):
    # offset metrics
    inOff = radians(min(self.angleOff, 180 / self.pcs));
    outOff = atan((inR / outR) * (tan(inOff)));
    
    # loop through angles as cosi + isini
    angles = np.linspace(90, 450, self.pcs + 1);
    for i in range(self.pcs):
        # current and next angle of each polygon
        curr = radians(angles[i]);
        next = curr + radians(360 / self.pcs);
        
        # order angles and radii for each corresponding point, with offsets
        angOrd = [curr + outOff, next - outOff, next - inOff, curr + inOff];
        radOrd = [outR, outR, inR, inR];
        
        self.create_polygon(
            calcPolyPoints(angOrd, radOrd),
            fill = fillCol,
            width = lineWeight,
            outline = outlineCol,
            tags = ("polygon")
        );
        
        # overlaying current value as text
        midRad = (outR + inR) / 2;
        midAng = (curr + next) / 2;
        tag = values[i].replace(" ", "\n");
        self.create_text(
            calcCircXY(midRad, midAng),
            anchor = CENTER,
            font = (myFont, floor((4 / self.pcs) * baseFontSize)),
            fill = outlineCol,
            text = tag,
            tags = ("polygon")
        );

# draw centre with window.quit() bound
def drawCentre(self, window):
    offSpace = sqrt(2 * (inR ** 2) * (1 - cos(radians(2 * self.angleOff))));
    cCircOff = inR - offSpace;
    p1, p2 = c - cCircOff + pad, c + cCircOff + pad;
    self.create_oval(
        [(p1, p1), (p2, p2)],
        fill = fillCol,
        outline = outlineCol,
        width = lineWeight,
        tags = ("centre")
    );
    self.create_text(
        [(c + pad, c + pad)],
        anchor = CENTER,
        font = (myFont, 18),
        text = "X",
        fill = outlineCol,
        tags = ("centre")
    );
    
    # binds the circle selecting to the circle
    self.bind("<Button>", lambda event: interactCircle(event, self, cCircOff, window));
    