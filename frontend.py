# frontend.py
# Primary file for user interface of Tom the AI.
# Programmed by Murray Jones (murray.jones12@bigpond.com)

print("Loading Tom ...") # Initial confirmation of program execution.

tomVersion = "1.1.1"

from ioUtils import * # Various utilities that I use with a lot of my programs. Mostly innput / output related.

import time # Handles time using python builtin module.
startTime = time.time() # Record program start time.


# Import conmmand handlling moules.
from subprocess import Popen, PIPE # Used to start the backend and listener as parallel processes.
import os # Accesses te oporating system and file system.
import sys # Accesses and edits system files.
import subprocess # Used to run commands.

from settings import settings, editSettings
from moduleBrowser import moduleBrowser

# Detect and output the current python version.
version = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2])
print("Detected python version " + str(version))


platform = "unknown" # Placeholder for detected oporatinng system
dir_ = "" # Placeholder for working directory


estLoadTime = settings("estloadTime") # Placeholder for estimated load time. Value is later set on a per platform basis.
newGen = False # Placeholder to determine if a new response generation process has just been initiated.


def ignoreWarning(): # Provides aa warning telling the user not to ignore warnings.
    response = mbox("Choosing to ignore the previous warning may result in runtime errors, render important components of this "+
                    "software unavailiable, or interfere with the function of other software on your device. "+
                    "This is really not a good idea. Only continue if you know what you are doing, and you accept the risks "+
                    "associated.",
        heading="Probable instability ahead.", buttons=["Continue at own risk.", "Yikes! Go back."], type_="warning")

    if response == "Continue at own risk.":
        return True # User really wants to ignore the warning, so let them.
    
    else: # User reconsidered their life choices, and thought better of ignoring my warning.
        return False


os.chdir("/".join(__file__.split("/")[:-1]))

sys.path = [dir_]

if "\\" in os.getcwd(): # Recognises windows machines by use of \\ in their file paths.
    platform = "windows"
    
    dir_ = os.getcwd() + "\\" # Find directory from which program is running.
    #sys.path.insert(0, dir_ + "windows_modules") # Add windows module directory to locations that python will search when tryingg to impory modules.

    kernedFont = "Ariel"

    if version[:3] != "3.6": # Check thaat python version is 3.6, as is required on windows by tensorflow.
        while 1:# mbox loop for incorrect python version.
            response = mbox("Tom requires Python 3.6 to run on Windows, but version " + version + " was detected. " +
                            "Please install Python 3.6 and try again, using Python 3.6 to run Tom.",
                            heading="Python version warning.", buttons=["Ignore", "Quit"], type_="warning")

            if response == "Ignore":
                if ignoreWarning():
                    break
                else:
                    continue
            else:
                quit()
    
else: # File path uses / instead of \\. Therefor we are running on a unix or bsd system
    platform = "linux" # BSD and mac are not supported. Therefor assume we are running on linux.
    
    dir_ = os.getcwd() + "/" # Find directory from which program is running.
    #sys.path.insert(0, dir_ + "linux_") # Add linux module directory to locations that python will search when tryingg to impory modules.
    sys.path.insert(0, dir_ + "responses") # Add linux module directory to locations that python will search when tryingg to impory modules.

    kernedFont = "Helevicta"


sys.path.insert(0, dir_ + "generic_modules") # Modules used by both windows and linux systems.

print("Oporating System identified as " + platform) # Output identified OS to shell.


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-q", "--quiet", help="Start Tom reduced to system tray.", action="store_true")
args = parser.parse_args()

if args.quiet:
    settings("startDown", True)
    settings("discordServer", False)
    time.sleep(8)
else:
    settings("startDown", False)

username = str(subprocess.check_output(['whoami']))[2:-3] # Get the user's name.

if platform == "windows": # Fixes a bug that occurs on windows machines running a dual user.
    username = username.split("\\")[0]

# Create a loading window, as loading can take a while.

import PySimpleGUI as sg # Primary graphics manager. Handles user interface

if not settings("startDown"):
    # Layout definition for loading window.
    loadingLayout = [[sg.Column([[sg.Image("graphics/squareFace.gif", background_color="black", key="-LOADGIF-")],
                     [sg.Text("LOADING TOM ...", text_color="light blue", background_color="black", font="Helevicta 12 italic", size=(None, 1))],
                     [sg.ProgressBar(100, orientation="horizontal", size=(20, 2), bar_color=["purple", "black"], key="-LOAD-PROGRESS-",
                                     border_width=0)],
                     [sg.Text("Importing modules...", text_color="grey60", background_color="black", key="-LOAD-TEXT-",
                              font=(kernedFont, 8), size=(None, 1))]
                      ], element_justification="centre", background_color="black")]]

    # Initiate loading window.
    loadingWindow = sg.Window('Loading Tom ...', loadingLayout,
            grab_anywhere=True,
            keep_on_top=True,
            background_color="black",
            alpha_channel=.92, # Transparency.
            finalize=True, # Update assembled loading window to screen.
            icon="graphics/squareFace.png",
            #no_titlebar=True,
            margins=(35, 35))

    loadingWindow.refresh() # Make sure loading window is fully displayed before continuing.
else:
    loadingWindow = {}

def retort(message): # Outputs a message to the backend / listener via an intermediary.txt file.

    print("[Retorting] " + message)
    
    with open("intermediaryFrontToBack.txt", "a", encoding="utf-8") as intermediary: # Open intermediary temporarily. Will be closed automatically when done.
        intermediary.write("\n[FRONTEND] " + message) # Write message to intermediary file.


lastIntort = "" # Placeholder for last message recieved.
inLines = 0 # Placehlder for lines of intermediary read.
        
def intort(): # Recieves a message from the backend / listener via an iintermediary .txt file.
    global lastIntort
    global inLines
    
    with open("intermediaryBackToFront.txt", "r", encoding="utf-8") as intermediary: # Open iintermediary to read. Closes automatically when done.
        
        lines = intermediary.readlines() # Read contents of the intermediary line by line.
        
        #print("Intermediary at: ", len(lines), inLines) # Intermediary buffer status.
        
        if len(lines) == 0: # Intermediary is empty. Backend and listener are still loading.
            return ""
        
        elif len(lines) > inLines: # New data is present to read.
            incoming = lines[inLines:] # Ignnore lines of data we have read before.
            inLines = len(lines) # Update buffer status.
            
        else: # No new data to read.
            return ""

    incoming = str(incoming).replace("[BACKEND] ", "") # Removes the backend flag. Possily superfluous.

    if incoming != lastIntort: # Ignore repeated messages.
        print("Recieved Local Pass: " + incoming)
        lastIntort = incoming
        
    else: # Message has alreadht been recieved. Ignore it.
        pass

    # Fix formatting issues caued as the data is passed through the .txt format.
    incoming = incoming.replace(" \']", "").replace("\"]", "").replace("\']", "")

    return incoming


import systemGraphTool # A program I created to make a configurable system activity graph in PySimpleGUI.
import importlib # Used to refresh the activity graph after settings had been chanded by reimporting the systemGraphTool module.

import psutil # Used to kill zombie backends.
import signal # Database of process signalling. Used with psutil to find correct kill codes.

activePID = os.getpid() # Get the PID of this frontend process, so theat we don's accidentally kill it.

print("My PID: ", activePID) # Output the recognised PID of this frontend.

def killZombies():
    for proc in psutil.process_iter(): # Iterate over all running process to find and kill zombie backends / listeners.
        # Zombie presesses occur when the software did not exit correctly. e.g. someone typed ctrl+c in the shell instead of quit in the UI.
        # We need to remove these to avoid double-ups on processing.
        
        try: # Try to get process name & pid from process object.
            
            processName = proc.name()
            processID = proc.pid
            
            #print(processID, processName)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): # Process could not be acessed by python.
            pass # Don't do anything to system processes.

        if str(processID) != str(activePID): # Avoid killing this frontend.

            if processName in ["python3.9", "py.exe"]: # Check for zombie backends (or listeners).

                # Kill any zombie backends / listeners so that we can start afresh.
                if platform == "linux":
                    os.kill(int(processID), signal.SIGKILL) # End process with kill signal on linux.
                elif platform == "windows":
                    os.kill(int(processID), signal.SIGTERM) # Terminate signal is used on windows.
                    
                print("Killed PID", processID)

killZombies()

# Clear / create the intermediary files. One for each direction of transmission.
intermediary = open("intermediaryFrontToBack.txt", "w")
intermediary.close()
intermediary = open("intermediaryBackToFront.txt", "w")
intermediary.close()

# Start the backend and lisener processen in the appropriate pyhton version
# These can satart loading whildst the froonntenf continues loading.
if platform == "linux":
    backendProcess = Popen(["python3.9", dir_ + "backend.py"], stdout=PIPE, stderr=PIPE)
    listenerProcess = Popen(["python3.9", dir_ + "listener.py"], stdout=PIPE, stderr=PIPE)
    emotionProcess = Popen(["python3.9", dir_ + "emotion.py"], stdout=PIPE, stderr=PIPE)
elif platform == "windows":
    backendProcess = Popen(["py", "-3.6", dir_ + "backend.py"], stdout=PIPE, stderr=PIPE)
    listenerProcess = Popen(["py", "-3.6", dir_ + "listener.py"], stdout=PIPE, stderr=PIPE)
    emotionProcess = Popen(["py", "-3.6", dir_ + "emotion.py"], stdout=PIPE, stderr=PIPE)


import requests # used to retrieve web pages.

if not settings("startDown"):
    loadingWindow["-LOAD-TEXT-"].update("Connecting to the Internet ...")
    loadingWindow.refresh()

while 1: # Loop to check we are connected to the internet.
    
    try: # Try a simple web request.
        request = requests.get("https://www.google.com", timeout=10)
        print("Internet connected")
        break # Exit the loop.
    
    except (requests.ConnectionError, requests.Timeout) as exception: # No internet connection.
        print("Internet disconnected")
        
        response = mbox("Some of Tom's functions, including voice recognition and objective response, require an internet "+
                        "connection. Please connect to the internet and try again.\n",
                        heading="No internet connection.", buttons=["Retry", "Ignore", "Quit"], type_="warning")

        if response == "Ignore":
            if ignoreWarning():
                break
            else:
                continue
        elif response == "Quit":
            quit()
        else:
            continue

if not settings("startDown"):
    loadingWindow["-LOAD-TEXT-"].update("Importing Modules ...")
    loadingWindow.refresh()

# Import PyQt5 with PyQt4 backwards compatibility, used for system tray icon.
import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import plyer # A remarkably versetile module, so far we're only using it for sending desktop notifications.

# Give a test notification during loading.
if not settings("startDown"):
    plyer.notification.notify(title="Hello!", message="Did you know: Tom can use these notifications to run in the backgroud " +
                              "via voice recognition and vocalisation.",
                              app_icon=dir_+"graphics/squareFace.ico", timeout=12)


import datetime # Handles dates. Possibly superfluous.
import random # Random number generation.
import re # Reqular expressions, used with web scraper.
import webbrowser # Used to open web pages.
import pyjokes # Rather nerdy jokes: I find them hilarious.

import threading # Dependancy of PyQt5, Note: threading gets messy really quickly: Avoid, if at all possible.
import multiprocessing # Used to facilitate menu functions from the system tray icon.
from multiprocessing import Process, Queue # Used to run system tray icon in parallel.


try: # Import media player
    import vlc
    from vlc import Instance # Possibly superfluous.
    
except FileNotFoundError: # VLC media player is not installed.
    print("VLC media player is not installed")

    while 1: # mbox loop for incorrect python version.
        response = mbox("Tom's media functions require VLC media player. " +
                        "Please download and install the latest 64-Bit version of VLC media player from " +
                        "https://get.videolan.org/vlc/3.0.11/win64/vlc-3.0.11-win64.exe. " +
                        "If you already have VLC installed, please ensure thaat you are runneing the latest 64-Bit version of VLC, and " +
                        "taht VLC has been correctly added to PATH.",
                        heading="VLC not found.", buttons=["Ignore", "Quit"], type_="error")

        if response == "Ignore":
                if ignoreWarning():
                    break
                else:
                    continue
        else:
            quit()


# Import Pyhton Natural Language Toolkit and associated packeges.
import nltk
nltk.data.path.append(dir_ + "generic_modules/nltk_data") # Define local directory as nltk data source.
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import sent_tokenize, word_tokenize

import asyncio
import discord
from discord.ext import tasks

TOKEN = eval(open("/home/murray/discord_id.txt").read())["token"] #"<Instert Discord bot token here>"
GUILD = eval(open("/home/murray/discord_id.txt").read())["guild"]

client = discord.Client()


# Set global Variables.

tomFace = "graphics/squareFace.gif" # Gif for tom's 'face'. Should be 300x300px.



# Establish base Directory for file search
if platform == "linux":
    dirName = '/home/' + username 
elif platform == "windows":
    dirName = 'C:\\'

username = username.capitalize() # Capitalise for output, because names should be capitalised.

# Variables relating to the activity / CPU graph.
lastGraphUpdate = 0 # [s since Epoch]
graphInterval = 0.15 # [s]
samples = 120 # No. samples to fit in the graph

loops = 0 # No. of program iterations

# Variables relating to media functions run from the froontend.
playing = False
playlist = []

# Variables relating to timing and program flow.
doubleClickInterval = 0.5 # [s]
#settings("microphoneState") = "passive" # Active, passive, or off.
intermediaryReadInterval = 0.1
readPeriod = 2 # [ms]
gifPeriod = 80 # [ms]

# Variables used for NLP settings("length") monitoring.
avgWordChars = 5.1 # [chars]
avgSentWords = 14.3 # [words]
avgSentChars = avgWordChars * avgSentWords # [chars]

stopwords = stopwords.words("english") # Load stopwords database.

domains = [] # Placeholder for popular website urls.
settings("url", "http://www.google.com/search?q=XXXX") # Base URL used for scraping the search engine. Must also be defined in settings.
settings("accent = english") # Accent for vocalisation. Superfluous on windows as there is only one choice.

working = "False" # Placeholder for curently active process.


with open("top-1m-domains.csv", "r") as domainsFile: # Load recognised domains from database.
    for domain in domainsFile.readlines():
        domain = domain.split(",")[1].replace("\n", "")
        domains.append(domain)


inp = ""
remote = False
secret = False
trivia = False

loadClosed = False

#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
### END OF LOADING ####################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################


class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0
        self.ready = False

        # start the task to run in the background
        self.outer_loop.start()


    async def on_ready(self):
        for guild in client.guilds:
            if guild.name == GUILD:
                print('Tom is connected to ' + f'{guild.name}.')
                self.ready = True


    async def on_message(self, message):
        global remote, inp, secret
        
        if message.author == client.user:
            return

        if contains(str((message.content).lower())[:10], ["tom ", "roll ", "/r", "/t ", "tom, "]):
            remote = True
            inp = message.content.lower()

            inp = replaceAll(inp, [["/r", "roll"], ["/t", "tom"]])

            inp = inp.replace("tom, ", "tom ")
            
            if "tom " in inp:
                inp = inp.split("tom ")[1]
            if "roll " in inp:
                inp = "roll " + inp.split("roll ")[1]

            response = None
            while response == None or response == False:
                response = main(inp)

            print("Discord response", response)

            secret = False
            
            if "[SECRET] " in response:
                response = response.relpace("[SECRET] ", "")
                secret = True

            remote = False

            if response == "None":
                return

            if not secret:
                await message.channel.send(str(response))
            else:
                user = message.author
                await user.create_dm()
                await user.dm_channel.send(response)

            secret = False
            
        return None
        

    @tasks.loop(seconds=0) # task runs every 60 seconds
    async def outer_loop(self):
        global loadClosed

        if self.ready:
            if not loadClosed:
                #startTrayIcon()
                loadingWindow.close() # Close the loading window.
                loadClosed = True

            #SystemTrayIcon.update()

            main()


    @outer_loop.before_loop
    async def before_loop(self):
        await self.wait_until_ready() # wait until the bot logs in


def discernTopic(sent): # Identifies a particular noun as the topic of a scentence.
    
    topic = "I" # Placeholder for default topic.
    
    for word in word_tokenize(sent)[1:]:
        if str(word)[0].isupper() and word not in ["I"] and "NN" == tagWord(word):
            topic = word # Assign topic as first noun in secentence.
            
    return topic


lastVocalisation = "" # Placeholder for the lasst vocalised output.
deline = True

responsesGiven = 0

def output(message, text_color=None, title="Tom", icon="graphics/squareFace.png", silent=False): # Output a response.
    # Includes vocalisation, text, and system tray icon outputs.
    
    global window, deline, remote, responsesGiven
    global lastVocalisation

    message = str(message) # Ensure the message is a string.

    try: # Try to capitalise the message.
        message = message[0].capitalize() + message[1:]
    except IndexError: # Message was null.
        return False

    #if deline: # Removes newline (\n) characters from message.
    #    message = message.strip().replace("\n", "").replace("\\n", " ")

    if not contains(message[-1], [".", "!", "?"]): # Add proper end punctuation.
        message += "."

    # Fix any punctuation issues. These are often created as messages are passed through .txt files.
    message = message.replace(".?", "?")
    message = message.replace("   ", " ").replace(" . ", ". ").replace(" , ", ", ").replace(" ; ", "; ")
    message = message.replace("  ", " ").replace("%27", "")

    if not remote:
        runVoice = settings("useVoice")

        if silent: # Don't vocalise the output.
            runVoice = False

        if not contains(message, ["~>"]) or runVoice == True:
            if settings("notify") and message[0] != "~":
                # Send output as a desktop notification.
                plyer.notification.notify(title=title, message=message, app_icon=dir_+"graphics/squareFace.ico", timeout=6)
            
        if settings("windowOpen"): # Print output to main window.

            responsesGiven += 1
            
            window["-OUTPUT-"].print(message, text_color=text_color)
            window.refresh()

            if responsesGiven > 2:
                window["-TIPS-"].hide_row()

        if runVoice and message[0] != "[" and message[0] != "~": # Vocalise a message

            # Prepare message for vocalisation.
            message = message.replace("\\\'", "\'").replace("\\\"", "\"")
            message = message.replace("\".", "\"")
            message = message.replace("\n", " ")
            
            retort("Say: " + message) # Vocalise message.
            
            #window["-STATUS-"].update("Vocalising ...")
            window.refresh()
            print("Local Output.")

    else:
        remote = False

    return message


def insertTopic(Inp): # Insert a discerned topic into the input.
    topic = discernTopic(Inp) # Get the topic to be inserted.

    output = ""
    
    for word in Inp.split(" "): # Iterage through words in scentence.

        # Replace vague words with what they actually represent.
        if word.lower() in ["it", "it's", "its", "their", "his", "he", "her", "she", "their"]:
            output += topic
        else:
            output += word
        
        output += " "

    return output


# Variable placeholders for media functions.
player = None # VLC Media Player entity.
duration = 0 # [s] Duration of currently playing media
audioPauseTime = 0 # [s] Time media has been paused.
audioStartTime = 0 # [s since Epoch] time when audio started playing.
audioStartBuffer = 0 # Used to halt the progress bar whilst media is paused.
playIndex = -1 # Index in playlist.
choice = "None" # Currently playing media

def mediaPlay(inp="", playon=False): # Play a given media file.

    # Get relevant global var's
    global player, duration, audioPauseTime, audioStartBuffer, playing, playIndex, playlist
    global audioStartTime, working, choice, window

    volIncrement = "10%" # Increment by which volume is adjusted with 'volume up / down' command (Linux only).

    if time.time() - audioStartBuffer >= duration: # Current Audio is finished. 
        playIndex += 1 # Cycle to next in playlist.
        
        try: # Stop the audio in case it has not stopped its-self.
            player.stop() 
        except AttributeError: # Audio is already stopped, as if should be.
            pass
        
        playon = False # We need to start a new song not continue the last one.

    if not playon: # If we need to satrt a new sond not continue the last one.

        # Unmute the device, in case the user forgot to do so. Only works on linux
        if platform == "linux":
            process = Popen(["amixer", "-D", "pulse", "sset", "Master", "unmute"], stdout=PIPE, stderr=PIPE) 

        print("Playlist: ", playlist, playIndex) # Print the playlist that will be played.

        try: # Get the next media file from the playlist.
            choice = playlist[playIndex]
            print("Now playing", choice)
            
        except IndexError: # No more media files in playlist.
            output("Media ended.")

            # Reset media variables for next time.
            playlist = []
            playing = "False"
            working = "False"
            playIndex = 0 # Reset playlist index
            
            window["-MEDIA-GO-"].hide_row() # Hide media control buttons.
            
            return ""
        
        output("Playing " + choice, silent=True)

        # Change the play button to a pause button, because mefia is already playing.
        window["-MEDIA-GO-"].update(image_filename="graphics/Pause.png", image_subsample=3)
        window.refresh()

        player = vlc.MediaPlayer(choice) # Create player instance.
        player.play() # Start playing the selected media using VLC media player

        while player.get_length() == 0: # Wait for media file to load completely.
            window["-STATUS-"].update("Loading Meida ...")
            window.refresh()
            pass

        # Update the status indicatior for the currently playing media.
        if platform == "windows":
            window["-STATUS-"].update("Playing " + str(choice.split("\\")[-1]))
        elif platform == "linux":
            window["-STATUS-"].update("Playing " + str(choice.split("/")[-1]))

        audioStartTime = time.time() # Time that audio was first started
        audioPauseTime = 0 # [s] Time spent paused.
        audioStartBuffer = audioStartTime # Define the pause buffer.
        
        playing = "playing"
        window["-MEDIA-GO-"].unhide_row() # Show media control buttons.

        window.refresh()

        duration = player.get_length() / 1000 # Get settings("length") of track.
        print("Media Duration:", duration) 

    if playing == "paused": # If audio has been paused
        audioStartBuffer = audioStartTime + time.time() - audioPauseTime # Buf the buffer to prevent the progressbar prgressing.

    # Update the progressbar with the percentage through the currently playing track.
    progress = float(((time.time() - audioStartBuffer) / duration) * 100)
    window["-GEN-PROGRESS-"].update(progress)

    if not len(inp): # No command was given to the media.
        return ""

    if contains(inp, getSyns(["pause"])): # Pause the media.
        
        player.pause()
        output("Media paused.")
        audioPauseTime = time.time() # Begin paused timer.
        window["-STATUS-"].update("Audio Paused.")
        window["-MEDIA-GO-"].update(image_filename="graphics/Play.png", image_subsample=3)
        
        playing = "paused"


    elif contains(inp, getSyns(["resume"])): # Resume the paused media.
        
        player.play()
        output("Media resumed.")
        
        if platform == "windows":
            window["-STATUS-"].update("Playing " + str(choice.split("\\")[-1]))
        elif platform == "linux":
            window["-STATUS-"].update("Playing " + str(choice.split("/")[-1]))
            
        window["-MEDIA-GO-"].update(image_filename="graphics/Pause.png", image_subsample=3)
        
        playing = "playing"
        

    elif contains(inp, getSyns(["louder", "up"])): # Increase volume (Linux only)
        if platform == "linux":
            process = Popen(["amixer", "-D", "pulse", "sset", "Master", volIncrement + "+"], stdout=PIPE, stderr=PIPE)
            process = Popen(["amixer", "-D", "pulse", "sset", "Master", "unmute"], stdout=PIPE, stderr=PIPE)
            output("Increased volume by " + volIncrement, silent=True)

    elif contains(inp, getSyns(["quieter", "down"])): # Reduce volume (Linux only)
        if platform == "linux":
            process = Popen(["amixer", "-D", "pulse", "sset", "Master", volIncrement + "-"], stdout=PIPE, stderr=PIPE)
            output("Decreased volume by " + volIncrement, silent=True)

    elif contains(inp, getSyns(["mute"])): # Mute audio (Linux only)
        if platform == "linux":
            process = Popen(["amixer", "-D", "pulse", "sset", "Master", "mute"], stdout=PIPE, stderr=PIPE)
            output("Muted audio.", silent=True)

    elif contains(inp, getSyns(["unmute"])): # Unmute audio (Linux only)
        if platform == "linux":
            process = Popen(["amixer", "-D", "pulse", "sset", "Master", "unmute"], stdout=PIPE, stderr=PIPE)
            output("Unmuted audio.", silent=True)

            
    elif contains(inp, getSyns(["stop", "end"])): # Stop playing audio
        
        player.stop() # Stop the player.
        output("Media stopped.")

        # Reset media variabled for next time.
        playlist = []
        playing = "False"
        working = "False"
        playIndex = 0
        
        window["-MEDIA-GO-"].hide_row() # Hide media controls.


    elif contains(inp, getSyns(["next"])): # Play the next track in the playlist.
        
        player.stop() # Stop playing this track
        
        output("Iterating Media.")
        audioStartBuffer = 0

    elif contains(inp, getSyns(["back"])): # Restart the currently playing track
        
        player.stop() # Stop the player.
        
        output("Restarting Media.")
        duration = 0
        audioStartTime = 0
        playIndex -= 1

    else: # Send input back to generate a different type of response.
        
        window.refresh()
        return inp

    # Should never get here. This is just a contingency.
    window.refresh()
    return ""
        

def mediaPass(inp, playOnly): # Determined tpye of media to be played, then pass to backend.

    window["-STATUS-"].update("Opening  Media ...")
    window.refresh()

    out = ""

    if not playOnly: # May or may not be playing an audio file.
        
        splitInp = inp.lower().replace(".", " ").strip().split(" ")

        #print("Split for web domain check settings("length"): ", len(splitInp))

        if contains(inp.lower(), getSyns(["internet", "website", "site", "online"])): # Open media from the web.
        
            for domain in domains: # Check for site in popular domains.
                
                if domain.lower().split(".")[0] in splitInp:
                    
                    webbrowser.open(domain) # Open the site in the web browser.
                    output(affirm())
                    return 


        if not len(out): # Input was not a request to open a popular website.

            # Pass to backend generic commend to open file.
            retort("Open: " + inp) 
            working = "open"

    else: # Pass to backend with specifin instruction to play audio.
        
        retort("ToPlay: " + inp)
        working = "open"

    return "working"


asked = False

def respond(inp): # Determines type of response, then retrieves and returns that response.
    global loops, working, newGen, adventureStarted, asked
    global window, remote, secret, deline, trivia

    newGen = True # Generating a new response
    
    loops += 1 # Iterate response counter. Possibly superfluous.

    out = ""

    # Format the user input.
    inp = inp.lower()
    inp = inp.capitalize()

    if not contains(inp[-1], ["?", "!", "."]): # Add punctuation if the user did not.
        inp += "."


    #inp = insertTopic(inp) # Insert topic
    #inp = substitute(inp) # Substitute reflections

    print(inp)


    if contains(inp.lower(), ["open", "show", "document", "file"]) and not remote: # Open files.

        window["-STATUS-"].update("Opening file ...")
        mediaPass(inp.lower(), False) # Open a file.


    elif contains(inp.lower(), ["play ", "open ", "watch ", "music", "media"]) and not remote: # Open audio or video media.

        for word in ["play", "open", "watch", "music", "media"]:  # Remove original 'play' command.
            inp = inp.replace(word, "")
            
        inp = inp.replace("  ", " ") # Fix formatting isses caused by removing the play command.

        window["-STATUS-"].update("Opening file ...")
        mediaPass(inp, True) # Play audio or video media.

    elif not asked:
        asked = True
        retort("Respond: " + inp)

    return "working" # Return retrieved output.



def help_(): # Open .pdf help file
    webbrowser.open("https://github.com/Mblizzard/Tom-the-AI/blob/main/README.md")


def about(): # Display about window.
    webbrowser.open("https://github.com/Mblizzard/Tom-the-AI/blob/main/README.md")
    

settings("windowOpen", False) # Placeholder for if window is currently open.
runGIF = True # Can't recieve input and run gif at the same time.


def loadMainWindow(): # Loads the main program window.
    global runGIF

    runGIF = True # Can't recieve input and run gif at the same time.

    if settings("windowOpen"): # Bring Window into focus
        global window
        window.BringToFront() # I love how easy this is :)
        return window


    # Define element sixes by platform.

    if platform == "linux":
        buttonSize = 8
        buttonBg = "grey6"
        outputSize = (44, 28)
        fontSize = 10
        progressLen = 75
        inputSize = 43
        graphtop = 50
        imagetop = 50
        enterSize = 10
        boxColor = "grey5"
        graphSize = (400, 70)
        
    elif platform == "windows":
        buttonSize = 10
        buttonBg = "grey15"
        outputSize = (52, 30)
        fontSize = 11
        progressLen = 80
        inputSize = 53
        graphtop = 65
        imagetop = 60
        enterSize = 14
        boxColor = "grey10"
        graphSize = (380, 70)
        
        
    buttonPad = ((3, 3), (0, 0)) # Define padding for buttons.


    micImage = "graphics/microphone_light_blue.png"

    if settings("microphoneState") == "off":
        micImage = "graphics/microphone_white.png"
    

    # Defind layout of left hand side of window.
    
    LHS = [[sg.Column([[sg.Button("Modules", button_color=("light blue", buttonBg), key="-MODULES-", size=(buttonSize, None),
                                  font=(kernedFont, fontSize), pad=buttonPad),
                        sg.Button("Settings", button_color=("light blue", buttonBg), key="-SETTINGS-", size=(buttonSize, None),
                                  font=(kernedFont, fontSize), pad=buttonPad),
                        #sg.Button("Help", button_color=("light blue", buttonBg), key="-HELP-", size=(buttonSize, None),
                        #          font=(kernedFont, fontSize), pad=buttonPad),
                        sg.Button("About", button_color=("light blue", buttonBg), key="-ABOUT-", size=(buttonSize, None),
                                  font=(kernedFont, fontSize), pad=buttonPad),
                        sg.Button("Exit", button_color=("light blue", buttonBg), key="-QUIT-", size=(buttonSize, None),
                                font=(kernedFont, fontSize), pad=buttonPad, mouseover_colors=(None, "firebrick"))]],
                        expand_x=True, background_color="black", vertical_alignment="top",
                        pad=((0, 0), (0, 0)))],
           [sg.Image(tomFace, enable_events=True, background_color="black", key='-IMAGE-', pad=((0, 0), (imagetop, 0)))],
           [sg.Graph(graphSize, (0, 0), (samples, 100), background_color='black', key='-GRAPH-', pad=((0, 0), (graphtop, 5)),
                     tooltip="    Activity Graph:\n Purple: CPU Usage,\n Light Blue: Network Upload,\n Dark Blue: Network Download.")],
           [sg.HorizontalSeparator(color="black")],
           [sg.Column([[sg.Text("How can I be of assistance?", text_color="grey60", background_color="black", key="-STATUS-",
                        font=(kernedFont, fontSize), size=(None, 1), pad=((0, 0), (1, 0)))]],
                      element_justification="left", vertical_alignment="bottom", expand_y=True, expand_x=True,
                      background_color="black", pad=((0, 0), (0, 0)))]]


    # Defind layout of right hand side of window.

    RHS = [[sg.Multiline(size=outputSize, key="-OUTPUT-", default_text="Conversation transcript for this session:\n",
                         background_color=boxColor, text_color='grey60', autoscroll=True,
                         font=(kernedFont, fontSize), pad=((25, 0), (0, 0)))]]


    # Define main window layout.

    layout = [[sg.Column(LHS, background_color="black", element_justification="centre", pad=((0, 0), (0, 0))),
               sg.Column(RHS, background_color="black", element_justification="right", vertical_alignment="top",
                         pad=((0, 0), (0, 0)), expand_x=True)],
              [sg.ProgressBar(100, orientation="horizontal", size=(progressLen, 2), bar_color=["purple", "grey8"], key="-GEN-PROGRESS-",
                                 border_width=0, pad=((1, 1), (12, 10)))],
              [sg.Text("Type an input in the box below, or say \"" + settings("activationPhrase") + "\" to get started! ", # +
              #         "Try asking \"" + settings("activationPhrase") + " what can you do?\" for an overview of Tom's abilities.",
                       text_color="grey60", background_color="black", key="-TIPS-", font=(kernedFont, fontSize), size=(None, 1),
                       pad=((0, 0), (0, 3)))],
              [sg.Button(image_filename=micImage, image_subsample=13, key="-MICROPHONE-",
                         border_width=0, button_color=(None, "black"), mouseover_colors=(None, "grey1"),
                         pad=((0, 20), (0, 0))),
               sg.MLine(size=(inputSize, 3.4), key='-INPUT-', enter_submits=True,  do_not_clear=False, pad=((0, 0), (0, 0)),
                        background_color=boxColor, text_color='orchid1', autoscroll=True, font=(kernedFont, 15),
                        no_scrollbar = True,
                        #tooltip="Type an input here or say \"" + settings("activationPhrase") + "\" to get started!"
                        ),
               sg.Column([[sg.Button('Enter', bind_return_key=True, button_color=("orchid1", buttonBg), size=(enterSize, None),
                                     font=(kernedFont, fontSize), pad=((3, 3), (3, 3)))],
                           #sg.Button('Elaborate', button_color=("slateblue1", "grey10"), size=(7, None),
                           #          font=(kernedFont, 10), pad=((3, 3), (3, 3)), key="-ELABORATE-"),
                           #sg.Button('Clear', button_color=("grey90", "grey10"), size=(7, None),
                           #          font=(kernedFont, fontSize), pad=((3, 3), (3, 3)), key="-CLEAR-")],
                          [sg.Button(image_filename="graphics/Restart.png", key="-MEDIA-BACK-", image_subsample=3, border_width=0,
                                     button_color=(None, "black"), mouseover_colors=(None, "grey1")),
                           sg.Button(image_filename="graphics/Stop.png", key="-MEDIA-STOP-", image_subsample=3, border_width=0,
                                     button_color=(None, "black"), mouseover_colors=(None, "grey1")),
                           sg.Button(image_filename="graphics/Pause.png", key="-MEDIA-GO-", image_subsample=3, border_width=0,
                                     button_color=(None, "black"), mouseover_colors=(None, "grey1")),
                           sg.Button(image_filename="graphics/Next.png", key="-MEDIA-NEXT-", image_subsample=3, border_width=0,
                                     button_color=(None, "black"), mouseover_colors=(None, "grey1"))]],
                         background_color="black", pad=((5, 0), (0, 0)), expand_x=True, element_justification="centre")],
              #[sg.Column([[sg.Text("Tom the AI v" + str(tomVersion) + "; © Murray Jones, 2021.",
              #             text_color="grey60", background_color="black", key="-COPY-", font=(kernedFont, fontSize), size=(None, 1),
              #             pad=((0, 0), (0, 0)))]],
              #           background_color="black", pad=((0, 0), (0, 0)), expand_x=True, element_justification="right")]
              ]


    # Define main window parameters.

    window = sg.Window('Tom the AI (v' + str(tomVersion) + ')', layout,
            grab_anywhere=False,
            keep_on_top=False,
            background_color="black",
            alpha_channel=.98,
            finalize=True,
            icon="graphics/squareFace.png",
            margins=(25, 25))


    window['-INPUT-'].Widget.config(insertbackground='light blue') # Make the mouse cursor in the input box light blue.

    vbar = window['-OUTPUT-'].Widget.vbar # After window finalized
    vbar.configure(background="grey8")
    vbar.configure(troughcolor="purple")
    #vbar.configure(highlightcolor="yellow")
    #vbar.configure(highlightbackground="green")
    vbar.configure(troughcolor="black")


    window["-MEDIA-GO-"].hide_row() # Hide the media controls by default.

    window.refresh() # Update these changes to the window.

    window.BringToFront()

    settings("windowOpen", True)

    return window


# Start loading the user interface.

if not settings("startDown"):
    loadingWindow["-LOAD-TEXT-"].update("Loading interface...")
    loadingWindow.refresh()

notified = False

while True: # Wait for backend to be ready.

    fromBack = intort()
    
    if "Ready" in fromBack: # Backend is ready.
        print("Backend Ready")
        break

    elif not notified: # Change the loading status.
        if not settings("startDown"):
            loadingWindow["-LOAD-TEXT-"].update("Indexing local file system ...")
            loadingWindow.refresh()
        notified = True

    else: # Move the progressbar in accord with the estimated loading time.
        if not settings("startDown"):
            loadingWindow["-LOAD-PROGRESS-"].update(float(((time.time() - startTime) / estLoadTime*1.2) * 100))
            loadingWindow['-LOADGIF-'].update_animation(tomFace, time_between_frames=15) # Update the animation in the window
            loadingWindow.refresh()

    if "TELL: " in fromBack:
        if not settings("startDown"):
            msg = fromBack.split("TELL: ")[-1]
            loadingWindow["-LOAD-TEXT-"].update(msg)
        
            loadingWindow.refresh()
    #time.sleep(0.1)


if not settings("startDown"):
    window = loadMainWindow() # Load the main window once the backend is ready.

settings("estloadTime", time.time() - startTime)


def close(): # Closes the main window and exits the program.
    global window

    # Output a brief goodbye.
    partingWords = random.choice(getSyns(["goodbye", "bye"]))
    output(partingWords.capitalize() + ".", text_color='light blue')

    killZombies()

    time.sleep(1.5) # Give user a chance to read the goodbye message.
    window.close() # Close main window.
    time.sleep(1.5) # Wait for goodbye message fo finish vocalising.
    retort("Frontend Closed") # Close the backend and listener.
    exit() # Exit the frontent.
    

# Output a random greeting at runtime

greeting = ""

while True:
    greeting = random.choice(getSyns(["hello", "howdy"]))
    if not contains(greeting.lower(), ["hawai", "aloha"]): # Hawaii is not term most people would use as a greeting.
        break

output(greeting.capitalize() + ", " + username.capitalize() + ".", text_color='light blue')


loops = 0 # Counter of program responses. Possibly superfluous.

#print("Done Loading :)") # :)


# Initiate some global interface variables.
genStart = 0
lastIntermediaryRead = 0
lastMicrophoneClick = 0


def main(inp=""): # Main program function.-
    # Note: The system tray icon requires this function to be non-blocking.

    # Get all relevant variables as global.
    global loops, runGIF, playing, playlist
    global lastGraphUpdate, genTimes, newGen, remote, asked
    global lastMicrophoneClick, doubleClickInterval, systemGraphTool
    global working, newGen, genStart, lastIntermediaryRead, intermediaryReadInterval

    loops += 1 # Iterate loop counter

    # Placeholders for user inferface inputs.
    event = ""
    values = ""

    incoming = "" # Placeholder for data from backend

    if time.time() - lastIntermediaryRead > intermediaryReadInterval: # Check the intermediary for new data from the backend.
        incoming = intort()
        lastIntermediaryRead = time.time()


    if newGen: # Set the start time for ne response generation.
        genStart = time.time()
        newGen = False


    if len(str(incoming)) > 4: # Data has been recieved from backend.

        if "generated in " in str(incoming).lower() and not contains(working, ["False", "playing"]): # Finetune progressbars based on recent situation.

            genStat = float(incoming.split("Generated in ")[1][:5]) # Get the time taken to generate the last response.

            if genStat > 0.6: # Ignore instant or near instant responses.

                # Fietune the estimated generation time based upon the last generation time.
                settings(str(working) + "Time", float(settings(working + "Time") + genStat) / 2)
                print("New Time:", working, settings(working + "Time"))


            working = "False" # Generation is complete.

            if playing != "playing" and playing != "paused": # Reset loading bar if not playing audio.
                window["-GEN-PROGRESS-"].update(0)

            incoming = incoming.split("Generated in ")[0] # Clean incoming data incase other information is also present.


        if "GEN: " in incoming or "FALLBACK" in incoming:

            gen = "response"
            
            if "FALLBACK" in incoming:
                gen = "subjective_response"
            else:
                gen = incoming.split("GEN: ")[-1]
                gen = gen.replace("\\n", "\n")
                gen = gen.split("\n")[0]

            working = gen
                
            window["-STATUS-"].update("Generating " + str(gen).replace("_", " ") + ".")
            window.refresh()
            print("GEN, ", gen)


        if "Response: " in incoming: # Response recieved from backend.
            asked = False

            # Format incoming data to remove unwanted tags and syntax.
            incoming = incoming.split("Response: ")[1]
            
            #if "\", \'" in incoming:
            #    incoming = incoming.split("\", \'")[0]
            #elif "\', \'" in incoming:
            #    incoming = incoming.split("\', \'")[0]

            incoming = replaceAll(incoming, [["\\n\', \"", "\n"],
                                             ["\\n\', \'", "\n"],
                                             ["\\n\", \'", "\n"],
                                             ["\\n\", \"", "\n"]])

            out = output(incoming, text_color="light blue", silent=False) # Output the recieved response.
            print("Frem response", out)
            return out

        if "Play: " in incoming: # Pass from backend to frontend media player.

            # Format incoming data to locate playlist amidst framing syntax.

            if platform == "linux":
                
                playlistString = " ".join(incoming.split("Play: ")[1:])

                playlist = playlistString[3:-5].split("\\\', \\\'")

                if len(playlist) == 1 and "\", \"" in playlist[0]:
                    playlist = playlistString[3:-5].split("\", \"")

                if len(playlist) == 1 and "\', \'" in playlist[0]:
                    playlist = playlistString[3:-5].split("\', \'")


            elif platform == "windows":
                
                playlistString = " ".join(incoming.split("Play: ")[1:])
                
                playlistString = playlistString.replace("\\\\", "\\")
                playlistString = playlistString.replace("\\\\", "\\")

                playlist = ("C:" + "C:".join(playlistString.split("C:")[1:])).split("\\\', \\\'")

                if len(playlist) == 1 and "\", \"" in playlist[0]:
                    playlist = playlistString.split("\", \"")

                if len(playlist) == 1 and "\', \'" in playlist[0]:
                    playlist = playlistString[2:].split("\', \'")

                if len(playlist) == 1 and "\', \"" in playlist[0]:
                    playlist = playlistString[2:].split("\', \"")
                    
                
            for mediaIndex in range(0, len(playlist)): # Iterate through entries that we have identified as part of a playlist.

                if not len(playlist[mediaIndex]): # Remove null values.
                    continue

                if platform == "linux": # Add deliminator for local file system on linux.
                    if playlist[mediaIndex][0] != "/":
                        playlist[mediaIndex] = "/" + playlist[mediaIndex]

                    
            print("Playlist Length:", len(playlist))
            print("Playlist ", playlist)

            
            mediaPlay() # Play th media. This is a non-blocking function and must be called every loop.

            # Set var's to inddicate that media is playing.
            playing = "playing"
            newGen = True
            working = "playing"


        if "Error: " in incoming: # Errors are usually caught earlier than this. I've never seen one get to here.

            response = mbox("An error has occurerd whilst retrieving your response, rendering Tom unable to continue function. " + 
                            "We're really sorry about this. " + 
                            "Please restart Tom, and avoid giving the input that caused the error. " +
                            "The error code for this issue is \"" + str(incoming) + "\". Plese report this error, and the input that caused " +
                            "the error to the developer so that it can be rectified: murray.jones12@bigpond.com.",
                            "error", heading="Something went horribly wrong.", title="Fatal Error: " + str(incoming), buttons=["Ok"])

            if response == "Closed" or response == "Ok":
                 pass


    if settings("windowOpen") and not remote: # Catches main window events.

        if working == "False": # Clean old generation progress off progress bar.
            
            if playing != "playing" and playing != "paused": # Reset loading bar if not playing audio.
                window["-STATUS-"].update("Ready ...")
                window["-GEN-PROGRESS-"].update(0)
                
            else: # An attempt to fix a bug that occurred once, but that I was never able to reproduce.
                working = "playing"

        elif playing != "playing" and playing != "paused": # Update loading bar if not playing audio.

            estGenTime = settings(working + "Time")
                
            if estGenTime == None: # No estimated time, resort to a nominal value of 18 seconds.
                print("Gen time not found for", working)
                settings(working + "Time", 18) # Define this valus so that it can be finetuned in the future.
                estGenTime = 18

            # Update the progressbar.
            window["-GEN-PROGRESS-"].update(int(((time.time() - genStart) / (estGenTime * 1.3)) * 100))
            #time.sleep(0.02) # Possibly superfluous.


        # Read events and values from the window.
        
        if runGIF:
            event, values = window.read(timeout=readPeriod) 
        else:
            event, values = window.read()
            

        if time.time() - lastGraphUpdate > graphInterval: # Update the activity graph.

            cpuGraphMode = "cores" # default CPU graph modde.
            
            if not settings("detailedGraph"): # Apply the detailed graph setting if false.
                cpuGraphMode = "min"

            # Get the requested graph object from separate systemGraphTool module.
            systemGraphTool.sysGraph(window, window["-GRAPH-"], samples, CPU=cpuGraphMode, RAM=False, Disk=False, Net=True)
            
            lastGraphUpdate = time.time()


        # Here we start analysing our interface inputs and functions.

        if event == "-QUIT-" or event == "Exit": # User closed using one of the in window close buttons.
            close()
            

        elif event == sg.WIN_CLOSED: # User closed by using the window 'X' button
            if settings("quitToTray") == True and settings("discordServer") == False:
                settings("windowOpen", False)
                window.close()
                return
            else:
                close()

        elif event == "-SETTINGS-": # Edit program settings.
            systemGraphTool = editSettings(window, systemGraphTool)

        elif event == "-MODULES-": # Edit program settings.
            moduleBrowser()

        #elif event == "-HELP-": # Show help documentation
        #    help_()

        elif event == "-ABOUT-": # Show about documentation.
            about()

        elif event == "-MICROPHONE-": # User clickedthe microphone button.
            doubleClick = False # Placeholder for double click flag.
            
            if time.time() - lastMicrophoneClick < doubleClickInterval: # Check for double click.
                doubleClick = True

            if doubleClick and settings("microphoneState") != "passive": # Switch to passive mode.
                settings("microphoneState = passive")
                
                window["-MICROPHONE-"].update(image_filename="graphics/microphone_light_blue.png", image_subsample=13) # Change the button image.
                
                if not settings("useVoice"):
                    settings("useVoice = 1")
                    output("Passive voice recognition and vocalisation enabled.")
                    
                else:
                    settings("useVoice = 1")
                    output("Passive voice recognition enabled.")

            else:
                
                if settings("microphoneState") == "passive" or settings("microphoneState") == "active": # Switch off voice recognition.
                    
                    settings("microphoneState = off")
                    settings("useVoice = 0")
                    
                    window["-MICROPHONE-"].update(image_filename="graphics/microphone_white.png", image_subsample=13) # Change the button image.
                    output("Voice recognition and vocalisation disabled.", silent=True)
                    
                elif settings("microphoneState") == "off": # Switch to active mode.
                    
                    settings("microphoneState = active")
                    settings("useVoice = 1")
                    
                    window["-MICROPHONE-"].update(image_filename="graphics/microphone_purple.png", image_subsample=13) # Change the button image.
                    output("Listening...", silent=True)


            lastMicrophoneClick = time.time()


        elif event == "-MEDIA-BACK-": # Restart media.
            mediaPlay("back", True)

        elif event == "-MEDIA-NEXT-": # Iterate media
            mediaPlay("next", True)

        elif event == "-MEDIA-STOP-": # Stop playing media.
            mediaPlay("stop", True)
            window["-GEN-PROGRESS-"].update(0) # Reset progress bar.
            
        elif event == "-MEDIA-GO-": # Pause or resume media.
            
            if playing == "playing": # Pause media
                
                playing = "paused"
                mediaPlay("pause", True)

            elif playing == "paused": # Resume  media.
                
                playing = "playing"
                mediaPlay("resume", True)


        inp = "" # Placeholder for text or voice input.

        window['-IMAGE-'].update_animation(tomFace, time_between_frames=gifPeriod) # Update the animation in the window
        window.refresh()

        string = values['-INPUT-'].rstrip() # Get text input from UI

    
        if len(string) and "an input here" not in string: # Input ic currentlybeing typed in text input box.
            
            if runGIF: # Stop to record input
                
                runGIF = False # Stop to record input as it is typed.
                
                l1 = string # Give back first letter that was captured to recognise that an input has commenced.
                window["-INPUT-"].print(l1, end="", text_color="orchid1")

            else: # Input has been entered.
                
                inp = string
                runGIF = True
                
                output("~>  " + inp, text_color="orchid1") # Output to conversation transcript
            
        else:
            runGIF = True # Contingency. runGIF should already be  True at this stage.


    if not len(inp) and settings("cam") and runGIF and "Emotion: " in incoming and not remote: # Get a emotion from the camera.
        
        incoming = incoming.lower()
        incoming = incoming.split("emotion: ")[1].split(".")[0]

        if "ing" not in incoming:
            output("You look " + incoming.split("i am ")[1] + ".", silent=True)

        inp = incoming.capitalize()
        

    if not len(inp) and settings("useVoice") and runGIF and "Heard: " in incoming and not remote: # Get a voice input from the listener.

        # Format input.
        incoming = (incoming.lower()).replace(lastVocalisation.lower(), "") # Try to avoid hearing last vocalisation.
        incoming = incoming.strip()


        if len(incoming) > 2: # Avoid inputs that are definitely too short. 

            inp = str(incoming) # Ensuure we are dealing with a string.

            try: # Try to get required part of input.
                inp = inp.split("heard: ")[1]
            except Exception as e: # Should never happen.
                print(e)

            # Format voice input to remove extra syntax that arose from being passed through a .txt file.
            inp = inp.split(" \\n")[0]
            inp = inp.split("\\n")[0]
            inp = inp.replace("\"", "")

            inp = inp.capitalize() # Capitalise input.

            print("Heard: " + inp) # Print what we heard to shell.


            if settings("microphoneState") != "off": # Ignore voice inputs if we were not meant to be listening.
                
                if (settings("activationPhrase") in inp.lower() or settings("microphoneState") == "active"): # Check for the activation phrase

                    settings("useVoice = 1") # If voicce input was iused, we shoulduse a voice output.
                    
                    if inp.lower() != settings("activationPhrase"): # Remove the activation phrase from the input.
                        inp = inp.lower().replace(settings("activationPhrase"), "").strip().capitalize()

                    lastVoice = time.time()

                    output("~> " + inp, text_color='orchid1') # Output the input that we heard.

                    
                else: # Output what we heard, bu don't respnd  to it because there was no activation phrase.
                    
                    output("I heard \"" + inp + "\"", silent=True)
                    return


                if settings("microphoneState") == "active": # End active voice recognition.
                    
                    settings("microphoneState = off")
                    settings("useVoice = 0")
                    
                    window["-MICROPHONE-"].update(image_filename="graphics/microphone_white.png", image_subsample=13) # Change button image.


    if playing == "playing" or playing == "paused" and not remote: # As media player is non blocking, we have to call it every loop whilst playing media.
        inp = mediaPlay(inp=inp, playon=True)

    
    if len(inp): # Respond to input. 

        # Handle direct commands
        
        if "voice" in inp.lower() and not remote: # Change voice recognition mode.
            
            if contains(inp, getSyns(["on", "activate", "passive"])): # Activate passive voice recognnition.
                settings("microphoneState = passive")
                
                window["-MICROPHONE-"].update(image_filename="graphics/microphone_light_blue.png", image_subsample=13) # Change button image.
                
                if not settings("useVoice"):
                    settings("useVoice = 1")
                    output("Passive voice recognition and vocalisation enabled.")
                    
                else:
                    settings("useVoice = 1")
                    output("Passive voice recognition enabled.")
                    
                return

            elif contains(inp, getSyns(["off", "deactivate"])): # Deactivate voice recognition.
                
                settings("microphoneState = off")
                settings("useVoice = 0")
                
                window["-MICROPHONE-"].update(image_filename="graphics/microphone_white.png", image_subsample=13) # Change button image.
                output("Voice recognition and vocalisation disabled.", silent=True)
                

        elif contains(inp.lower(), ["exit", "quit", "close", "kill"], wholeWord=True) and not remote: # Quit the program.
            close()

        elif "help" in inp.lower() and not remote: # Display help documentation.
            help_()
            return output(affirm(), text_color='light blue')


        out = respond(inp) # Pass input to respose function.

        if out == "working": # Run gif whilst generating respnses.
            working = "working"
            runGIF = True

        else: # Output response.
            runGIF = True
            return output(out, remote, text_color='light blue')


def editSettingsLink():
    systemGraphTool = editSettings(systemGraphTool)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon): # Handles the system tray icon.

    def __init__(self, icon, parent=None): # Defines parameters for system tray icon

        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        
        menu = QtWidgets.QMenu(parent) # Define parameters for system tray icon right click menu.
        
        self.setToolTip("Tom")
        
        openInterface = menu.addAction("Open Interface")
        #helpAction = menu.addAction("Help")
        aboutAction = menu.addAction("About")
        modulesAction = menu.addAction("Modules")
        settingsAction = menu.addAction("Settings")
        exitAction = menu.addAction("Exit")
        
        self.setContextMenu(menu) # Creates system tray icon righht click menu.
        
        openInterface.triggered.connect(loadMainWindow)
        #helpAction.triggered.connect(help_)
        aboutAction.triggered.connect(about)
        modulesAction.triggered.connect(moduleBrowser)
        settingsAction.triggered.connect(editSettingsLink)
        exitAction.triggered.connect(close)
        
        self.update() # Run the udate methof on first load.

    def update(self): # This forms the main window loop
        
        cycleTime = 0 # Do not have a delay. This would only cause lag.

        main()

        QtCore.QTimer.singleShot(cycleTime, self.update) # Iterates Loop.


def startTrayIcon(): # Starts PyQt5 class iteration, required for system tray icon.
    
    app = QtWidgets.QApplication(sys.argv) # Setup PyQt5 application entity.

    widget = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("graphics/squareFace.png"), widget) # Create the system tray Icon from its class.

    trayIcon.show() # Display the system tray Icon.

    if not settings("startDown"):
        loadingWindow.close()
    
    app.exec_() # This is blocking, repeatedly callls the update() method until program is closed.


#settings(discordServer, False)

if settings("discordServer") == True:
    if not settings("startDown"):
        loadingWindow["-LOAD-TEXT-"].update("Connecting to Discord ...")
        loadingWindow.refresh()

    client = DiscordClient()
    print("Running Client...")
    client.run(TOKEN)

else:
    if not settings("startDown"):
        loadingWindow["-LOAD-TEXT-"].update("Connecting to System Tray ...")
        loadingWindow.refresh()

    startTrayIcon()


print("Done.")
