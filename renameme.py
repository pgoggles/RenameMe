import os
import requests
import re
import json
import yaml
from pymediainfo import MediaInfo

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
		self.lookupMovie()
		self.mediaInfoLookup()
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
	def mediaInfoLookup(self):
		for video in self.videoDict:
			mediaInfo = MediaInfo.parse(video)
			for i in range (len(mediaInfo.tracks)):
					if mediaInfo.tracks[i].track_type == 'Video' and 'videoTrack' not in self.videoDict[video]:
						self.videoDict[video]['videoTrack'] = i
					elif  mediaInfo.tracks[i].track_type == 'Audio' and 'audioTrack' not in self.videoDict[video]:
						self.videoDict[video]['audioTrack'] = i
			self.matchAudio(video, mediaInfo)
	def matchAudio(self, video, mediaInfo):
			audioInfo = mediaInfo.tracks[self.videoDict[video]['audioTrack']]
			audioCodec = audioInfo.commercial_name
			audioChannels = audioInfo.channel_s
			audioExtended = ''
			if audioChannels == 8:
				audioChannels = '7.1'
			if audioChannels == 6:
				audioChannels = '5.1'
			elif audioChannels == 2:
				audioChannels = '2.0'
			if audioCodec == 'Dolby Digital Plus with Dolby Atmos':
				audioCodec = 'DDP'
				audioExtended = 'Atmos'
			elif audioCodec == 'Dolby Digital Plus':
				audioCodec = 'DDP'
			elif audioCodec == 'Dolby Digital':
				audioCodec = 'DD'
			self.videoDict[video]['audioChannels'] = audioChannels
			self.videoDict[video]['audioCodec'] = audioCodec
			self.videoDict[video]['audioExtended'] = audioExtended

### Define Constants ###
videoExtensions = ['mkv', 'mp4', 'avi']