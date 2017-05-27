import urllib.request
import json
import datetime
import geocoder

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

def get_user_data(username):
    url_ = "https://api.github.com/users/{}?access_token={}".format(username, access_token)
    r = urllib.request.urlopen(url_).read()
    result = json.loads(r)
    return result['location'], result['id']

def get_locations_of_fans(stargazers):

    data = {'users': []}

    for user in stargazers:
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

def write_in_js_file(location_data):
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)

    with open("data/stargazers.js", "w") as js_file:
        js_file.write("var data = { users:")
        js_file.write(str(location_data["users"]))
        js_file.write(", created_at: new Date(%s, %s, %s) };" % (year, month, day))

    js_file.close()

if __name__ == "__main__":
    import sys
    
    username = str(sys.argv[1])  
    stargazers = follower_list(username)
    location_data = get_locations_of_fans(stargazers)
    write_in_js_file(location_data)

    print ("completed.")