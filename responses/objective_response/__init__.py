from ioUtils import *

def objectiveResponse(inp): # Get webernet results for a given input

    result = -1 # Placeholder for result itteration
    retries = -1 # Will hold current retry count.

    searchAttempts = 1 # Holds  search engiine retry coount.
    maxSearchAttempts = 4 # Max. search engine retries.
    sentenceCount = 3
    scrapeRetries = 7
    length = 250 # [chars]

    searchResults = findURLs(inp) # Get initial search enging results for input.

    while len(list(searchResults)) < 1: # No search results have been found.

        searchResults = findURLs(inp) # Try to get search enging results for input.

        searchAttempts += 1 # Iterate counter.

        print("Found " + str(len(searchResults)) + " pages to query for objective response to query \"" + inp + "\".")

        if searchAttempts >= maxSearchAttempts: # findURLs() did not find any URL's from search engine after tyring as many timesas it was allowed.

            if not len(searchResults): # No search results foound.
                print("Response: I could not find search results for your objective query.")

                return False
            else: # Search results were found.
                break
        else: # Keep trying to find search results.
            continue


    if len(searchResults) < scrapeRetries: # Limit scrape setries to number of search results found.
        scrapeRetries = len(searchResults)


    while 1: # Loop for retries on search results.
        
        # Iterate result & retry count.
        result += 1
        retries += 1

        if retries >= scrapeRetries: # None of the requests succeeded.
            print("Response: I could not find results on the internet for your objective query.")
            return False

        print("Scraping " + searchResults[result] + " for objective response.")

        try: # Try to retrieve web page content
            page = requests.get(searchResults[result], "html.parser", headers=getHeaders()) 
        except: # Web scraping failed.
            continue # Try again.

        soup = BeautifulSoup(page.content, features="html.parser") # Parse html

        paras = str(soup.find_all("body")) # Find <p> paragraph tags.

        paras = paras.replace("<br>", "\n") # Replace HTML line breaks with ASCII newline character.

        paras = paras.replace(">", "> ").replace(")", ") ").replace("}", "} ").replace("]", "] ") # Reformat text near brackets before they are removed.

        # Remove all brackets of any description!
        paras = removeMarkup(paras, "<", ">")
        paras = removeMarkup(paras, "(", ")")
        paras = removeMarkup(paras, "{", "}")

        paras = paras.replace(" , ", ", ").replace("  ", " ") # Fix formatting issues cause by removing brackets.


        for para in paras.split("\n"): # Cycle through paragraphs within the <p> tag.

            para = removeMarkup(para, "[", "]") # Remove square blackets on a per paragraph basis.

            # Fixes a wierd bug that caused crashes on non-www. websites, e.g. www3. sites, includiing UAC.
            para = para.replace("\xa0", " ")
            para = para.replace("\\xa0", " ")

            if len(str(para)) < 20: # Paragrapg is too short to be useful.
                continue # Skip it.

            # Words used to identify and ignore eleements such as "this website uses cookies" banners.
            killWords = ["jump to ", " .mw-", "•", "=", "^", "\\xa0", "\":\"", "@", "style rules", "._", " - ", " store ", "place of origin",
                    "citation", "update", "this article", "learn more.", " support", "review", "official portrait", "what is ", "@", ":",
                    ".pfroducts", "gories:", " purchase ", "editor", "blog", "redirect", "born", "citation", "video", "learn more", "•",
                    "&amp", "worksheet", "survey", "deutsch", "italiano", "polski", "norsk", "slovak ", "loading", "created by", "etc.",
                    "This article is about ", "first appearance", "am single", "am a single", "publish", "cookie", "sign up", "guide",
                    ".Mui", ".Recirc", ".cls-1", "cookies", " .ib-", "author of ", "up-to-date", "Click on ", "CAPTCHA", "new study",
                    "inclusive", "don't miss out", "free trial", "learning more", "more about", " journal ", "Improve your ",
                    "frequently asked questionse", "official website", "this chart ", "trending", "britannica", "% European", "dedicated",
                    " lisccenced ", "creative commons", "talk page", "subscribe", "click here", "for other uses", "see the tip below",
                    "the full article", "photograph of ", "reference", "no.", "register", "\u200b", "\\u200b", ".com", "/ \'", "This page ",
                    "promotional", "earn money", "product", "cover of", "not to be confused with", "1.2.", "1.1.", "1.3.", "login",
                    "acknowledge", "\ufeff", "show ", " style manual ", "&gt"]

            killed = False # Flag to determine of a killword has been found.

            for killWord in killWords: # Iterate through killwords.

                if killWord.lower() in str(para).lower() or killWord in str(para): # Check if killword in paragraph
                    print("Rejected " + str(para).lower() + " for \"" + killWord + "\" Killword")
                    #print("Rejected for \"" + killWord + "\" Killword")

                    killed = True # Set flag.
                    break # Don't check for moe killwords if we have already found one.

            if killed: # Ignore paragraphs with killwords
                continue # Skip it.

            if len(para.split(" ")) < len(para) / 25: # Paragraph has too few spaces to be useful text.
                print("Rejected " + str(para).lower() + " block text.")
                continue # Skip it.

            # Get a summary up to sentenceCount variable, to the nearest whole scentence.
            summary = str(". ".join(para.split(". ")[:sentenceCount])).strip() + "." 
            
            if not len(summary): # 1st scentence was longer than user set length.
                summary = para.split(". ")[0] # Get first scentence.

            if len(summary) < length / 3: # Paragraph was too short to be useful, but long enough to evade our earlier check.
                print("Rejected " + str(para).lower() + " too short.")
                continue # Skip it.

            out = str(summary).strip() # Remove trailing wwhitespace.

            if len(out) < 10: # Paragraph was mostly whitespace.
                continue # Skip it.

            loc = str(searchResults[result].split("://")[1].split("/")[0]).strip() # Get the site that the suummary came from.
            citation = "According to " + loc + " ...\n"

            out = citation + out
            
            return out

        else: # No valid paragraphs foound on this webpage.
            continue # Retry.
    
        break # Contingency. Should never be called.


def respond(inp):
    if isQuestion(inp.lower()) and not contains(inp.lower(), ["there"]): # Get an objective respense from the web.
        out = objectiveResponse(inp)
        return out
    
    else:
        return False

if __name__ == "__main__":
    while 1:
        print(respond(input("> ")))
