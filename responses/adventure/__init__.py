"""
Offer Adventure at a custom command prompt.

Copyright 2010-2015 Brandon Rhodes.  Licensed as free software under the
Apache License, Version 2.0 as detailed in the accompanying README.txt.
"""

import argparse
import os
import re
import readline
from sys import executable, stdout
from time import sleep
from .init import load_advent_dat
from .game import Game

BAUD = 1200

gameVar = None
adventureStarted = False


def baudout(s):
    for c in s:
        sleep(9. / BAUD)  # 8 bits + 1 stop bit @ the given baud rate
        stdout.write(c)
        stdout.flush()

        
def move(line):
    global gameVar
    
    if not gameVar.is_finished:
        words = re.findall(r'\w+', line)
        if words:
            out = gameVar.do_command(words).lower().capitalize()

            out = out.replace("\n", " ")

            if "Please answer the " in out:
                return False
            elif "I don't know that word." in out:
                return False
            elif "I don't understand that" in out:
                return False
            else:
                result = ""
                out = out.replace("  ", " ")
                
                for sent in out.split(". "):
                    sent = sent.capitalize() + ". "
                    result += sent
                
                return result
        else:
            return False
    else:
        return False


def start():
    global gameVar
    
    parser = argparse.ArgumentParser(
        description='Adventure into the Colossal Caves.',
        prog='{} -m adventure'.format(os.path.basename(executable)))
    parser.add_argument(
        'savefile', nargs='?', help='The filename of game you have saved.')
    args = parser.parse_args()

    if args.savefile is None:
        gameVar = Game()
        load_advent_dat(gameVar)
        gameVar.start()
        out = gameVar.output
        out = out.capitalize()
        return out
    else:
        gameVar = Game.resume(args.savefile)
        return 'Game restored\n'

    #if not gameVar.is_finished:
    #    line = inp
    #    move(line)


def respond(inp):
    global adventureStarted

    inp = inp.lower().replace(".", "").strip()

    if "advent" in inp and not adventureStarted:
        out = start()
        return out
    elif adventureStarted:
        out = move(inp)
        return out
    else:
        return False
        

if __name__ == "__main__":
    start()

    while True:
        try:
            print(move(input("> ")))
        except EOFError:
            pass
