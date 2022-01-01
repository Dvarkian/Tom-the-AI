from profanity import profanity
import time
import random
#from ioUtils import contains
import requests

dir_ = "/".join(__file__.split("/")[:-1])

list_ = open(dir_ + "/commonMisconceptions.txt").read().splitlines()


def numbersapi(inp):

    parts = inp.split(" ")

    if not inp or 'help' in parts:
        print(numbersapi.__doc__)
        return

    if any((not part.isnumeric() for part in parts)):
        print("\tPlease, pass valid integers as arguments.")
        return False

    for number in parts:
        data = get_data(number)
        
        if data:
            out = (f"\t{data}")
            out = out.strip()
            return out


def get_data(number):
    base_url = "http://numbersapi.com/"
    try:
        response = requests.get(f"{base_url}{number}")
        return response.text
    
    except requests.exceptions.RequestException:

        print(f"\tCould not get data from {base_url}")
        return False
    

def smarter():
    return random.choice(list_)


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


def respond(inp):

    inp = inp.strip(" ").replace(".", "")
    
    try:
        inp = int(inp)
        return numbersapi(inp)
    except:
        pass

    st = -1
    end = -1

    
        
    if contains(inp.lower(), ["fun fact", "smarter", "misconception", "misunderstanding", "fact of the"]):

        inp += " "

        for i in range(0, len(inp)):
            if inp[i].isdigit() and st == -1:
                st = i
            elif not inp[i].isdigit() and st >= 0:
                end = i
                val = str(int(inp[st:end]))
                return numbersapi(val)

        else:
            inp = inp.strip()
            
            out = smarter()
            return out
        
    else:
        return False


if __name__ == "__main__":
    while True:
        print(respond(input("> ")))
