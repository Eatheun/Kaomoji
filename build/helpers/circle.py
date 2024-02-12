from ..constants.constants import *
from ..setup.kaoCat import *
from tkinter import *
from time import sleep
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
        if i % 2 == 0: # for curved areas
            angSteps = int(45 / len(angOrd));
            a0 = angOrd[i]; a1 = angOrd[i + 1];
            step = (a1 - a0) / angSteps;
            polyPoints.append(list(map(lambda j: calcCircXY(radOrd[i], a0 + j * step), range(angSteps))));
    return polyPoints;

# animation for drawing the polygons
def drawPolygonAnim(self, window, values, angles, i, currR):
    self.delete(values[i]);
    # current and next angle of each polygon
    curr = radians(angles[i]);
    next = curr + radians(360 / self.pcs);
    
    # order angles and radii for each corresponding point, with offsets
    angOrd = [curr + self.outOff, next - self.outOff, next - self.inOff, curr + self.inOff];
    radOrd = [currR, currR, inR, inR];
    
    self.create_polygon(
        calcPolyPoints(angOrd, radOrd),
        fill = fillCol,
        width = lineWeight,
        outline = outlineCol,
        tags = ("polygon", values[i])
    );
    
    # overlaying current value as text
    midRad = (currR + inR) / 2;
    midAng = (curr + next) / 2;
    tag = values[i].replace(" ", "\n");
    self.create_text(
        calcCircXY(midRad, midAng),
        anchor = CENTER,
        font = (myFont, floor((4 / self.pcs) * baseFontSize * (currR - inR) / (outR - inR))), # scale with the current increment
        fill = outlineCol,
        text = tag,
        tags = ("polygon", values[i])
    );
    if currR <= outR:
        window.after(10, drawPolygonAnim, self, window, values, angles, i, currR + self.incrR);

# adds a delay before each polygon animation
def drawPolygonsFanWrap(self, window, values, angles, i):
    drawPolygonAnim(self, window, values, angles, i, self.incrR + inR);
    if i + 1 < self.pcs:
        window.after(30, drawPolygonsFanWrap, self, window, values, angles, i + 1);

# draw filled polygons
def drawPolygons(self, window, values):
    # offset metrics
    self.inOff = radians(min(self.angleOff, 180 / self.pcs));
    self.outOff = atan((inR / outR) * (tan(self.inOff)));
    
    # loop through angles as cosi + isini
    angles = np.linspace(90, 450, self.pcs + 1);
    self.incrR = (outR - inR) / (steps << 1);
    drawPolygonsFanWrap(self, window, values, angles, 0);

# animation for drawing centre of circle
def drawCentreAnim(self, window, currIncr):
    p1, p2 = c - currIncr + pad, c + currIncr + pad;
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
        font = (myFont, int(18 * currIncr / self.cCircOff)), # scale with the current increment
        text = "X",
        fill = outlineCol,
        tags = ("centre")
    );
    if currIncr <= self.cCircOff:
        window.after(5, drawCentreAnim, self, window, currIncr + self.offIncr);

# draw centre with window.quit() bound
def drawCentre(self, window):
    offSpace = sqrt(2 * (inR ** 2) * (1 - cos(radians(2 * self.angleOff))));
    self.cCircOff = inR - offSpace;
    self.offIncr = self.cCircOff / (steps << 1);
    drawCentreAnim(self, window, self.offIncr);
    
    # binds the circle selecting to the circle
    self.bind("<Button>", lambda event: interactCircle(event, self, self.cCircOff, window));
    