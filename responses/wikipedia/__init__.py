import wikipedia


def isQuestion(inp): # Identifies if an input is a quenton.
    # Note: quention mark is deliberatelty ommitted as some formatting / encoding styles use this for an unrecognissed character.
    
    inp = inp.lower().strip() # Format input
    
    if (inp.startswith("who") or inp.startswith("what") or inp.startswith("when") or inp.startswith("which") or
        inp.startswith("how") or inp.startswith("why") or inp.startswith("where")):
        return True # Input was a question.
    
    return False # Input was not a question.



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


def respond(inp):
    if ((isQuestion(inp.lower()) and not contains(inp.lower(), ["there"])) or contains(inp.lower(), ["wiki"])
        and not contains(inp.lower(), [" you", "you "])): # Get an objective respense from the web.
        
        try:

            if "the " in inp:
                inp = inp.split("the ")[-1]
            else:
                inp = inp.split(" ")[-1]

            inp = inp.strip(" ")
            inp = inp.replace(".", "")
            inp = inp.replace("?", "")
            
            return wikipedia.summary(inp.lower(), sentences=3)
        
        except:
            return False
    else:
        return False


if __name__ == "__main__":
    while True:
        print(respond(input("> ")))

