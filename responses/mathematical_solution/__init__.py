from sympy import *


def insert(string, index, replacement):
    # Replace character at nth index position5
    string = string[0:index] + replacement + string[index+1:]

    return string


def subSyns(string, syns, sub):
    for syn in syns:
        if syn in string:
            string = string.replace(syn, sub)
            
    return string


def mathSolve(inp):

    inp = inp.lower()

    if "solve" in inp and "=" not in inp:
        inp = inp.replace("solve", "solve x =")

    inp = subSyns(inp, ["minus"], "-")
    inp = subSyns(inp, ["plus"], "+")
    inp = subSyns(inp, ["times", "multiplied by"], "*")
    inp = subSyns(inp, ["raise", "to the power of", "to the power", "to the"], "**")
    inp = subSyns(inp, ["divided by", "on"], "/")

    inp = inp.replace("^", "**")
    inp = inp.replace("for", ", ")
    inp = inp.replace("\n", " ")
    
    inp = inp.replace("root", "sqrt")
    inp = inp.replace("f(x)", "expr")

    inp = inp.strip(" ")
    inp = inp.strip(".")

    inp = subSyns(inp, ["derivative of", "differentiate"], "diff")
    inp = subSyns(inp, ["integral of", "integral", "integarte", "intagrate"], "integrate")

    if "=" in inp:
        
        for i in range(0, len(inp)):
            if inp[i] == "=":
                inp = inp[:i] + "-(" + inp[i+1:] + ")"
                break       
                
        if "solve" not in inp:
            inp = "solve " + inp

    opened = 0
    closed = 0

    first = True
    subj = ""

    closeE = False

    last = "alpha"

    for i in range(0, len(inp)):
        
        if inp[i].isalpha() and opened > 0:
            exec(str(str(inp[i]) + " = Symbol(\'" + str(inp[i]) + "\')"))
                
            try:
                if inp[i] == "e" and inp[i+1] == "*" and inp[i+2] == "*":
                    inp = insert(inp, i+1, "")
                    inp = insert(inp, i+1, "")
                    inp = insert(inp, i, "exp(")
                    closeE = True
                    #opened += 1
            except:
                pass

            if first:
                subj = inp[i]
                first = False

            if last == "digit" and inp[i] != " ":
                #print("*ing")
                inp = inp[:i] + "*" + inp[i:]

            last = "alpha"

        elif inp[i].isdigit():
            last = "digit"
        else:
            last = "?"
            
        if inp[i] == " " and not opened:
            inp = insert(inp, i, "(")

        if (inp[i] == " " and closeE):
            inp = insert(inp, i, ")")
            closeE = False
            

        if inp[i] == "(":
            opened += 1
        elif inp[i] == ")":
            closed += 1    


    while len(inp.split("("))-1 > len(inp.split(")"))-1:
        inp += ")"
        print("Patch")
        closed += 1

    if __name__ == "__main__":
        print("MATHSOLVE " + str(inp))

    try: 
        out = eval(str(inp))
        print(out)
    except NotImplementedError:
        out = "No solutions."
    except Exception as e:
        if __name__=="__main__":
            print(e)
        return False

    out = str(out)

    if "," not in str(out):
        out = subSyns(str(out), ["[", "]"], "")

    out = out.replace("I", "i")
    out = out.replace("log", "ln")

    if "x" in inp and "solve" in inp:
        subj = "x"
        
    if "diff" in inp:
        subj = "dy/dx"
        
    if "integr" in inp:
        if "x" in inp:
            subj = "∫f(x)"
        elif "y" not in inp:
            subj = "∫y"
        else:
            subj = "∫" + subj

        out = out + " + c"
    
    out = subj + " = " + str(out)[:6].strip("0").strip(".")

    return out


def respond(inp):
    out = mathSolve(inp.lower())
    if out != False:
        out = out.replace("**", "^")
    return out


if __name__ == "__main__":
    while 1:
        print(respond(input("> ")))

