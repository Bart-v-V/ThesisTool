import os
import sys


calls = ["navigator.platform", "navigator.cookieenabled", "date.timezoneoffset", "navigator.javaenabled", "window.localstorage", "window.sessionstorage"]
score = [6, 4, 1, 4, 2, 2]

battery = ["battery.charging", "battery.level", "battery.chargingtime", "battery.dischargingtime", "navigator.getbattery"]
batteryScore = 12
resolution = ["screen.width", "screen.height", "screen.colordepth"]
resolutionScore = 4
plugins = ["navigator.plugins", "plugins.name", "plugins.length", "plugins.description"]
pluginsScore = 7
mimetype = ["navigator.mimetypes", "mimetypes.enabledplugin", "mimetypes.description", "mimetype.type"]
mimetypeScore = 6
track = ["navigator.donottrack", "navigator.msdonottrack"]
trackScore = 8

def getAstCount():
	count = int(sys.argv[1])
	for i in range(len(calls)):
		with open('current.txt.exp', 'rb') as f:
			lineCount = 0 
			for line in f:
				line = line.lower()
				lineCount += line.count(calls[i])
			if lineCount > 0:
				count += score[i]
			f.flush()
			f.close()


	intermediateCount = 0 
	for i in range(len(battery)):
		with open('current.txt.exp', 'rb') as f:
			lineCount = 0
			for line in f:
				line = line.lower()
				lineCount += line.count(battery[i])
				if lineCount > 0:
					intermediateCount += 1
			f.flush()
			f.close()
	if intermediateCount > 0:
		count += batteryScore


	intermediateCount = 0 
	for i in range(len(resolution)):
		with open('current.txt.exp', 'rb') as f:
			lineCount = 0
			for line in f:
				line = line.lower()
				lineCount += line.count(resolution[i])
				if lineCount > 0:
					intermediateCount += 1
			f.flush()
			f.close()
	if intermediateCount == len(resolution):
		count += resolutionScore


	intermediateCount = 0 
	for i in range(len(plugins)):
		with open('current.txt.exp', 'rb') as f:
			lineCount = 0
			for line in f:
				line = line.lower()
				lineCount += line.count(plugins[i])
				if lineCount > 0:
					intermediateCount += 1
			f.flush()
			f.close()
	if intermediateCount > 0:
		count += pluginsScore


	intermediateCount = 0 
	for i in range(len(mimetype)):
		with open('current.txt.exp', 'rb') as f:
			lineCount = 0
			for line in f:
				line = line.lower()
				lineCount += line.count(mimetype[i])
				if lineCount > 0:
					intermediateCount += 1
			f.flush()
			f.close()
	if intermediateCount > 0:
		count += mimetypeScore


	intermediateCount = 0 
	for i in range(len(track)):
		with open('current.txt.exp', 'rb') as f:
			lineCount = 0
			for line in f:
				line = line.lower()
				lineCount += line.count(track[i])
				if lineCount > 0:
					intermediateCount += 1
			f.flush()
			f.close()
	if intermediateCount > 0:
		count += trackScore


	return count


def addFinger(f):
	with open('finger.txt', 'a') as x:
		x.write("%s\n" % f)


def addNoFinger(f):
	with open('noFinger.txt', 'a') as x:
		x.write("%s\n" % f)


def main():
	link = sys.argv[2]
	threshold = 17
	lineCount = 0
	count = getAstCount()
	print ("final count: " + str(count))
	if count > threshold:
		addFinger(link)
	else:
		addNoFinger(link)
	return

main()
