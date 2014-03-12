import urllib2
import urllib
import json
import time

api_key = 'ef1b85bdb35b68b0f7ce0f7d6a575c528e600405'

user_data = { 'login':'justin.prather1', 'password':'camerasrule', 
	'api_version':'3'}

print 'Developer Auth'

url = urllib2.urlopen('http://8tracks.com/mixes/new.json?api_key='+api_key+'&api_version=3')
json_response = json.load(url)
print json_response

print 'User Auth'

user_data_encoded = urllib.urlencode(user_data)

user_request = urllib2.Request( 'https://8tracks.com/sessions.json', user_data_encoded)

response = urllib2.urlopen(user_request)

user_json = json.load(response)
print user_json
print user_json[unicode('user')][unicode('user_token')]

print 'Searching mixes'

mixes = urllib2.urlopen('http://8tracks.com/mix_sets/all.json?include=mixes&api_key='
	+api_key+'api_version=3')
json_mixes = json.load(mixes)

for mix in json_mixes[unicode('mix_set')][unicode('mixes')]:
	print mix[unicode('name')]