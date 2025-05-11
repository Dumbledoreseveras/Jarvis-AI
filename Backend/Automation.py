from AppOpener import close, open as appopen    # Import function to open and close apps
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os


env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")     # Retrive the Groq API Key

# Define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKOO SY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
            "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", 
           "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LwkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]
     
 
# Defibre a user-agent for making acb requests. 
useragent =  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

#Initialize the Greg client with the API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional response for user interaction.
professional_responses = [
    "Your satisfation is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]

messages = []

# System message to provide contextto the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letter"}]

# Function to perform a Google search.
def GoogleSearch(Topic):
    search(Topic)       # use pywhatkit's search function to perform a Google search.
    return True     #indiacte success.

# function to generate content using AI and save it to a file.
def Content(Topic):

    # Nested function to open a file in notepad.
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'     # Default text editor
        subprocess.Popen([default_text_editor, File])   #Open the file in notepad

    # Nested function to generate content using the AI chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})   # add the user's prompt to messages.

        completion = client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            messages = SystemChatBot + messages,
            max_tokens = 2048,
            temperature = 0.7,
            top_p = 1,
            stream = True,
            stop = None
        )

        Answer = ""     # intialize an empty string for the response


        # process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # check for content in the current chunk
                Answer += chunk.choices[0].delta.content # Append content to the answer.

        Answer = Answer.replace("</s>", "")     # Remove "content" from the topic
        messages.append({"role": "assistant", "content": Answer})   # Add the AI's response to messages
        return Answer
    
    Topic: str = Topic.replace("Content ", "")# remove "content" from the topic.
    ContentByAI = ContentWriterAI(Topic) # Generate content using AI.

    #save the genarated content to a text file.
    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding= "utf-8") as file:
        file.write(ContentByAI)     # write the content to the file.
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")  # open the file in notepad
    return True     #indicate success.

# function to search for a topic on youtube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"    # construct the Youtube search URL.
    webbrowser.open(Url4Search) #open the search URL in a webbrowser.
    return True     #Indicate success.

# function to play video in youtube.
def PlayYouTube(query):
    playonyt(query) # Use pywhatkit's playonyt function to play the video.
    return True     #Indicate success.

# Function to open an application or a relevant webpage
def OpenApp(app_name, sess=requests.session()):
    try:
        print(f"Trying to open app: {app_name}")
        appopen(app_name, match_closest=True, output=True, throw_error=True)
        return True

    except Exception as e:
        print(f"Could not open app '{app_name}'. Trying website instead. Reason: {e}")

        def search_bing(query):
            url = f"https://www.bing.com/search?q={query}+official+site"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            return None

        def extract_links(html):
            soup = BeautifulSoup(html, 'html.parser')
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith("http") and "microsoft" not in href and "bing" not in href:
                    links.append(href)
            return links

        html = search_bing(app_name)
        links = extract_links(html)

        if links:
            webbrowser.open(links[0])
            print(f"Opened website for '{app_name}': {links[0]}")
            return True
        else:
            print(f"No website found for '{app_name}'")
            return False



# function to close an application
def CloseApp(app):

    if "chrome" in app:
        pass    # skip if the app is chrome.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)   # attempt to close the app.
            return True     # indicate success.
        except:
            return False        #indicate failure.
        
# function to execute system level commands.
def System(command):

    # nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")   # simulate the mute key press.
    
    # nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume unmute")   # simulate the unmute key press.

    # nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up")   # simulate the unmute key press.

    # nested function to decress the system volume.
    def volume_down():
        keyboard.press_and_release("volume down")   # simulate the unmute key press.

    #execute the appropiate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True

# Asysnchronus function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):

    funcs = []  # list to store asynchronous tasks.

    for command in commands:

        if command.startswith("open "):     # handle "open" commands.

            if "open it" in command:    #ignore "open it" commands.
                pass

            if "open file" == command:      #ignore "open file" commands.
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))     # schedule app opening
                funcs.append(fun)

        elif command.startswith("general "):    #placeholder for general commands.
            pass

        elif command.startswith("realtime "):    #placeholder for real-time commands.
            pass

        elif command.startswith("close "):    # handle "close" commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))   #schedule app closing.
            funcs.append(fun)

        elif command.startswith("play "):    # handle "play" commands.
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))   #schedule youtube playback.
            funcs.append(fun)

        elif command.startswith("content "):    #placeholder for general commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content "))   #schedule content creation.
            funcs.append(fun)

        elif command.startswith("google search "):    # handle google search commands..
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))   #schedule youtube playback.
            funcs.append(fun)

        elif command.startswith("youtube search "):    #handle youtube search commands.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))   #schedule youtube search.
            funcs.append(fun)

        elif command.startswith("system "):    #handle system command.
            fun = asyncio.to_thread(System, command.removeprefix("system "))   #schedule system command.
            funcs.append(fun)

        else:
            print(f"No Function found. For {command}")  #print an error for unrecognized commands

    results = await asyncio.gather(*funcs)  # execute all tasks concurrently.

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronus function to automate command executaion.
async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):  # translate and execute command.
        pass

    return True

if __name__ == "__main__":
    asyncio.run(Automation(["open facebook", "open instagram", "open telegram", "play ishq"]))