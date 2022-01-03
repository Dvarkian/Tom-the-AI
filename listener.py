# frontend.py
# Background vloce recogniser for Tom the AI.
# Programmed by Murray Jones (murray.jones12@bigpond.com)
# Completed 21/06/2021


from ioUtils import * # Input / output utilities.

# Import command handellers.
import os
import sys
import time
import subprocess

from settings import settings


# Find platform and directory from which program is running.

platform = "unknown"
dir_ = ""

if "\\" in os.getcwd():
    platform = "windows"
    dir_ = os.getcwd() + "\\"
    sys.path.insert(0, dir_ + "windows_modules")
    
else:
    platform = "linux"
    dir_ = os.getcwd() + "/"
    sys.path.insert(0, dir_ + "linux_modules")

sys.path.insert(0, dir_ + "generic_modules") # Defind generic module source directory.


def retort(message): # Output a message to the frontend.

    with open("intermediaryBackToFront.txt", "a", encoding="utf-8") as intermediary: 
        intermediary.write("\n[LISTENER] " + message) # Append message to the intermediary file.


inLines = 0

def intort(): # Recieve message from the frontend.
    global inLines
    
    with open("intermediaryFrontToBack.txt", "r", encoding="utf-8") as intermediary:
        lines = intermediary.readlines()

        if len(lines) == 0:
            time.sleep(0.05)
            return ""
        
        elif len(lines) > inLines:
            incoming = lines[inLines:]
            inLines = len(lines)
            
        else:
            time.sleep(0.1)
            return ""

    incoming = str(incoming).replace("[FRONTEND] ", "")
    incoming = incoming.replace(" \']", "").replace("\']", "").replace("\"]", "")

    return incoming


import speech_recognition as sr # Import Speech Recognition module.
import time

time.sleep(3) # Give speech_recognition time to load.

retort("Listener Started")

notified = False # Has the user been notified about a lack of intenet connection?

r = sr.Recognizer() # Init speech recogniser


def listen(): # Listens for a voice input, blocking.
    global notified

    out = "" # Placeholder for heard output.

    try:
        
        with sr.Microphone() as source: # Establish microphone connection, closes automatically.

            r.adjust_for_ambient_noise(source) # Adjust mic vol for bg noise.

            #print("Listening... ", end="")

            try:
                
                data = r.listen(source) # Record audio from mic. May take a while.
                
                retort("Processing Voice")
                print("Done")

                
            except Exception as e: # An error occured whilst listening to the microphone. E.g. It was unplugged.
                
                response = mbox("An error occured whilst listening for a voice input. " +
                        "If you select \"Disable\", vice recognition will be unavailiable for this session. " +
                        "The error code for this issue is \"" + str(e) + "\". Plese report this error, and the input that caused " +
                        "the error to the developer so that it can be rectified: murray.jones12@bigpond.com.",
                        "warning", heading="Something went horribly wrong.", title="Listener Error: " + str(e), buttons=["Retry", "Disable"])

                if response == "Closed" or response == "Retry":
                     pass
                    
                elif response == "Disable":
                    quit()
                    
                
    except OSError: # Device does not have a microphone.
        
        response = mbox("No microphone was dectected. Voice recognition will be unavailiable. " +
                        "To use voice recognition, please connect and configure a microphone, then restart Tom.",
                        type_="warning", title="No Microphone Detected", buttons=["Ok"])
        quit()


    try: # Recognise with google if online. 
        out = r.recognize_google(data) # Google's voice recognition is the most reliable.

    except sr.UnknownValueError: # Google could not recognise audio - most likley nothing was said.
        print("[Unrecognised Voice]")

    except sr.RequestError as e: # Offline
        print("[Request Error]")

        if not notified: # Notify about lack of internet connection.
        
            response = mbox("You are either not connected to the internet, or python is not permitted to access the web. " +
                            "Speech Recognition cannot be conducted without an internet connection. " +
                            "Select \"Retry\" to try again if you have fixed the connection issues. " +
                            "Select \"Disable\" to disable speech recognition for this session. " +
                            "Speech Recognition can alsobe disabled permenantly in the settings page. " +
                            "Select \"Continue\" to keep retrying until a connection is established or the program is closed. " +
                            "If you select continue, this message will not be shown again this session.",
                            type_="warning", title="No Internet Connection", buttons=["Retry", "Disable", "Continue"])

            if response == "Retry":
                pass

            elif response == "Continue"  or response == "Closed":
                notified = True
            
            elif response == "Disable":
                retort("Error: No Internet. Closing Listener.")
                quit()


    if len(out): # Avoid a null response.
        out = out.lower().strip() # Remove trailing whitespace
        
        print("Heard: \"" + out + "\"")
        return out.capitalize() # Return recogninised voice

    else:
        return False # Noo voice recognised.


def main(): # Main listener function. Noon-blocking.
    
    incoming = intort() # Check for data from frontend.

    if "Frontend Closed" in incoming: # Exit listener if frontend has been closed.
        quit()

    elif "listen" in incoming.lower(): # Incoming data concerns the listener.
        
        if contains(incoming, ["stop", "quit", "exit"]): # Close the listener.
            
            retort("Closing Listener")
            settings("useVoice", False)

    if settings("useVoice") == True:
        heard = listen() # Listen for a voice input

        if heard: # A voice inpput was heard.
            retort("Heard: " + heard) # Send to frontend.
    else:
        time.sleep(2)


while True: # Main loop for listener.
    
    try:
        main() # Run the main function.

    except Exception as e: # Catch and report any errors. 
        
        if "broken pipe" in str(e).lower(): # Occurs if frontend is closed from shell.
            retort("Broken Pipe")
            quit() # Backend should also be closed.


        # Program may have crashed, but at least there's a lovely dialog box to tell you about it!
        
        response = mbox("An error has occurerd whilst listening for a voice input. Voice recognition will be unavailiable for thhis session. " +
                        "We're really sorry about this. " + 
                        "The error code for this issue is \"" + str(e) + "\". Plese report this error, and the input that caused " +
                        "the error to the developer so that it can be rectified: murray.jones12@bigpond.com.",
                        "warning", heading="The voice recogniser has malfunctioned.", title="Error: " + str(e), buttons=["Ok"])

        if response == "Closed" or response == "Ok":
             pass

        retort("[ERROR] " + str(e)) # :(

        quit()





