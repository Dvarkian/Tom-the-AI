

from googlesearch.googlesearch import GoogleSearch
import random
from ioUtils import contains


def findProb(inp): # Get webernet results for a given input

    if "that " in inp:
        inp = inp.split("that ")[1].replace("?", "").replace(".", "")
    elif "of " in inp:
        inp = inp.split("of ")[1].replace("?", "").replace(".", "")
    else:
        inp = inp.replace("?", "").replace(".", "")
    
    anti = ""
    inp = inp.replace("won't", "will not")

    if "not " in inp:
        anti = inp.relpace("not ", "")
    else:
        keywords = ["is", "am", "will", "are", "was"]

        for k in keywords:
            if k in inp:
                anti = inp.replace(k, k + " not")
                break
            
    try:
        response = GoogleSearch().search("\"" + inp + "\"")
        pos = response.total

        response = GoogleSearch().search("\"" + anti + "\"")
        neg = response.total
        
    except:
        response = GoogleSearch().search(inp)
        pos = response.total

        response = GoogleSearch().search(anti)
        neg = response.total

    if int((pos*100) / (pos + neg)) == 0:
        return random.choice(["How should I know?", "Give me a bagel and I'll tell you :).", "Sorry pal, not a clue.",
                              "If you find out, tell me.", "I calculate the probability as a grand total of I have no idea.",
                              "I could tell  you, but you wouldn't like the answer.", "Trust me, you don't want to know.",
                              "Hey look, a wierd bug."])

    ps = str((pos*100) / (pos + neg))[:min(6, len(str((pos*100) / (pos + neg))))].strip(".") + random.choice(["%", " percent."])

    out = random.choice(["I calculate the probability as ",
                         "The probability that " + inp + " is ",
                         "I calculate a chance of ",
                         "By my calculation, the chance that " + inp + " is "])

    out += random.choice([" ", "exactly ", "precicely ", "around ", "about ", "around about ", "approximately ",
                          "somewhere in the vicinity of "])

    out += ps

    return out


def respond(inp):
    if (contains(inp.lower(), ["probability", "chance", "how likely"]) and contains(inp.lower(), [" of ", " that "])):
            
        out = findProb(inp)
        return out
    
    else:
        return False
    

if __name__ == "__main__":
    while 1:
        print(respond(input("> ")))
