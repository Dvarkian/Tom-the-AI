import random
from word2number import w2n
import re

dir_ = "/".join(__file__.split("/")[:-1])
NLRME = open(dir_ + "/NLRMEv2.txt").read().splitlines()


def parse_number(string, numwords=None):
    """
    Parse the given string to an integer.

    This supports pure numerals with or without ',' as a separator between digets.
    Other supported formats include literal numbers like 'four' and mixed numerals
    and literals like '24 thousand'.
    :return: (skip, value) containing the number of words separated by whitespace,
             that were parsed for the number and the value of the integer itself.
    """
    if numwords is None:
        numwords = {}
    if not numwords:
        units = ["zero", "one", "two", "three",
                 "four", "five", "six", "seven", "eight", "nine", "ten",
                 "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                 "sixteen", "seventeen", "eighteen", "nineteen"]
        tens = ["", "", "twenty", "thirty", "forty", "fifty",
                "sixty", "seventy", "eighty", "ninety"]
        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numwords[word] = (10 ** (idx * 3 or 2), 0)

    skip = 0
    value = 0
    elements = string.replace(",", "").split()
    current = 0
    for d in elements:
        number = d.split("-")
        for word in number:
            if word not in numwords:
                try:
                    scale, increment = (1, int(word))
                except ValueError:
                    value += current
                    return skip, value
            else:
                scale, increment = numwords[word]
                if not current and scale > 100:
                    current = 1
            current = current * scale + increment
            if scale > 100:
                value += current
                current = 0
        skip += 1
    value += current
    return skip, value


def dice_parse(inp):
    repeat = 1
    howmany = 1
    edges = 6

    prefix = ""
    prefix_length = 0
    prefix_number = -1

    # Iterate string.
    # Search for number before keywords (edges, times, dices)
    for word_current in inp.split():
        parse_result = parse_number(prefix)

        # make sure, prefix still contains only number-characters
        if parse_result[0] != prefix_length:
            # last token not part of number -> reset prefix
            prefix = word_current
            prefix_length = 1
            continue
        
        prefix_number = parse_result[1]

        if word_current == "edge" or word_current == "edges" or word_current == "sided":
            edges = prefix_number

        if word_current == "times":
            repeat = prefix_number

        if word_current == "dices" or word_current == "dice":
            howmany = prefix_number

        prefix += " "
        prefix += word_current
        prefix_length += 1

    return {"repeat": repeat, "howmany": howmany, "edges": edges}


def dice_is_error_in_config(config):
    assert isinstance(config["edges"], int)
    assert isinstance(config["howmany"], int)
    assert isinstance(config["repeat"], int)

    if config["howmany"] == 0:
        return "No dice to roll?"
    if config["howmany"] < 0:
        return "Rolling {} dices does not really make sense ;).".format(
            config["howmany"])
    if config["repeat"] == 0:
        return "Roll 0 howmany? Finish!"
    if config["repeat"] < 0:
        return "Doing something {} does not really make sense ;).".format(
            config["repeat"])
    if config["edges"] <= 1:
        return "A dice with {} edges does not really make sense ;).".format(
            config["edges"])

    return False


def abstract_dice_roll(config):
    for _ in range(config["repeat"]):
        yield [str(random.randint(1, config["edges"])) for _ in range(config["howmany"])]


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



def roll(inp):
    
    nums = ""

    for word in inp.split(" "):
        try:
            word = w2n.word_to_num(word)
        except:
            pass

        nums += str(word) + " "

    if "." in nums:
        nums = nums.split(".")[0]
    nums = nums.strip()

    #print(nums)

    a = " ".join(inp.split(" ")[:2])
    b = " ".join(inp.split(" ")[2:])

    try:
        rolls = str(int(a.split(" ")[-1]))
        dice = str(int(b.split(" ")[0]))
    except:

        if "d" not in nums:
            #print(nums)
            try:
                #print("Nter")
                n = int(nums)
                return n, [n], 0
            except:
                #print("Noll")
                return 0, None, 0

        rolls = nums.split("d")[0]
        dice = nums.split("d")[1]

    for i in rolls:
        try:
            temp = int(i)
        except Exception as e:
            rolls = rolls.replace(i, "")

    for i in dice:
        try:
            temp = int(i)
        except Exception as e:
            dice = dice.replace(i, "")

    total = 0

    try:
        rolls = int(rolls)
    except:
        rolls = 1

    try:
        dice = int(dice)
    except:
        dice = 6

    aspect = []

    for i in range(0, rolls):
        value = random.randint(1, dice)
        aspect.append(value)
        total += value

    return total, aspect, rolls



def altRoll(inp):

    if (" a " not in inp and " time" not in inp) and "side" in inp:
        return False
    
    config = dice_parse(inp)

    #print(config)

    error = dice_is_error_in_config(config)
    
    if error:
        return False

    rolls = []

    for roll in abstract_dice_roll(config):
        rolls.append(int(roll[0]))

    return "I rolled " + str(rolls) + "."


def handle(inp):

    alt = altRoll(inp)

    if alt and "side" in inp:
        return alt
        
    inp = inp.lower()
    inp = inp.replace("plus", "+")

    parts = inp.split("+")

    total = 0
    aspects = []

    showAspect = False

    if len(parts) == 1 and "d" not in parts[0]:

        if alt:
            return alt
        else:
            total = random.randint(1, 20)

    else:
        for part in parts:
            value, aspect, rolls = roll(part)

            if rolls > 1:
                showAspect = True
                
            total += value
            aspects.append(aspect)

    astring = ""

    for a in aspects:
        astring += str(a) + " + "
        
    astring = astring[:-3]

    astring = astring.replace(", ", " + ")

    if showAspect:
        return "I rolled " + astring + " = " + str(total) + "."
    else:
        return "I rolled " + str(total) + "."


def respond(inp):

    if "coin" in inp and ("flip" in inp or "toss" in inp):
        return random.choice(["Heads", "Tails"])

    if " -" in inp or " 0 " in inp or "zero" in inp:
        return False
    
    if (contains(inp.lower(), ["roll ", "random "]) and not
        contains(inp.lower(), ["word", "action", "person", "place", "world", "thing", "object", "nature", "all", "AP"])):

        if "gi" in inp:

            st = False
            end = False

            st_index = 0
            end_index = 0 

            for i in range(0, len(inp)):
                if inp[i].isdigit() and not st:
                    st = True
                    st_index = i
                elif not inp[i].isdigit() and st and not end:
                    end = True
                    end_index = i

            try:
                num = int(inp[st_index:end_index])
            except:
                num = 1

            #print(num)

            rangis = ""

            for i in range(0, num):
                rangi = random.choice(NLRME)
                if num == 1:
                    rangi = " ".join(rangi.split(" ")[1:]).strip()
                    rangis += rangi
                elif i == num:
                    rangi = " ".join(rangi.split(" ")[1:]).strip()
                    rangis += rangi + ". "
                else:
                    rangi = " ".join(rangi.split(" ")[1:]).strip()
                    rangis += rangi + ";\n"
                    
            return rangis

        else:
            out = handle(inp)
            
        return out

    else:
        return False


if __name__ == "__main__":
    while 1:
        print(respond(input("> ")))
