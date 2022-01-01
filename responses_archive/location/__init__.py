import requests
import json

def respond(inp):

    if ("loca" in inp or "coord" in inp or "co-ord" in inp) and "my" in inp:
        
        send_url = "http://api.ipstack.com/check?access_key=aafa3f03dc42cd4913a79fd2d9ce514d"
        geo_req = requests.get(send_url)
        geo_json = json.loads(geo_req.text)
        
        latitude = geo_json['latitude']
        latitude = str(latitude)
        
        longitude = geo_json['longitude']
        longitude = str(longitude)
        
        city = geo_json['city']
        #continent_name = geo_json['continent_name']
        country_name = geo_json['country_name']
        
        pin = geo_json['zip']
        pin = str(pin)
        
        out = 'Your coordinates are (' + latitude[:6] + ", " + longitude[:6] + '), in ' + city + " " + pin + ", " + country_name + "."
        
        return out

    else:
        return False

if __name__ == "__main__":
    while True:
        print(respond(input("> ")))
