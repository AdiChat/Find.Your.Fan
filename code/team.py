import urllib
import json
import datetime
import geocoder
import requests
import mimetypes
from image import *

access_token = '' # get your own access token for GitHub API

def org_follower_list(username):
    page = 1
    fan = []
    while True:
        url = "https://api.github.com/orgs/{}/members?page={}&per_page=100&access_token={}".format(username, page, access_token)
        r = urllib.urlopen(url).read()
        result = json.loads(r)
        followers = len(result)
        if followers==0:
            break
        page += 1
        count = 0       
        
        while count<followers:
            fan.append(get_user_data(result[count]["login"]))
            count += 1
    print (len(fan))
    return fan

def get_user_data(username):
    url_ = "https://api.github.com/users/{}?access_token={}".format(username, access_token)
    r = urllib.urlopen(url_).read()
    result = json.loads(r)
    return result['id']

def store_follower_list(fans, location):
    with open(location, 'w') as outfile:
        json.dump(fans, outfile, indent=4)
    outfile.close()

def download(fans):
    
    for i in range(0, len(fans)):
   	url = "https://avatars1.githubusercontent.com/u/%s?v=3&s=460" % (str(fans[i]))
	response = requests.get(url)
	content_type = response.headers['content-type']
	extension = mimetypes.guess_extension(content_type)
	if extension==".jpe":
		extension = ".jpg"
	filename = "data/" + str(fans[i]) + extension
	print(extension)
    	urllib.urlretrieve(url, filename)
 
    return 1

if __name__ == "__main__":
    import sys
    
    username = str(sys.argv[1]) 
    
    fans = []
    fans = org_follower_list(username)
    
    store_follower_list(fans, 'data/fans.json')
    download(fans)
    
    create()
    
    print ("completed.")
