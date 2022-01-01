from cleverbot import cleverbot
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize


# With context and session
# An ongoing conversation with the first question as "How are you?"


online = True
try:
    cleverbot("Hello.", ["hi.", "How are you?"], "How are you?")
except ConnectionError:
    online = False

def contains(string, list_, wholeWord=False): # Returns true if the words iin the list are anywhere in the string.
    
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


def getSyns(list_): # Finds synonyms for words in the given list.
    syns = list_ # Add original words to synonym list.
    
    for word in list_: # Iterate through words in list.
        for syn in wordnet.synsets(word): # Get NLTK synonym sets.
            for lemm in syn.lemmas(): # Iterate through synonyms.
                
                if len(syns) >= 20: # Limits no. synonyms. Too great a value will cause lag.
                    break
                
                if lemm.name() in syns:
                    pass # Skip duplicates.
                
                else: # Append synanym to list.
                    syns.append(lemm.name().replace("_", " ").replace("-", " "))        
    return syns # Returns list of synonyms.


def go(inp):
    if not online:
        return False
    
    out = cleverbot(inp, session="How are you?")
    out = out.strip(" ")
    if out[-1] != ".":
        out += "."
    return out
    

def respond(inp):

    if not online:
        return False

    if ((contains(inp.lower(), ["you", "think"]) and not contains(inp, ["yout"])) or
         contains(inp.lower(), ["tom", "day", "they", "we"], wholeWord=True) or
         contains(inp.lower(), getSyns(["hello"]), wholeWord=True) or
         contains(inp.lower(), ["now", "current", "time"])):

        return go(inp)
    
    else:
        return False


if __name__ == "__main__":
    while True:
        print(respond(input("> ")))
