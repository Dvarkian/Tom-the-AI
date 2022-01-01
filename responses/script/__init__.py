import subprocess
from ioUtils import contains

def writeScript(inp):
    out = subprocess.check_output(["howdoi"] + inp.split(" "))

    out = str(out)[2:-1].replace("\\n", "\n")

    return out


def respond(inp):
    if (contains(inp.lower(), ["howdoi ", "write ", "script ", "code", " in python", " in C", " program "]) and
        not contains(inp.lower(), ["programm"])):
        
        out = writeScript(inp)
        
        if len(str(out)) > 5:
            return out
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    while 1:
        print(respond(input("> ")))
