
dir_ = "/".join(__file__.split("/")[:-1]) + "/responses/memory"

import random

from ioUtils import *
    
try:
    file = open(dir_ + "/knowledgeBase.txt", "x")
    knowledge = []
except:
    knowledge = open(dir_ + "/knowledgeBase.txt").read().splitlines()


def resp(inp):
    global knowledge

    inp = inp.lower()

    if "is" in inp:
        foc = "is "
    else:
        foc = "are "
    
    if contains(inp, ["what " + foc, "where " + foc, "who " + foc, "when " + foc]):
        
        topic = inp.split(foc)[1].strip().replace(".", "").replace("?", "")

        for fact in knowledge:
            if topic in fact:
                return fact.capitalize()
        else:
            return False

    elif (contains(inp, ["is", "are"]) and not
          contains(inp, ["where", "who", "what", "when", "how", "why", "?"])):

        try:
            topic = inp.split(foc)[1].strip().replace(".", "")
        except:
            return False

        for fact in range(0, len(knowledge)):
            if topic in knowledge[fact]:
                knowledge = list(knowledge[:fact]) + [inp] + knowledge[fact+1:]

                with open(dir_ + "/knowledgeBase.txt", "w") as file:
                    for data in knowledge:
                        file.write(data + "\n")
                break

        else:
            
            with open(dir_ + "/knowledgeBase.txt", "a") as file:
                file.write(inp + "\n")

        return affirm()

    else:
        return False


def respond(inp):

    out = resp(inp)
    
    if ((contains(inp.lower(), [" is ", " are "]) and
        (out != False and isQuestion(inp)) and
        not contains(inp, ["you", "we"]))):

        return out

    else:
        return False


if __name__ == "__main__":
    while 1:
        print(respond(input("> ")))










        
