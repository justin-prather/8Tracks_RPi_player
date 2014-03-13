import urllib2, urllib, json, time

class Gr8_Tracks():

	def __init__(self, api_key, username, password, api_version='3'):
		self.api_key = api_key
		self.username = username
		self.password = password
		self.api_version = api_version

		user_data = {'login':self.username, 
			'password':self.password, 'api_version':self.api_version}

		# dev_auth_url = urllib2.urlopen('http://8tracks.com/mixes/new.json?api_key='
		# 	+api_key+'&api_version='+api_version)

		# dev_auth_json = json.load(dev_auth_json)

		user_data_encoded = urllib.urlencode(user_data)
		user_request = urllib2.Request( 'https://8tracks.com/sessions.json', user_data_encoded)
		user_response = response = urllib2.urlopen(user_request)
		self.user_json = json.load(user_response)

		self.user_token = self.user_json[unicode('user')][unicode('user_token')]

	def search_mix(self, searchType, keys = None, sort = None ):
		base_url_head = 'http://8tracks.com/mix_sets/'
		base_url_tail = '.json?include=mixes&api_key='
			+self.api_key+'api_version='+self.api_version
			
		if searchType is 'all':

		elif searchType is 'tags':

		elif searchType is 'keyword':

		else:

player = Gr8_Tracks( 'ef1b85bdb35b68b0f7ce0f7d6a575c528e600405', 'justin.prather1',
	'camerasrule')