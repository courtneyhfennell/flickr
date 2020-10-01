
import config
import webbrowser
import requests
from requests_oauthlib import OAuth1
from oauthlib.common import urldecode


def main():
	flickr = "https://www.flickr.com/services"
	REQUEST_TOKEN_URL = "https://www.flickr.com/services/oauth/request_token"
	AUTHORIZE_URL = "https://www.flickr.com/services/oauth/authorize"
	ACCESS_TOKEN_URL = "https://www.flickr.com/services/oauth/access_token"
	SET_LICENSE_URL = "https://www.flickr.com/services/rest/?method=flickr.photos.licenses.setLicense"
	
		
	print('Step 1: authenticate')
	# Get a request token
	oauth = OAuth1(config.API_KEY, config.SECRET)
	tokencache.SimpleTokenCache()
	
	fetch_response = requests.post(REQUEST_TOKEN_URL, data={'oauth_callback':'oob'}, auth=oauth)
	token = dict(urldecode(fetch_response.text.strip()))
	
	print(token)

	# Open a browser at the authentication URL
	authorize_url = "%s?oauth_token=%s&perms=%s" % (AUTHORIZE_URL, token['oauth_token'], 'write')
	webbrowser.open_new_tab(authorize_url)

	# Get the verifier code from the user
	verifier = str(input('Verifier code: '))

	# Trade the request token for an access token
	oauth = OAuth1(config.API_KEY,
                   config.SECRET,
                   resource_owner_key=token['oauth_token'],
                   resource_owner_secret=token['oauth_token_secret'],
                   verifier=verifier)
				   
	fetch_response = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
	resp = dict(urldecode(fetch_response.text.strip()))
	print(resp)
	OWNER_KEY = resp['oauth_token']
	OWNER_SECRET = resp['oauth_token_secret']

	'''
	&api_key=8871c6f05ca8b9d979c6fc97191fa999
	&photo_id=17025391635
	&license_id=2
	&format=json
	&nojsoncallback=1
	&auth_token=72157716197517768-361e56335c210b2b
	&api_sig=86424d7dea0e6312417496035687a89d'''

	
if __name__ == '__main__':
    main()
