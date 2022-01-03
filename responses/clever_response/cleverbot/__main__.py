from .cleverbot import cleverbot

if __name__ == "__main__":
    print("Start the conversation, press Ctrl-c to stop \n")
    try:
        while True:
            print(f"Bot: {cleverbot(input('>> '), session='main')}")
    except KeyboardInterrupt:
        print("Exiting.")
