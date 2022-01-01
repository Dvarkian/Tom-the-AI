print("Loading ...")

import random
import nltk
from better_profanity import profanity
from nltk.corpus import wordnet
from ioUtils import contains

def contains(string, list_, wholeWord=False): # Returns true if the words iin the list are anywhere in the string.
    from nltk.tokenize import word_tokenize
    
    if wholeWord: # List item must be a entire word in string.
        for i in list_: 
            for s in word_tokenize(string): 
                if i == s:
                    return True
                
    else: # List item can be can be part of a word in string
        for i in list_:
            try:
                if i.lower().strip() in string.lower().strip():
                    return True
            except AttributeError:
                pass
            
    return False # List item was not found in sting.


dir_ = "/".join(__file__.split("/")[:-1])


persons = open(dir_ + "/persons").read().splitlines()
places = open(dir_ + "/places").read().splitlines()
things = open(dir_ + "/things").read().splitlines()
actions = open(dir_ + "/actions").read().splitlines()
nature = open(dir_ + "/nature").read().splitlines()

"""
worldSet = open(dir_ + "/worldSet").read().splitlines()

places = []

for place in worldSet:
    city, country, loc = (place.split(",")[0], place.split(",")[1], place.split(",")[2])

    if country not in places:
        places.append(country)

    places.append(city + " (" + country.capitalize() + ")")

"""

"""
cityList = []
cities = open(dir_ + "/cities15000.txt").read().splitlines()

for city in cities:
    
    try:
        loc = city.split("\t")[1]
        cityList.append(loc)
    except:
        pass
"""
#print(len(cityList), len(maybePlaces))

played = []


def gen(inp):

    valid = False

    while not valid:
        if "action" in inp:
            choice = random.choice(actions)
        elif "person" in inp:
            choice = random.choice(persons)
        elif contains(inp, ["place", "world"]) and contains(inp, ["other"]):
            choice = random.choice(world)
        elif contains(inp, ["place", "world"]):
            choice = random.choice(places)
        elif "nature" in inp:
            choice = random.choice(nature)
        elif contains(inp, ["thing", "object"]):
            choice = random.choice(things)
        else:
            seed = random.randint(0, 4)
            if seed == 0:
                choice = random.choice(actions)
            elif seed == 1:
                choice = random.choice(persons)
            elif seed == 2:
                choice = random.choice(places)
            elif seed == 3:
                choice = random.choice(nature)
            elif seed == 4:
                choice = random.choice(things)

        if profanity.contains_profanity(choice) == 0 and choice not in played:
            valid = True

    if "(" not in choice:
        choice = choice.capitalize()

    played.append(choice)
    return "Your word is '" + choice + "'."



def define(inp):

    inp = inp.split(" ")[-1].strip(" ").strip(".")

    syns = wordnet.synsets(inp)
    
    try:
        out = "'" + inp.capitalize() + "' refers to " + syns[0].definition() + "."
        return out
    
    except:
        return False


def respond(inp):
    inp = inp.lower()
    
    if (contains(inp, ["roll ", "random"]) and
        contains(inp, ["word", "action", "person", "place", "world", "thing", "object", "nature", "all", "AP"])):
        
        out = gen(inp)
        out = "[SECRET] " + out
        return out

    elif contains(inp, ["define ", "definition "]):
        out = define(inp)
        return out

    else:
        return False


if __name__ == "__main__":
    while 1:
        print(gen(input("> ")))
        #print(define(input("> ")))
