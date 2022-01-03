print("Program Started.")

import subprocess
from time import sleep
import re


def runCommand(command):
    #print("Command: " + command[0], end="\n\n")

    if "sudo" in str(command) and "-S" not in str(command):
        return False

    """
    if "sudo" in command[0]:
        password = input("[sudo] password required: ")
        command = ["echo " + password + " | " + command[0].replace("sudo", "sudo -S") + " -y"]
    """
    
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)

    output = ""
    
    # Read stdout from subprocess until the buffer is empty !
    for line in iter(p.stdout.readline, b''):
        if line: # Don't print blank lines
            #print(str(line)[2:-3])
            output += str(line)[2:-3] + "\n"
            #yield line
            
    # This ensures the process has completed, AND sets the 'returncode' attr
    while p.poll() is None:                                                                                                                                        
        sleep(.1) #Don't waste CPU-cycles
        
    # Empty STDERR buffer
    err = p.stderr.read()
    
    if p.returncode != 0:
       # The run_command() function is responsible for logging STDERR 
       print("Error: " + str(err).replace("\\n", "\n"))
       return False

    return output


def respond(inp):
    output = runCommand([inp])
    return output

if __name__ == "__main__":
    while 1:
        print(respond(input("~> ")))


