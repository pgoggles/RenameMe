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
		self.parseMovieName()
	def parseMovieName(self):
		for video in self.videoDict:
			originalTitle = video
			resolution = re.findall(r"[0-9][0-9][0-9][0-9]p", video)
			if resolution == []:
					resolution = re.findall(r"[0-9][0-9][0-9]p", video)
			if resolution != []:
				video = video.split(resolution[0])[0]
			year = re.findall(r"[0-9][0-9][0-9][0-9]", video)
			if year != []:
				video = video.split(year[0])[0]
				year = year[0]
				self.videoDict[originalTitle]['year'] = year
			video = video.replace('.', ' ')
			video = video.rstrip()
			self.videoDict[originalTitle]['parsedTitle'] = video
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