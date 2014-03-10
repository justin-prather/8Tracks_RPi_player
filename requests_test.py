import urllib2
import urllib
import json
import time

api_key = 'ef1b85bdb35b68b0f7ce0f7d6a575c528e600405'

print 'Developer Auth'

url = urllib2.urlopen('http://8tracks.com/mixes/new.json?api_key='+api_key+'&api_version=3')
json_response = json.load(url)
print json_response

