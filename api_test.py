# This file is meant as a script to test the API
import requests

def register(name, email, api_url="https://csaar.herokuapp.com"):
    payload = {'name':name, 'email':email}
    r = requests.post("%s%s" % (api_url, "/register/"), data=payload)
    if r.status_code == 200:
        j = r.json()
        if j.get("error") == 'Already Exists':
            print "Logged in user with ID %d" % j['UserID']
        else:
            print "Created user with ID %d" % j['UserID']
        return j['UserID']
    else:
        raise LookupError

def rate(user_id, fiducial_id, rating, api_url="https://csaar.herokuapp.com"):
    url = "%s/fn/%s/rate/%d/%s/" % (api_url, fiducial_id, user_id, rating)
    #print url
    r = requests.get(url)
    if r.status_code == 200:
        print "Rated the fiducial, current rating is %f", r.json()['total_rating']
    else:
        raise LookupError
        
if __name__=='__main__':
    print("Registration:")
    name = str(raw_input("What is your name: "))
    email = str(raw_input("What is your email: "))
    uid = register(name, email)
    while True:
        fid = str(raw_input("What's the name of the fiducial you want to rate: "))
        rating = str(raw_input("Give it a rating 1-5: "))
        rate(uid, fid, rating)
    