import os
import requests

def createDict(directory = os.getcwd()):
	files = os.listdir(directory)
	videoDict = {}
	for file in files:
		try:
			fileExtension = file.rsplit('.', 1)[1]
			if fileExtension in videoExtensions:
				videoDict[file] = {}
		except IndexError:
				continue
	return videoDict

### Define Constants ###
videoExtensions = ['mkv', 'mp4', 'avi']