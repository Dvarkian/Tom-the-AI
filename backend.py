# backend.py
# Primary file for backend processing functions of Tom the AI.
# Programmed by Murray Jones (murray.jones12@bigpond.com)
# Completed 21/06/2021

# Import modular components that I programmed.
from ioUtils import * # Input / Output utilities.
#from sidend import * # Functions that both the frontend and the backend need to access.

import time # Handles time.
startTime = time.time() # Define program start time.

# Import command handelers.
import sys
import os
import subprocess
from subprocess import Popen, PIPE

from settings import settings

# Create annd clear the intermediary file, used to talk to frontend.
intermediary = open("intermediaryBackToFront.txt", "w")
intermediary.close()


def retort(message): # Output a message to the frontenf through the intermediary.

    print("[Retorting] " + message)
    
    with open("intermediaryBackToFront.txt", "a", encoding="utf-8") as intermediary: # Open the intermediary.

        encodeFailed = False # Init flag for unicode errors.
        
        try: # Try to write data to intermediary.
            intermediary.write("\n[BACKEND] " + message)
            
        except UnicodeDecodeError:
            encodeFailed == True
            
        except UnicodeEncodeError:
            encodeFailed == True


        if encodeFailed: # Non-unicode character encountered.
            
            intermediary.write("\n[BACKEND] " + "Response: Unicode Issue.")
        
            response = mbox("Tom encountered a non-unicode character while fetching your response. " + 
                            "The response to your last input has unfortunately been lost. " +
                            "Please try a different input.",
                            "warning", title="Unicode Decode Error", buttons=["Ok"])

            if response == "Closed" or response == "Ok":
                pass


inLines = 0 # Placeholder for linedof data in intermediary file.

def intort(): # Recieve data from the frontend.
    global inLines
    
    with open("intermediaryFrontToBack.txt", "r", encoding="utf-8") as intermediary: # Read data from iintermediary file.
        
        lines = intermediary.readlines()
        
        if len(lines) == 0: # No data in intermediary file.
            time.sleep(0.05)
            return ""
        
        elif len(lines) > inLines: # New data in intermediary file
            incoming = lines[inLines:] # Get new data
            inLines = len(lines)
            
        else: # No new data is present.
            time.sleep(0.1)
            return ""

    # Remove some of the unwanted syntax that arose from passinng the data through a .txt file.
    incoming = str(incoming).replace("[FRONTEND] ", "")
    incoming = incoming.replace(" \']", "").replace("\']", "").replace("\"]", "")

    return incoming


retort("Backend Started")


platform = "unknown" # Placeholder for platform
dir_ = "" # Placehoolder for working directory.

if "\\" in os.getcwd(): # Recognises windows machines by use of \\ in their file paths.
    platform = "windows"
    dir_ = os.getcwd() + "\\" # Find directory from which program is running.
    sys.path.insert(0, dir_ + "windows_modules") # Add windows module directory to locations that python will search when trying to import modules.

else:
    platform = "linux" # File path uses / instead of \\. Therefor we are running on a unix or bsd system
    dir_ = os.getcwd() + "/" # Find directory from which program is running.
    sys.path.insert(0, dir_ + "linux_modules") # Add linux module directory to locations that python will search when trying to import modules.

sys.path.insert(0, dir_ + "responses") # Add linux module directory to locations that python will search when trying to import modules.
sys.path.insert(0, dir_ + "generic_modules") # Modules used by both windows and linux systems.


retort("Loading")


import regex # Tensorflow Dependency
import re # Used for regular expressions.

import nltk # Python natural language toolkit.
nltk.data.path.append(dir_ + "generic_modules/nltk_data") # Define local directory as nltk data source.
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

stopwords = stopwords.words("english") # Load stopwords database.

from profanity import profanity # Keep it friendly, GPT.

# Modules used to retrieve and parrse HTML.
import requests # Used to retrieve web data.
import urllib3 # Dependancy of BS4.
from bs4 import BeautifulSoup # Html parser.

fake_headers = incur("fake_headers") # Used to dodge google's bot blocking.
from fake_headers import Headers

import webbrowser # Opens files or URL's in the web browser

import random # Random number generator.

#import convai
#from what_are_the_chances import findProb

indexedFiles = 0 # Will hold total count of files that have been iindexed.

username = str(subprocess.check_output(['whoami']))[2:-3] # Get username.

if platform == "windows": # Fixes a bug that occurs on windows machines running a dual user.
    username = username.split("\\")[0]

# Establish base Directory for file search
if platform == "linux":
    dirName = '/home/' + username # Base Directory for file search
elif platform == "windows":
    dirName = 'C:\\' # Base Directory for file search

# Folders to exclude from file indexing. Speeds up indexing  by avoiding system files.
exclude = set(['Program Files', 'Program Files (x86)', 'Windows', 'Intel', "src", "lib", "bin", "include", "lu", "corpora", "Anaconda3",
               "Trash", "trash", ".trash1000", "libcache", "contrib", "tensorflow", "Data", "__pyscache__", "translations", "WCH.CN",
               "Prefabs", "qml", "api", "Editor", "bindings", "DECApps", "Logs", "ProgramData", "AppData", "unityclient", "Windows.old",
               "Adobe", "backups", "$Recycle.Bin", "$Windows.~BT", "Updates", "HP", "Drivers", "SWSetup", "SYSTEM.SAV", "Util",
               "pygame", "Assets", "dist", "src_c", "AccountPictures", "models", "install", "driver"])



if settings("cache"): # If we are going to create a settings("cache") of indexed files. Whole function possibly superfluous.
    
    try: # Create the settings("cache") file.
        cacheFile = open("dircache.txt", "x")
        
    except FileExistsError: # Read cachhe file if it already exists.
        cacheFile = open("dircache.txt", "r")

        lastRead = 0
        
        try: # Identify when the settings("cache") file was made.
            lastRead = cacheFile.readlines()[0]
        except IndexError:
            pass
        except UnicodeDecodeError:
            pass

        cacheFile.close()


sentenceCount = int(settings("length") / 5.1) # [sentences] of subjective and objective response


listOfFiles = [] # Will store list of indexed files.

#print("Indexing home directory...")

for (dirpath, dirnames, filenames) in os.walk(dirName): # Index all files under dirName.

    dirnames[:] = [d for d in dirnames if d not in exclude] # Ignore excluded directories.

    filepath = [os.path.join(dirpath, file) for file in filenames] # Walk along file path.

    if not len(filepath): # Ignore null file paths that occur in corrupted sectors.
        continue

    for loc in filepath: # Iterate throuth files in path.

        # Ignore any files containing these keywords.
        if contains(loc, ["/.", "corpora", "module", "lib", "Packages", "packages", "tensorflow", "NTUSER.DAT"]):
            continue

        listOfFiles.append(loc) # Append files to list.
        indexedFiles += 1 # Iterate number of indexed files.

        if indexedFiles % 2000 == 0:
            retort("Indexing home directory... " + str(indexedFiles) + " files indexed.")

#print("Indexed a total of " + str(indexedFiles) + " files.") # Output number of files indexed.


if settings("cache"): # Create a settings("cache") of files we justt indexed.

    # Clear the settings("cache") file.
    cacheFile = open("dircache.txt", "w", encoding="utf-8")
    cacheFile.close()

    with open("dircache.txt", "a", encoding="utf-8") as cacheFile: # Write data to settings("cache") file.

        cacheFile.write(str(time.time()) + "\n")
        
        for file in listOfFiles: # Iterate through list of files.
            
            try: # Try to crite directory to settings("cache").
                cacheFile.write(file + "\n")
                
            except UnicodeEncodeError as e: # Directory contained a special character.
                retort("cache Encoding Exception: " + str(e))

     
# Variables used for NLP settings("length") monitoring.
avgWordChars = 5.1 # [letters]
avgSentWords = 14.3 # [words]
avgSentChars = avgWordChars * avgSentWords # [chars]

sentenceCount = int(settings("length") / avgSentChars) # [sentences] of subjective and objective response

# Define file types that can be pened on each platform.

if platform == "linux":
    mediaTypes = ["ogg", "mp3", "mp4", "mkv", "wma", "mpeg", "webm", "m4a", "avi"] # Open with vlc.
    otherTypes = {"py": "idle", "pdf": "evince"}

elif platform == "windows":
    mediaTypes = ["ogg", "mp3", "wma", "mpeg", "webm", "m4a"] # Open with vlc.
    otherTypes = {}

officeTypes = ["odf", "odt", "ods", "odp", "doc", "docx", "ppt", "xls", "pptx", "xlsx", "rtf", "txt"] # Open with libreoffice
webTypes = ["jpeg", "jpg", "png", "gif", "htm", "html"]


#responseModules = os.listdir(dir_ + "responses")
#responseModules.sort()

responseModules = str(open("responseOrder.txt").read()).split("\n")

for resp in responseModules:
    resp = resp.replace("\n", "").replace(" ", "")
    if "." not in str(resp) and len(resp) > 3:
        retort("TELL: Importing " + str(resp).replace("_", " ") + " cabability.")
        try:
            exec("import " + str(resp))
        except:
            responseModules.remove(str(resp))

            file = open("responseOrder.txt", "w")
            file.close()
            
            with open("responseOrder.txt", "a") as file:
                for resp in responseModules:
                    file.write(str(resp) + "\n")
            
            
        #print(eval(str(resp) + ".respond(\"" + input("inport > ") + "\")"))



# Identify and ooutput load time.
loadTime = time.time() - startTime
retort("Loaded in " + str(loadTime) + " s.")

retort("Ready") # Inform frontend that loading is complete.



#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
### END OF LOADING ####################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################



def openMedia(inp, playOnly): # Open media files based on a given input
    
    selected = [] # Will hold a list of all relevant files.
    sorted_ = [] # Will hold a list of all relevanf files iin order of relevance.

    maxToSort = 100 # Liimit on how many files to try to sort, reduces lag.

    instruction = inp.split(" ")[0] # Instruction, eg. "play", "open", etc.
    
    inp = " ".join(inp.split(" ")[1:]) # Tidy input, remove instruction.


    if "monty" in inp: # Fixes a very funny bug when trying to play monty python episodes.
        inp = inp.replace("python", "")


    oldinp = inp # Save old version for the stopwords included iteration.

    unknownTypes = []

    for stopwd in [0, 1]: # Try first without stopwords, then with.

        if stopwd == False: # Remove stopwords.
            inp = "".join([word for word in inp.split(" ") if word not in stopwords])
            
        else: # Re-enstate old input with stopwords.
            inp = oldinp
            

        for elem in listOfFiles: # Iterate through File Index

            if "." not in elem: # Ignore files with no extension.
                continue


            # Fromat file paths to a plain string for relevance comparison.

            if platform == "linux":
                fileName = (" " + elem.split("/")[-1].strip() + " ").lower()
                elemString = " " + elem.replace("/", " ").replace("_", " ").replace("-", " ") + " "
                
            elif platform == "windows":
                fileName = (" " + elem.split("\\")[-1].strip() + " ").lower()
                elemString = " " + elem.replace("\\", " ").replace("_", " ").replace("-", " ") + " "


            ext = (fileName.split(".")[-1]).replace("\n", "").strip() # Determine file type.

            if playOnly and (ext not in mediaTypes): # Ignore non--media files if we have been specifically asked to play media.
                continue

            # Check that extension can be opened.
            if (((ext not in mediaTypes and ext not in officeTypes and ext not in webTypes and ext not in otherTypes.keys()) or len(ext) > 5)):
                
                if ext not in unknownTypes: # Avoid duplicates of unknown types.
                    unknownTypes.append(ext) # Record unknown types for potential upgrade purposes.
                
                continue
                
            for word in inp.lower().split(" "): # Cycle through words in the input.

                if " " + word + " " in " " + fileName.lower() + " ": # Only compare whole words in file name, not parts of words.
                    
                    if word not in stopwords: # Stopwors carry less importance.
                        
                        for i in range(0, 3):
                            selected.append(elem) # Non-stop words in the file name are the most important.
                            
                    else:
                        selected.append(elem) # Stopwoords are less important.

                elif " " + word + " " in elemString.lower(): # Comare words from file path.
                    selected.append(elem) # Assemble relevant selections.



        while len(selected): # Sort selected files by relevance.
            best = max(set(selected), key=selected.count) # Find best match.

            if len(sorted_) >= maxToSort: # Limit files to sort to reduce lag.
                break
        
            sorted_.append(best) # Add relevant file to sorted list.
            selected.remove(best) # Remove relevant file from unsorted list.

        sorted_ = list(dict.fromkeys(sorted_)) # Remove duplicates from sorted list.
        
        if len(sorted_) > 0: # If we found any files, proceed to open them.
            break

    else: # Nothing was found in our search
        retort("No local files found.")

        try: # Try to open the media on the internet.

            query = oldinp
            
            if playOnly: # Open a video, most likeley from youtube.
                query = oldinp + " video"

            urls = []
            i = 0
            
            while not len(urls):
                urls = findURLs(oldinp)

                i += 1
                if i >= 3:
                    break
            
            urlToOpen = urls[0]
            webbrowser.open(urlToOpen) 

            retort("Response: " + affirm())
            return affirm()


        except IndexError as e: # No relevant media was found online either.
            
            retort("Response: No relevant files were found on your device, or online.")
            return ""


    if not len(sorted_): # We found files, but they were all irrelevant. Shhould never happen.
        retort("No relevant files found.")

        try: # Try to open the media on the internet.
            
            query = oldinp
            
            if playOnly: # Open a video, most likeley from youtube.
                query = oldinp + " video"

            urls = []
            i = 0
            
            while not len(urls):
                urls = findURLs(oldinp)

                i += 1
                if i >= 3:
                    break
            
            urlToOpen = urls[0]
            webbrowser.open(urlToOpen) 

            retort("Response: " + affirm())
            return affirm()
        
        except IndexError: # No relevant media was found online.
            
            retort("Response: No relevant files were found on your device, or online.")
            return ""
        

    retort("File search complete")

    while 1: # Loop for playlist.
        
        for choice in sorted_: # Iterate through list of sorted files.
            
            extension = choice.split(".")[-1] # Determine file type.
            
            if extension in mediaTypes or playOnly: # Open audio aor video media files with vlc.

                index = 0

                while True:

                    try: # Try to get the item from thhe sorted list.
                        item = sorted_[index]
                    except IndexError: # Should never happen.
                        break

                    ext = item.split(".")[-1] # Determine file type.
                    
                    if ext not in mediaTypes: # Remove non media files if we are trying to play a playlist of media files.
                        
                        #retort("Removed bad type " + str(ext))
                        sorted_.remove(item)
                        
                    else: # Iterate through sorted files.
                        index += 1

                
                retort("Play: " + str(sorted_)) # Pass sorted files to frontend media player.
                
                return
            
            else: # Not an audio or video file.
                
                if platform == "linux":
                    
                    if extension in officeTypes: # Open with libreoffice.
                        
                        process = Popen(["loffice", choice], stdout=PIPE, stderr=PIPE)
                        
                        retort("Response: " + affirm())
                        return affirm()

                    elif extension in webTypes: # Open with web browser.
                        
                        webbrowser.open(choice)
                        
                        retort("Response: " + affirm())
                        return affirm()
                    
                    elif extension in otherTypes.keys(): # Run designated ccommand for file type.
                        
                        process = Popen([otherTypes[extension], choice], stdout=PIPE, stderr=PIPE)
                        
                        retort("Response: " + affirm())
                        return affirm()

                    
                elif platform == "windows":
                    
                    os.startfile(choice) # Open with installed applications.
                    
                    retort("Response: " + affirm())
                    return affirm()
    

def main(): # Main backend function, non-blocking.

    responded = False # Flag to determin if a response has been generated.

    incoming = intort() # Check for incoming data from frontend.
    #incoming = "Respond: " + input("> ")

    if not len(incoming): # Avoid constantly reading the intermediary, uses up too much CPU.
        time.sleep(0.3)
        

    genStTime = time.time() # Start time of response generation.


    if "Frontend Closed" in incoming: # Frontend is closed, close the backend too.
        quit()


    elif "Update settings" in incoming: # Update to changed settings.
        retort("Settings reloaded")
        reloadSettings()
        

    elif "Respond: " in incoming: # Generate a subjective response.

        inp = (incoming.split("Respond: ")[1].replace("\n", " ")).strip() # Format input.

        retort("Gererating response for " + str(inp)) # working on it!

        responseModules = str(open("responseOrder.txt").read()).split("\n")

        for module in responseModules:
            retort("GEN: " + str(module))
            
            try:
                out = eval(str(module) + ".respond(\"" + str(inp) + "\")")
            except Exception as e:
                retort("Response error: " + str(e) + " in " + str(module))
                continue
            
            if out != False and out != None:
                break
        else:
            retort("FALLBACK")
            out = clever_response.go(inp)
            if out == False or out == None:
                out = subjective_response.go(inp)
        
        retort("Response: " + str(out)) # Output response.
        responded = True


    elif "Say: " in incoming: # Vocalise a string.
        inp = incoming.split("Say: ")[1].strip() # Format input.

        retort("Vocalising " + str(inp))
        say(inp, voiceRate=settings("voiceRate")) # Pass to ioUtils.py for vocalisation.


    elif "Open: " in incoming: # Open a file, may be a document  or audio.
        inp = (incoming.split("Open: ")[1].replace("\n", " ")).strip() # Format input.

        retort("Opening file " + str(inp)) # working on it!
        out = openMedia(inp, False) # Find and open file.

        responded = True

    elif "ToPlay: " in incoming: # Open audio or video media.
        inp = (incoming.split("ToPlay: ")[1].replace("\n", " ")).strip() # Format input.

        retort("Opening media " + str(inp)) # working on it!
        out = openMedia(inp, True) # Find and open media.

        responded = True


    if responded: # A response has just been generated.
        
        incoming = "" # Reset recieved data variable.
        time.sleep(0.5) # Give the frontend a chance to recieve the response.
        
        genTime = time.time() - genStTime # Determine how long response took to generate.
        retort("Generated in " + str(genTime) + " s.") # Output generation time to finetune loading bars.



while True: # Main loop for backend.

    #main()

    
    try:
        main() # Run the main function.

    except Exception as e: # Catch and report any errors. 
        
        if "broken pipe" in str(e).lower(): # Occurs if frontend is closed from shell.
            retort("Broken Pipe")
            quit() # Backend should also be closed.


        # Program may have crashed, but at least thhere's a lovely dialog box to tell you about it!
        
        response = mbox("A fatal error has occured whilst processing your response, rendering Tom unable to continue function. " +
                        "We're really sorry about this. " + 
                        "Please restart Tom, and avoid giving the input that caused the error. " +
                        "The error code for this issue is \"" + str(e) + "\". Plese report this error, and the input that caused " +
                        "the error to the developer so that it can be rectified: murray.jones12@bigpond.com.",
                        "error", heading="Something went horribly wrong.", title="Fatal Error: " + str(e), buttons=["Ok"])

        if response == "Closed" or response == "Ok":
             pass

        retort("[ERROR] " + str(e)) # :(

