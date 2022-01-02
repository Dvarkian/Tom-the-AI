Tom the AI (v1.0)
=================

Tom is an open source AI desktop assistant for Linux systems, built using a series of independent response modules to generate replies to any input. 

Tom uses natural language processing to determine which response module is best suited to generate a response for each input, thus avoiding the need for precise syntax.

![UI Screenshot](https://github.com/Mblizzard/Tom-the-AI/blob/main/graphics/screenshot1.png)

Note: Tom is tested on Ubuntu 22.04. It *should* work fine on other Linux systems, but some minor tweaking may be required to the method of installling dependencies.

By Analogy
----------

Tom the AI is designed as a Linux alternative to software such as Apple's Siri, or Microsoft's Cortana.


Set Up
------

**Step 1 - Update repositories:** 

Update apt package repositories using `sudo apt update` to ensure that the apt package manager has access to the latest versions of the below dependencies.

**Step 2 - Install APT dependencies:** 

First, install python by running `sudo apt install python3.9` in a terminal. Tom is tested on python 3.9, but any newer version should (probably) also work just fine.

Next, install the latest version of VLC Media player using `sudo apt install vlc`.

**Step 3 - Download Tom**: 

Download Tom by cloning the GitHub repository into your home folder using `git clone https://github.com/Mblizzard/Tom-the-AI`.

**Step 4 - Install Python dependencies:** 

Open a terminal inside Tom's application folder, or navigate using `cd ~/Tom-the-AI/`. Now run `sudo pip3 install requirements.txt`. Some systems may use `pip` in place of `pip3`.

Next, we need to download the required NLTK libraries by running the following code in a python shell:

```python
>>> import nltk
>>> nltk.download('all')
```

**Step 5 - Running Tom:** 

Go ahead and run `python3.9 ~/Tom-the-AI/frontend.py`. Tom will boot up, and after a minute or so of loading, you'll be ready to go! If you feel inclined, go ahead and make a desktop launcher of this command, link Tom into your Application Menu, or create a dock shortcut.


Mission
-------

The mission of Tom is to provide an open source compound AI for which anyone can program and contribute response modules, expanding Tom's capabilities to create a useful and entertaining artificial intelligence software.


Features
--------

Tom generates outputs to any input by using natural language processing to determine the most suitable response module from which to source the reply.

Give Tom natural language input, either via voice recognition or text input, for instance `Hey Tom, what is petrichor?`, and he'll respond in the most appropriate way. Note that the 'Hey Tom' activation phrase is only required of voice inputs. Passive voice input can be activated by double clicking the microphone button. Single click to use voice recognition for a single input.

![Tom the AI](https://github.com/Mblizzard/Tom-the-AI/blob/main/graphics/tomFace_original.gif)

The following is a non-exhaustive list of Tom's capabilities:

*Objective Response (From anywhere on the internet):*
    
    ~> Hey Tom, what is petrichor?
    According to en.wikipedia.org... Petrichor is the earthy scent produced when rain falls on dry soil. The word is constructed from the Greek petra, "rock", or petros, "stone", and ichor, the fluid that flows in the veins of the gods in Greek mythology.

*Subjective Response (From Cleverbot):*
    
    ~> Hey Tom, I'm in an optimistic mood.
    I'm not sure if this is a good thing or not.

*Emotions (Using sentiment analysis + NLTK chatbots):*
    
    ~> Hey Tom, you are a brilliant individual!
    I am but one, you are but one more.
    ~> Hey Tom, thou art a fool.
    Become more interesting before I die of fatal boredom.

*Fact Memory & Recall:*
    
    ~> Hey Tom, the answer to life, the universe, and everything is 42.
    Ok.
    ~> Hey Tom, what is the answer to life, the universe, and everything?.
    The answer to life, the universe, and everything is 42.


*Playing music (From device or web, includes UI controls for the former):*

    ~> Hey Tom, play up the shard.
    Playing /home/murray/Music/Dr Who/Up The Shard.webm.
    ~> Hey Tom, stop the music.
    Media stopped.
    *NOTE: File names do not have to match exactly.*

*Opening Files:*

    ~> Hey Tom, open my English essay.
    Alright.
    *NOTE: File names do not have to match exactly.*

*Opening websites:*
    
    ~> Hey Tom, open Reddit.
    Alright.

*Jokes (From PyJokes):*
    
    ~> Hey Tom, tell me a joke.
    I went to a street where the houses were numbered 8k, 16k, 32k, 64k, 128k, 256k and 512k. It was a trip down Memory Lane.

*Trivia:*
    
    ~> Hey Tom, ask me a trivia question.
    Question: What is "Sealed crustless sandwich"?
    1) The part of Yellowstone National Park in Idaho, where any crime can technically be committed without punishment – but don't tempt fate!
    2) I got a fever, and the only prescription... is more cowbell!
    3) The only nuclear reactor in a 17th-century building.
    4) A patented peanut butter and jelly sandwich.
    ~> 4.
    Correct!

*Colossal Cave Adventure (Willie Crowther's ADVENT-350):*
    
    ~> Hey Tom, let's go on an adventure!
    Welcome to adventure!! would you like instructions?

*Fun facts:*
    
    ~> Hey Tom, make me smarter.
    Spices were not used to mask the flavor of rotting meat before refrigeration. Spices were an expensive luxury item; those who could afford them could afford good meat, and there are no contemporaneous documents calling for spices to disguise the taste of bad meat.

*Dice Rolls (great for D&D):*
    
    ~> Hey Tom, roll me a d20.
    I rolled a 14.

*Word generation (great for Articulate)*
    
    ~> Hey Tom, give me a random action word.
    Your word is 'winning'.

*Complex Mathematics (using SymPy):*
    
    ~> Hey Tom, integrate (tan(x))^1/2
    ∫f(x) = -ln(cos(x))/2 + c

*Code generation (using howdoi):*
    
    ~> Hey Tom, write a hello world script in C++.
    #include <\iostream>
    int main()
    {
    std::cout << "Hello World!" << std::endl;
    return 0;
    }

*Most of Betty's functionality (From https://github.com/pickhardt/betty):*

    ~> Hey Tom, what time is it?
    Running date +"%r (%T)" ...
    02:34:46 PM (14:34:46).
    ~> Hey Tom, what day is it?
    Running date +"%A" ...
    Saturday.
    ~> Hey Tom, whats my username?
    Running whoami ...
    murray
    ~> Hey Tom, what is my ip address?
    Wlo1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500
        inet 192.168.43.9 netmask 255.255.255.0 broadcast 192.168.43.255
        inet6 fe80::5c61:caf:5614:7b82 prefixlen 64 scopeid 0x20<link>
        ether 54:35:30:60:a8:b9 txqueuelen 1000 (Ethernet)
        RX packets 401121 bytes 523184185 (523.1 MB)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 235650 bytes 23471151 (23.4 MB)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0.

This is a fair representation of Tom's capabilities as they currently stand. See the following section on contributing for a guide of how to create your own response modules for Tom, and expand upon the above abilities.


Contributing
------------

How to write a custom response module for Tom:

**Step 1 - Understanding how Tom will treat your module:** 

Tom is programmed in Python. Response modules are imported into Tom using the python `import <response_module>` statement, and the response is retrieved from the module using `output = <response_module>.respond(<user_input>)`. The output is then returned to the user.

**Step 2 - Programming the response module:** 

Go ahead and program your response. Your script should have a main function `def respond(inp):`, where inp is the user input parameter that will be passed to your function by Tom. Your function should provide it's output through a `return` statement (*NOT* a `print()` statement).

**Step 3 - Testing your module:** 

Paste the following bit of code at the end of your python script, then run your program:

```python
if __name__ == "__main__":
    while True:
        print(respond(input("~> ")))
```

If this works as expected, and you can type inputs on the `~>` prompts and receive your output printed in the console, then continue to step 4.

**Step 4 - Relative imports**: 

Rename your main response script to `__init__.py`, and make sure it's at the first level of your project folder (not nested in other folders). Next, rename the folder containing your script to the name of your module (no white-space or special characters). Now, if you are importing any functions from other scripts (does not include dependencies installed through pip), you will need to change the import statement by placing a '.' in front of the location. For example, `from myOtherScript import customFunction` becomes `from .myOtherScript import customFunction`, but `import requests` would remain unchanged.

**Step 5 - Dependencies:** 

If your response module requires python packages from PyPi, make sure it includes a `requirements.txt` file. Any dependencies not available from PyPi should bundled with project, located in the project folder alongside `__init__.py`.

**Step 6 - Using your module:** 

Paste the folder containing your response module into Tom's `/responses` directory. You will then need to activate the response module within Tom's modules interface, or by manually adding the name of your module to `responseOrder.txt`. 

**Step 7 - Creating a pull request:** 

If you feel inclined to share your module with the world, go ahead and create a pull request for your module on Tom's GitHub repository (`https://github.com/Mblizzard/Tom-the-AI`).


Planned Features
----------------

New response modules & capabilities to look forward to in future versions of Tom:

 - Timers & stopwatch capabilities.
 - Ability execute terminal commands.
 - Automated module installation.
 - Releases and updates available on the Ubuntu apt repositories.


Features I'm not currently planning to include in Tom, but that I'll consider adding if enough people are interested:

 - Windows support.
 - Easier discord setup (more on this below). 

**Versioning:** Releases will follow a [semantic versioning format](http://semver.org/): `<major>.<minor>.<patch>`


Discord Bot
-----------

Tom is set up to run as a locally hosted Discord bot. Unfortunately I am unable to host this bot full time, and I am yet to find a freely availiable web host for Discord bots. Therefore, to use this functionality, you will need to set up your own Discord Bot at the [Discord Developer Portal](https://discord.com/developers), and insert your bot token and guild name at the indicated positions around line 310 in `frontend.py`. 

If anyone has a server and would like to host Tom as a full time Discord bot, by all means go ahead. All the necessary programming is already complete.


Final Notes
-----------

I started developing Tom the AI in early 2021 as a major work for the HSC Software course. Since submitting the assigment, and getting full marks :), I have kept developing Tom over the past year as a hobby - a bit of fun to take my mind off lockdowns and to have a break in between studying for HSC exams. Tom is not perfect, but I think it's pretty cool. I hope that as more people contribute and help to develop response modules, Tom will grow to become a truly amazing piece of software that everyone can enjoy.


License
-------

    Tom the AI: A compound AI for Linux systems.
    Copyright (C) 2021  Murray Jones

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
