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
			self.matchVideo(video, mediaInfo)
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
	def matchVideo(self, video, mediaInfo):
		videoInfo = mediaInfo.tracks[self.videoDict[video]['videoTrack']]
		videoCodec = videoInfo.format
		if videoCodec == 'AVC':
			videoCodec = 'H.264'
		elif videoCodec == 'HEVC':
			videoCodec = 'H.265'
		videoWidth = videoInfo.width
		videoHeight = videoInfo.height
		videoResolution = str(videoHeight) + 'p'
		if (videoWidth == 3840 or videoHeight == 2160):
			videoResolution = '2160p'
		elif (videoWidth == 1920 or videoHeight == 1080):
			videoResolution = '1080p'
		elif (videoWidth == 1280 or videoWidth  == 1248 or videoHeight == 720):
			videoResolution = '720p'
		elif (videoHeight == 576 and videoWidth != 1280):
			videoResolution = '576p'
		elif (videoHeight == 480 and videoWidth != 1280):
			videoResolution = '480p'
		elif (videoHeight == 360):
			videoResolution = '360p'
		videoHDR = videoInfo.hdr_format
		if (videoHDR == 'SMPTE ST 2086'):
			videoHDR = 'HDR'
		elif (videoHDR == 'Dolby Vision'):
			videoHDR = 'DV'
		elif (str(videoHDR) == "None" and videoInfo.color_primaries == 'BT.2020'):
			videoHDR = 'HDR'
		elif (str(videoHDR) == "None"):
			videoHDR = ''
		self.videoDict[video]['videoCodec'] = videoCodec
		self.videoDict[video]['videoResolution'] = videoResolution
		self.videoDict[video]['videoHDR'] = videoHDR


### Define Constants ###
videoExtensions = ['mkv', 'mp4', 'avi']