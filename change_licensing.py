
import config
import flickrapi
import webbrowser

def main():
	
	flickr = flickrapi.FlickrAPI(config.API_KEY, config.SECRET)
	
	print('Step 1: authenticate')
	# Get a request token
	flickr.get_request_token(oauth_callback='oob')

	# Open a browser at the authentication URL
	authorize_url = flickr.auth_url(perms='write')
	webbrowser.open_new_tab(authorize_url)

	# Get the verifier code from the user
	verifier = str(input('Verifier code: '))

	# Trade the request token for an access token
	flickr.get_access_token(verifier)

	
if __name__ == '__main__':
    main()
