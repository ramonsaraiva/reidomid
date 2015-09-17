import requests
import json
import sys

from requests.auth import HTTPBasicAuth

BASE_URL = 'http://localhost:5000/api'
HEADERS_JSON = {'Content-Type': 'application/json'}

def post(url, data):
	return requests.post('{0}{1}'.format(BASE_URL, url), data=json.dumps(data), headers=HEADERS_JSON, auth=HTTPBasicAuth('ramon', 'ramon'))

def get(url):
	return requests.get('{0}{1}'.format(BASE_URL, url))

if __name__ == '__main__':
	if sys.argv[1] == 'create':
		data = {'name': sys.argv[2]}
		r = post('/summoners/', data)
		print(r.text)

	elif sys.argv[1] == 'summoners':
		print(get('/summoners/').text)

	elif sys.argv[1] == 'verificate':
		print(post('/summoners/{0}/verification/'.format(sys.argv[2]), {}).text)
