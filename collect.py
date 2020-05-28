import wget
import os
import jsbeautifier
import sys
import hashlib
import signal
import time


signs = ["hash", "identifier", "userid", "beacon", "ad.js", "webgl_debug_rendered_info", "getdataurl", "oscillator"]
score = [6, 4, 6, 6, 8, 9, 4, 12]
count = 0


def handler(signum, frame):
	raise IOError("Timeout")


def getHash(fileName):
	BLOCKSIZE = 65536
	hasher = hashlib.md5()
	with open(fileName, 'rb') as f:
		buf = f.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = f.read(BLOCKSIZE)
		f.flush()
		f.close()
	return hasher.hexdigest()


def checkHash(h):
	with open('hashes.txt', 'rb') as f:
		for line in f:
			if line.count(h) > 0:
				f.flush()
				f.close()
				return True
		f.flush()
		f.close()
		return False

		
def addDuplicate(x):
	with open('duplicate.txt', 'a') as f:
		f.write("%s\n" % x)	


def addHash(h):
	with open('hashes.txt', 'a') as f:
		f.write("%s\n" % h)	


def addFailed(x):
	with open('fails.txt', 'a') as f:
		f.write("%s\n" % x)


def getRawCount():
	count = 0
	for i in range(len(signs)):
		with open('current.txt', 'rb') as f:
			lineCount = 0 
			for line in f:
				line = line.lower()
				lineCount += line.count(signs[i])
			if lineCount > 0:
				count += score[i]
			f.flush()
			f.close()
	return count


def main():
	fileLink = sys.argv[1]
	start = time.time()
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(60)
	try:
		fileName = wget.download(fileLink, bar=None)
	except (ValueError, IOError) as e:
		addFailed(fileLink)
		return None
	h = getHash(fileName)
	if (checkHash(h)):
		addDuplicate(fileLink)
		os.remove(fileName)
		return None
	else:
		addHash(h)
		with open('current.txt', 'w') as f:
			f.write(jsbeautifier.beautify_file(fileName).encode('ascii',errors='ignore'))
			f.flush()
			f.close()
		with open('current.txt', 'rb') as f:
			f.flush()
			f.close()
			count = getRawCount()	
			os.remove(fileName)
			print(count)
			print(fileLink)
			return count, fileLink

main()
