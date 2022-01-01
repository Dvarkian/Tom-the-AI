#print("Prog. Started: Rand. Trivia")
#print("Loading... ", end="")

#import requests
#from bs4 import BeautifulSoup

dir_ = "/".join(__file__.split("/")[:-1])

import random
from profanity import profanity

def filter_line(line):
    count=0
    ignore=False
    result=[]
    for c in line:
        if c==">" and count==1:
            count=0
            ignore=False
        if not ignore:
            result.append(c)
        if c=="<" and count==0:
            ignore=True
            count=1
    return "".join(result)

"""
page = requests.get('https://en.wikipedia.org/wiki/Wikipedia:Unusual_articles')
soup = BeautifulSoup(page.text, 'html.parser')


alltext = soup.find_all('table')

triviaFile = open("triviaData.txt", "w")
triviaFile.write(str(alltext))
triviaFile.close()
"""

alltext = str(open(dir_ + "/triviaData.txt", "r").read())

splittext = str(alltext).split("<tr>")


questions = []
answers = []

for qa in splittext:
    if len(qa.split("</td>")) != 3:
        continue
    
    q, a, junk = qa.split("</td>")

    try:
        q = q.split("/wiki/")[1].split("\"")[0]
    except:
        continue

    q = q.replace("_", " ")
    q = profanity.censor(q)

    a = filter_line(a)
    a = a.replace("<>", "")
    a = a.replace("href=", "")
    a = a.replace("/wiki/", "")
    a = a.replace("\"", "")
    a = a.replace("\n", "")
    a = profanity.censor(a)

    if len(q) and len(a):
        questions.append(q)
        answers.append(a)


loops = 1
active = False

numOptions = 4
numQuestions = 20

score = 0
correctAns = -1

#print("Done!")

def trivia(inp):
    global correctAns

    if inp[0].isdigit() and correctAns != -1:
        if inp[0] == str(correctAns):
            return "Correct!"
        else:
            return "Wrong!, correct answer was " + str(correctAns) + "."

    else:
        
        out = ""
        out += "\n\nQuestion: "

        index = random.randint(0, len(questions) - 1)

        out += "What is \"" + questions[index] + "\"?\n"

        correctAns = random.randint(1, numOptions)

        for i in range(1, numOptions + 1):
            if i == correctAns:
                out += " "*8 + str(i) + ") " + answers[index] + "\n"
            else:
                out += " "*8 + str(i) + ") " + answers[random.randint(0, len(questions) - 1)] + "\n"

        out = out.strip("\n")

        return out


def respond(inp):
    global active
    
    if "trivia" in inp.lower() or (active == True and inp[0].isdigit()):
        out = trivia(inp.lower())
        
        if "trivia" in inp.lower():
            active = True
        else:
            active = False

        return out
    else:
        return False

if __name__ == "__main__":
    while True:
        print(respond(input("> ")))
