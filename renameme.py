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
		self.configure()
		self.videoDict = self.createDict(directory)
		if (self.mode.lower() == 'movie'):
			self.matchMovie()
		else:
			self.matchTV()
	def configure(self):
		with open("config.yml", "r") as ymlfile:
			self.apikey = yaml.load(ymlfile)['themoviedb']['apikey']
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
	def matchMovie(self):
		self.parseMovieName(self)
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
	def lookupMovie(self):
		for video in self.videoDict:
			params = {
				'query': self.videoDict[video]['parsedTitle'],
				'api_key': self.apikey,
			}
			if ('year' in self.videoDict[video]):
				params['year'] = self.videoDict[video]['year']
			lookup = requests.get('https://api.themoviedb.org/3/search/movie', params=params)
			movieData = lookup.json()
			self.videoDict[video]['matchedTitle'] = movieData['results'][0]['title']
			self.videoDict[video]['year'] = movieData['results'][0]['release_date'].split('-')[0]






### Define Constants ###
videoExtensions = ['mkv', 'mp4', 'avi']