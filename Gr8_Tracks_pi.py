import urllib2, urllib, json, time
import vlc
import RPi.GPIO as gpio

class Gr8_Tracks():

	currentMix_json = None
	next_mix_json = None
	current_song = None
	next_song = None
	vlc_player = None
	at_end = False

	def __init__(self, api_key, username, password, safe=False, api_version='3'):
		self.api_key = api_key
		self.username = username
		self.password = password
		self.api_version = api_version
		self.safe = safe

		user_data = {'login':self.username, 
			'password':self.password, 'api_version':self.api_version}

		user_data_encoded = urllib.urlencode(user_data)
		user_request = urllib2.Request( 'https://8tracks.com/sessions.json', user_data_encoded)
		user_response = response = urllib2.urlopen(user_request)
		self.user_json = json.load(user_response)

		self.user_token = self.user_json[unicode('user')][unicode('user_token')]


	def get_play_token(self):
		playtoken_url = urllib2.urlopen('http://8tracks.com/sets/new.json?api_key='+self.api_key
			+'api_version='+self.api_version)

		self.playtoken_json = json.load(playtoken_url)
		self.playtoken = self.playtoken_json[unicode('play_token')]

		return self.playtoken

	def search_mix(self, searchType, keys = None, sort = None, safe = False ):
		base_url_head = 'http://8tracks.com/mix_sets/'
		base_url_tail = '.json?include=mixes&api_key='+self.api_key+'&api_version='+self.api_version

		if searchType == 'all':
			params = 'all'
			if sort is not None:
				params = params + ':' + sort
			if safe is True or self.safe is True:
				params = params + ':safe'
			url = base_url_head + params + base_url_tail

		elif searchType == 'tags':
			params = 'tags'
			if keys is not None:
				params = params + ':'
				for i in keys:
					params = params + i + '+'
			params = params[:-1]
			if sort is not None:
				params = params + ':' + sort
			if safe is True or self.safe is True:
				params = params + ':safe'
			url = base_url_head + params + base_url_tail

		elif searchType == 'keyword':
			if keys is None:
				pass #throw exception
			params = 'keyword'
			if keys is not None:
				params = params + ':'
				for i in keys:
					params = params + i + '+'
			params = params[:-1]
			if sort is not None:
				params = params + ':' + sort
			if safe is True or self.safe is True:
				params = params + ':safe'
			url = base_url_head + params + base_url_tail

		else:
			pass #throw exception

		mixes = urllib2.urlopen( url )
		mixes_json = json.load(mixes)

		return mixes_json

	def get_similar_mix( self, playtoken=None, mixId=None ):
		if mixId is None:
			mixId = self.currentMix_json[unicode('id')]
		if playtoken is None:
			playtoken = self.playtoken

		next_mix = urllib2.urlopen('http://8tracks.com/sets/'+str(playtoken)+'/next_mix.json?api_key='+self.api_key+'&mix_id='+str(mixId))

		next_mix_json = json.load(next_mix)
		
		return next_mix_json[unicode('next_mix')]

	def get_first_song(self):
		if self.currentMix_json is None:
			pass #throw error

		mixId = self.currentMix_json[unicode('id')]
		mixUrl = ('http://8tracks.com/sets/'+str(self.playtoken)+'/play.json?mix_id='
			+str(self.currentMix_json[unicode('id')])+'&api_key='+str(self.api_key)+'&api_version='+str(self.api_version))

		stream_url = urllib2.urlopen(mixUrl)

		self.current_song = json.load(stream_url)

		return self.current_song

	def get_next_song(self):
		if self.currentMix_json is None:
			pass #throw error

		mixId = self.currentMix_json[unicode('id')]
		mixUrl = ('http://8tracks.com/sets/'+str(self.playtoken)+'/next.json?mix_id='
			+str(self.currentMix_json[unicode('id')])+'&api_key='+str(self.api_key)+'&api_version='+str(self.api_version))

		stream_url = urllib2.urlopen(mixUrl)

		self.next_song = json.load(stream_url)

		return self.next_song

	def callback(self, event):
		self.at_end = True

	def play_song(self):
		if self.vlc_player is None:
			i = vlc.Instance()
			self.vlc_player = vlc.MediaPlayer(i,'')

		url = self.current_song[unicode('set')][unicode('track')][unicode('track_file_stream_url')].encode('utf-8')
		if 'https' in url:
			url = url.replace('https', 'http')

		m = vlc.Media(url)
		self.vlc_player.set_media(m)

		self.vlc_player.play()

	def play_mix(self):
		self.get_first_song()

		self.play_song()

		manager = self.vlc_player.event_manager()
		manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.callback)

		self.get_next_song()
		print self.current_song[unicode('set')][unicode('track')][unicode('track_file_stream_url')].encode('utf-8')

		while True:
			
			if not gpio.input(27):
				while not gpio.input(27):
					pass
				print 'Toggle pause'
				self.vlc_player.pause()
			if not gpio.input(22):
				print 'Exiting'
				self.vlc_player.stop()
				import sys
				sys.exit(0)

			if self.at_end or not gpio.input(18):
				if self.current_song[u'set'][u'at_end'] is True:
					print 'End of mix'
					break
				self.at_end = False
				self.current_song = self.next_song
				self.play_song()
				self.get_next_song()
				print self.current_song[unicode('set')][unicode('track')][unicode('track_file_stream_url')].encode('utf-8')


if __name__ == '__main__':
	gpio.setmode(gpio.BCM)
	gpio.setup(22, gpio.IN, pull_up_down=gpio.PUD_UP)
	gpio.setup(27, gpio.IN, pull_up_down=gpio.PUD_UP)
	gpio.setup(18, gpio.IN, pull_up_down=gpio.PUD_UP)

	player = Gr8_Tracks( 'ef1b85bdb35b68b0f7ce0f7d6a575c528e600405', 'justin.prather1',
			     'camerasrule')

	print player.get_play_token()

	search_results = player.search_mix('tags', ['edm', 'party'], 'recent')

	for i in range(0,len(search_results[unicode('mix_set')][unicode('mixes')])):
		print str(i) + ') ' + search_results[unicode('mix_set')][unicode('mixes')][i][unicode('name')].encode('utf-8')

	print 'Enter mix number:'
	player.currentMix_json = search_results[unicode('mix_set')][unicode('mixes')][int(raw_input())]

	player.play_mix()

