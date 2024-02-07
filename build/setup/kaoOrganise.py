import random
import win32api as wapi, win32con as wcon
import urllib.request as ulib
import os
import kaoCat as dat

kaomojiDatabase = "http://kaomoji.ru/en/";
kaomojisFile = "kaomojis.txt";
NOT_KAOMOJI = "not kaomoji";

# it's like clicking but dragging
def drag(x1, y1, x2, y2):
	wapi.SetCursorPos((x1, y1));
	wapi.mouse_event(wcon.MOUSEEVENTF_LEFTDOWN, 0, 0);
	wapi.SetCursorPos((x2, y2));
	wapi.mouse_event(wcon.MOUSEEVENTF_LEFTUP, 0, 0);

################################ STAGE 1 ################################

# helper to extract the Kaomoji data
def extractHtmlData(line):
	cleanLine = line.decode("utf-8"); # decode that shit
	cleanLine = cleanLine.lstrip().rstrip(); # clean up whitespace

	htmlGarb = ["<td><span>", "</span></td>"];
	if cleanLine.startswith(htmlGarb[0]):
		cleanLine = cleanLine.replace("\n", "");
		cleanLine = cleanLine.removeprefix(htmlGarb[0]);
		cleanLine = cleanLine.removesuffix(htmlGarb[1]);

		return cleanLine;
	else:
		return NOT_KAOMOJI;

# Converts HTML Kaomojis to human-friendly data
def webpToFile(url):
	# grab HTML of Kaomoji website
	webp = ulib.urlopen(url);
	kaomojis = webp.readlines();

	with open(kaomojisFile, "w+", encoding = "utf-8") as wFile:
		for dataLine in kaomojis:
			cleanLine = extractHtmlData(dataLine);
			if cleanLine == NOT_KAOMOJI or cleanLine == "": continue;

			wFile.write(cleanLine + "\n");

################################ STAGE 2 ################################

# importing variables
pos = dat.pos;
neg = dat.neg;
neu = dat.neu;
varAct = dat.varAct;
animals = dat.animals;
other = dat.other;

all = {
	"Positive Emotions": pos,
	"Negative Emotions": neg,
	"Neutral Emotions": neu,
	"Various Actions": varAct,
	"Animals": animals,
	"Other Types": other
};

# files and directory paths
ALL_KAOMOJIS = "./All Kaomojis";

# checks if file exists before mkdir
def cleanMkdir(path):
	if not os.path.exists(path): os.mkdir(path);

# given a category with KaoTypes and the number of Kaomojis, we will write the Kaomojis into the files
def writeKaoFile(category, currCatPath, rFile):
	for kaoType, kaoNum in category.items():
		currFilePath = currCatPath + "/" + kaoType + ".txt";
		with open(currFilePath, "w+", encoding = "utf-8") as kaoFile:
			for i in range(kaoNum): kaoFile.write(rFile.readline());

# well duh, it organises the Kaomojis
def organiseKaomojis(filepath, all):
	with open(filepath, "r", encoding = "utf-8") as rFile:
		cleanMkdir(ALL_KAOMOJIS);
		
		for name, category in all.items():
			currCatPath = ALL_KAOMOJIS + "/" + name;
			cleanMkdir(currCatPath);
			writeKaoFile(category, currCatPath, rFile);

################################-#-##-#-################################
################################  MAIN  ################################
################################-#-##-#-################################

# Stage 1: grab the URL and filter out the Kaomojis into a big file
webpToFile(kaomojiDatabase);

# Stage 2: organise the big file into files
organiseKaomojis(kaomojisFile, all);
