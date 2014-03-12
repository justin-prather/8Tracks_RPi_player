import urllib2, urllib, json, time

class Gr8_Tracks():

	def __init__(self, api_key, username, password):
		self.api_key = api_key
		self.username = username
		self.password = password