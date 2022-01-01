import pyjokes
from ioUtils import *

def respond(inp):
    if (contains(inp.lower(), getSyns(["joke", "funny"]))): # Respond with a joke from PyJokes database.
        out = pyjokes.get_joke()
        return out
    else:
        return False
