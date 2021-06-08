import os
import requests
import re
import json
import yaml

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

def parseMovieName(videoDict):
	for video in videoDict:
		originalTitle = video
		# Try to split title based on resolution#
		resolution = re.findall(r"[0-9][0-9][0-9][0-9]p", video)
		if resolution == []:
				resolution = re.findall(r"[0-9][0-9][0-9]p", video)
		if resolution != []:
			video = video.split(resolution[0])[0]
		#Try to split title based on year#:
		year = re.findall(r"[0-9][0-9][0-9][0-9]", video)
		if year != []:
			video = video.split(year[0])[0]
			year = year[0]
			videoDict[originalTitle]['year'] = year
		#Replace spaces in filename#
		video = video.replace('.', ' ')
		video = video.rstrip()
		videoDict[originalTitle]['parsedTitle'] = video
	return videoDict



### Define Constants ###
videoExtensions = ['mkv', 'mp4', 'avi']