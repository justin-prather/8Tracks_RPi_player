import urllib2, urllib, json, time

class Gr8_Tracks():

	def __init__(self, api_key, username, password, api_version='3'):
		self.api_key = api_key
		self.username = username
		self.password = password
		self.api_version = api_version

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
		base_url_tail = '.json?include=mixes&api_key='+self.api_key+'api_version='+self.api_version

		if searchType is 'all':
			params = 'all'
			if sort is not None:
				params = params + ':' + sort
			if safe is True:
				params = params + ':safe'
			url = base_url_head + params + base_url_tail

		elif searchType is 'tags':
			params = 'tags'
			if keys is not None:
				params = params + ':'
				for i in keys:
					params = params + i + '+'
			params = params[:-1]
			if sort is not None:
				params = params + ':' + sort
			if safe is True:
				params = params + ':safe'
			url = base_url_head + params + base_url_tail

		elif searchType is 'keyword':
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
			if safe is True:
				params = params + ':safe'
			url = base_url_head + params + base_url_tail

		else:
			pass #throw exception

		mixes = urllib2.urlopen( url )
		mixes_json = json.load(mixes)

		return mixes_json

	def get_similar_mix( playtoken=None, mixId=None ):
		if mixId is None:
			mixId = str(self.currentMix_json[unicode('id')])
		if playtoken is None:
			playtoken = self.playtoken
		next_mix = urllib2.urlopen('http://8tracks.com/sets/'+playtoken+'next_mix.json?mix_id='+mixId
			+'api_version='+self.api_version)

		self.next_mix_json = json.load(next_mix)
		return self.next_mix_json


player = Gr8_Tracks( 'ef1b85bdb35b68b0f7ce0f7d6a575c528e600405', 'justin.prather1',
	'camerasrule')

player.search_mix('tags', ['hey', 'you'], 'recent', safe = True)










