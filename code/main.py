import urllib.request
import json
import datetime
import geocoder

access_token = '' # get your own access token for GitHub API

def follower_list(username):
    page = 1
    fans = []
    while True:
        url = "https://api.github.com/users/{}/followers?page={}&per_page=100&access_token={}".format(username, page, access_token)
        r = urllib.request.urlopen(url).read()
        result = json.loads(r)
        followers = len(result)
        if followers==0:
            break
        page += 1
        count = 0    
        while count<followers:
            fans.append(result[count]["login"])
            count += 1
    return fans

def org_follower_list(username):
    page = 1
    fan = []
    while True:
        url = "https://api.github.com/orgs/{}/members?page={}&per_page=100&access_token={}".format(username, page, access_token)
        r = urllib.request.urlopen(url).read()
        result = json.loads(r)
        followers = len(result)
        if followers==0:
            break
        page += 1
        count = 0       
        
        while count<followers:
            fan.append(result[count]["login"])
            count += 1
    print (len(fan))
    return fan

def fork_list(username, reponame):
    page = 1
    fan = []
    while True:
        url = "https://api.github.com/repos/{}/{}/forks?page={}&per_page=100&access_token={}".format(username, reponame, page, access_token)
        r = urllib.request.urlopen(url).read()
        result = json.loads(r)
        followers = len(result)
        if followers==0:
            break
        page += 1
        count = 0       
        
        while count<followers:
            fan.append(result[count]["owner"]["login"])
            count += 1
    print (len(fan))
    return fan

def star_list(username, reponame):
    page = 1
    fan = []
    while True:
        url = "https://api.github.com/repos/{}/{}/stargazers?page={}&per_page=100&access_token={}".format(username, reponame, page, access_token)
        r = urllib.request.urlopen(url).read()
        result = json.loads(r)
        followers = len(result)
        if followers==0:
            break
        page += 1
        count = 0       
        
        while count<followers:
            fan.append(result[count]["login"])
            count += 1
    print (len(fan))
    return fan


def get_user_data(username):
    url_ = "https://api.github.com/users/{}?access_token={}".format(username, access_token)
    r = urllib.request.urlopen(url_).read()
    result = json.loads(r)
    return result['location'], result['id']

def get_locations_of_fans(fans):

    data = {'users': []}

    for user in fans:
        user_country, user_id = get_user_data(user)

        if user_country == "N/A":
            pass
        else:
            user_country = geocoder.google(user_country).country_long
            if user_country:
                user_ = {"user": user_id, "country": user_country}
                data["users"].append(user_)
                print ("A fan from " + user_country)

    return data

def write_in_js_file(location_data, location):
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)

    with open(location, "w") as js_file:
        js_file.write("var data = { users:")
        js_file.write(str(location_data["users"]))
        js_file.write(", created_at: new Date(%s, %s, %s) };" % (year, month, day))

    js_file.close()

def store_follower_list(fans, location):
    with open(location, 'w') as outfile:
        json.dump(fans, outfile, indent=4)
    outfile.close()

if __name__ == "__main__":
    import sys
    
    username = str(sys.argv[1]) 
    user_type = 0
    repo_name = ""
    print (len(sys.argv))
    if len(sys.argv) == 4:
        repo_name = str(sys.argv[2])
        user_type = int(sys.argv[3])
    elif len(sys.argv) == 3:
        user_type = int(sys.argv[2])
    fans = []
    if user_type == 0:
        fans = follower_list(username)
    elif user_type == 1:
        fans = org_follower_list(username)
    elif user_type == 2:
        fans = fork_list(username, repo_name) 
    else:
        fans = star_list(username, repo_name) 
    store_follower_list(fans, 'data/fans.json')
    location_data = get_locations_of_fans(fans)
    write_in_js_file(location_data, 'js/fans.js')

    print ("completed.")