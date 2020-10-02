
import config
import webbrowser
import requests
from requests_oauthlib import OAuth1
from oauthlib.common import urldecode
import os
import json

def save_token_to_file(OWNER_KEY, OWNER_SECRET):
    with open('./config.py', 'a') as f:
        f.write(f"\nOWNER_KEY = '{OWNER_KEY}'\n")
        f.write(f"OWNER_SECRET = '{OWNER_SECRET}'\n")

def get_token():
    # imaginary API call to get token
    flickr = "https://www.flickr.com/services"
    REQUEST_TOKEN_URL = "https://www.flickr.com/services/oauth/request_token"
    AUTHORIZE_URL = "https://www.flickr.com/services/oauth/authorize"
    ACCESS_TOKEN_URL = "https://www.flickr.com/services/oauth/access_token"
    SET_LICENSE_URL = "https://www.flickr.com/services/rest/?method=flickr.photos.licenses.setLicense"

    # Get a request token
    oauth = OAuth1(config.API_KEY, config.SECRET)

    fetch_response = requests.post(REQUEST_TOKEN_URL, data={'oauth_callback':'oob'}, auth=oauth)
    token = dict(urldecode(fetch_response.text.strip()))

    # Open a browser at the authentication URL
    authorize_url = "%s?oauth_token=%s&perms=%s" % (AUTHORIZE_URL, token['oauth_token'], 'write')
    webbrowser.open_new_tab(authorize_url)

    # Get the verifier code from the user
    verifier = str(input('Verifier code: '))

    # Trade the request token for an access token
    oauth = OAuth1(config.API_KEY,
                   config.API_SECRET,
                   resource_owner_key=token['oauth_token'],
                   resource_owner_secret=token['oauth_token_secret'],
                   verifier=verifier)

    fetch_response = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    resp = dict(urldecode(fetch_response.text.strip()))
    
    save_token_to_file(resp['oauth_token'], resp['oauth_token_secret'])
    return (resp['oauth_token'], resp['oauth_token_secret'])


def main():
    # Try to get the owner key and secret from the config file, otherwise call the API
    try:
        OWNER_KEY = config.OWNER_KEY
        OWNER_SECRET = config.OWNER_SECRET
    except AttributeError:
        OWNER_KEY, OWNER_SECRET = get_token()
        
    # queryoauth = OAuth1(config.API_KEY, config.API_SECRET,
                        # OWNER_KEY, OWNER_SECRET,
                        # signature_type='query')
    # r = requests.get(url, auth=queryoauth)


if __name__ == '__main__':
    main()
