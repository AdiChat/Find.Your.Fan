import urllib.request
import json

access_token = '' # get your own access token for GitHub API

def follower_list(username):
    url = "https://api.github.com/users/{}/followers?access_token={}".format(username, access_token)
    r = urllib.request.urlopen(url).read()
    result = json.loads(r)
    print (len(result))
    followers = len(result)
    count = 0
    stargazers = []
    
    while count<followers:
        stargazers.append(result[count]["login"])
        count += 1
    return stargazers

if __name__ == "__main__":
    import sys
    
    username = str(sys.argv[1])  
    stargazers = follower_list(username)
    print ("completed.")