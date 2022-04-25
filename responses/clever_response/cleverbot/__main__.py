from sys import argv

from .cleverbot import Cleverbot


def chat():
    """
    Chat with Cleverbot.
    """
    bot = Cleverbot()
    print("Start the conversation, press Ctrl-c to stop \n")
    try:
        while True:
            print(bot.send(input(">> ")))
    except KeyboardInterrupt:
        print("Exiting.")


def self_chat():
    """
    This function makes cleverbot chat with itself.
    """
    alice = Cleverbot()
    bob = Cleverbot()
    message = "Hi there! How are you doing?"
    print("Press Ctrl-c to stop \n")
    try:
        while True:
            print("Bob: ", message)
            message = alice.send(message)
            print("Alice: ", message)
            message = bob.send(message)
    except KeyboardInterrupt:
        print("Exiting.")


if __name__ == "__main__":
    if len(argv) == 1:
        chat()
    elif len(argv) == 2 and argv[1] == "auto":
        self_chat()
    else:
        print("Usage: python -m cleverbot [auto]")
