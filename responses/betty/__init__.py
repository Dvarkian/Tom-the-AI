import subprocess

dir_ = "/".join(__file__.split("/")[:-1]) + "/"
#dir_ = dir_.replace(" ", "\ ")

def respond(inp):
    betty = dir_ + "main.rb"

    if "version" in inp.lower() or "speak" in inp.lower() or "you" in inp.lower() or "i " in inp.lower():
        return False

    cmd = [betty, inp]
    #cmd = cmd.split(" ")
    
    try:
        output = str(subprocess.check_output(cmd))
    except Exception as e:
        print("err", e)
        return False
    
    output = str(output)[2:-3].replace("\\n", "\n")
    output = output[7:]
    
    if output.startswith("I don't understand."):
        print(output)
        return False

    #output = output.strip("\n")

    try:
        output = output.split("\n\n")[-1]
    except:
        pass

    output = output.strip("\n")

    if "betty" in output.lower():
        print("False__ ", output)
        return False

    if len(output) < 3:
        print("short", output)
        return False
    
    return output


if __name__ == "__main__":
    while 1:
        print(respond(input("\n> ")))
    

