# sentiment.py
# A sentiment analyser, and a few associated utilities.
# Programmed by Murray Jones (murray.jones12@bigpond.com)
# Completed 21/06/2021


# NLTK packages to import.
from nltk.corpus import wordnet # Offline Dictionary
from nltk.corpus import stopwords # Allows the ignoration of superfluous linguistics


def depunctuate(x): # Removes all forms of punctiation from a string.
    x = x.replace(".", "")
    x = x.replace("!", "")
    x = x.replace(",", "")
    x = x.replace(";", "")
    x = x.replace("?", "")
    x = x.replace(":", "")
    x = x.replace(")", "")
    x = x.replace("(", "")
    x = x.replace("\"", "")
    x = x.replace("\'", "")
    x = x.replace("[", "")
    x = x.replace("]", "")
    x = x.replace("-", "")
    x = x.replace("\n", " ")
    x = x.replace("   ", "")
    x = x.replace(" ", "")

    return(x)


DefnRecursion = 1 # Level of definition recursion.

def relateDefn(dWords): # Relate a list of words to thhe words in their definitions.
    
    results = [] # Willl hold list of associated words.
    
    for i in dWords: # Iterate through list of words.
        i = depunctuate(i) # Depunctuate the word.

        syns = wordnet.synsets(i) # Get synonyms for the word as NLP entities.

        for focus in range(0, DefnRecursion): # Preference words at shallower recursion depths
            results.append(i.lower()) # Append word to list.

        try: # Locatte a definition for the word
            definition = syns[0].definition()
        except: # Word hhas no definition.
            definition = ""
              
        definition = depunctuate(definition) # Depunctuate the defintion.
            
        for n in definition.split(" "): # Iterate through words in definition.
            n = n.strip(" ")

            if n.lower() not in stopwords.words('english') and len(n.lower()) > 1: # Allow bigger stopwords
                results.append(n.lower()) # Append related word from definition to associated words list.

    return results # Return list of associated words.


def word_feats(words): # Returns feats of given words.
    return dict([(word, True) for word in words])


def sentiment(string): # Determine the net sentiment of a given string.

    # Load positive and negative words databases.

    positive_db = open("positive-words.txt", "r")
    
    positive_vocab = []
    
    for positive_word in positive_db:
        positive_vocab.append(positive_word)
        
    positive_db.close()

    negative_db = open("negative-words.txt", "r")
    
    negative_vocab = []
    
    for negative_word in negative_db:
        negative_vocab.append(negative_word)
        
    negative_db.close()
    

    # Placeholders for positive and negative sentiment components.
    neg = 0.0
    pos = 0.0
    

    #words = definitionFunctions.relateDefn(string)
    words = string.split(" ") # Format string into a list.
    

    for word in words: # Iterate through each word in the list
        
        word = depunctuate(word)
        
        if (word + "\n") in positive_vocab:
            pos += 1
        
        elif (word + "\n") in negative_vocab:
            neg += 1


    # Balance sentiment to length of input.
    Pos = float(pos) / len(words)
    Neg = float(neg) / len(words)

    return Pos - Neg # Return net sentiment.


