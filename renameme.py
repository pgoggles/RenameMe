import os
import requests
import re
import json
import yaml

class RenameMe ():
	def __init__(self, mode, formatString = None, directory = os.getcwd()):
		self.mode = mode
		self.formatString = formatString
		self.directory = directory
		self.videoDict = self.createDict(directory)
		if (self.mode.lower() == 'movie'):
			self.videoDict = self.parseMovieName(self.videoDict)
	def createDict(self, directory):
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
	def parseMovieName(self, videoDict):
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