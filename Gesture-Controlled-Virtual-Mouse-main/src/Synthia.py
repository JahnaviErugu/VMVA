import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import wikipedia
import Gesture_Controller
import app
from threading import Thread
import subprocess


# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files =[]
path = ''
is_awake = True  #Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)

    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("I am Synthia, how may I help you?")

# Set Microphone parameters
with sr.Microphone() as source:
        r.energy_threshold = 500 
        r.dynamic_energy_threshold = False

# Audio to String
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry my Service is down. Plz check your Internet connection')
        except sr.UnknownValueError:
            print('cant recognize')
            pass
        return voice_data.lower()

def open_application(app_name):
    if app_name == "notepad":
        subprocess.Popen(["notepad.exe"])
    elif app_name == "calculator":
        subprocess.Popen(["calc.exe"])
    elif app_name == "chrome":
        subprocess.Popen(["C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"])
    elif app_name == "camera":
        subprocess.Popen(["camera.exe"])
    else:
        reply("Sorry, I don't know how to open that application.")

def control_presentation(voice_data):
    if 'next slide' in voice_data:
        # Code to navigate to the next slide
        pass
    elif 'previous slide' in voice_data:
        # Code to navigate to the previous slide
        pass
    elif 'go to slide' in voice_data:
        # Extract slide number from voice_data and navigate to that slide
        pass
    elif 'start presentation' in voice_data:
        # Code to start the presentation
        pass
    elif 'end presentation' in voice_data:
        # Code to end the presentation
        pass

def type_in_notepad(text):
    # Wait for Notepad to open
    time.sleep(1)
    
    # Simulate typing in Notepad
    pyautogui.typewrite(text)

def take_screenshot():
    # Timestamp for unique filenames
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Define the filename
    filename = f"screenshot_{timestamp}.png"
    # Take screenshot
    screenshot = pyautogui.screenshot()
    # Save screenshot
    screenshot.save(filename)
    # Return the filename for reference
    return filename

# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data.replace('synthia','')
    app.eel.addUserMsg(voice_data)

    if is_awake==False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    # STATIC CONTROLS
    elif 'hello' in voice_data:
        wish()

    elif 'take screenshot' in voice_data:
        reply("Taking screenshot...")
        filename = take_screenshot()
        reply(f"Screenshot taken and saved as {filename}")

    elif 'what is your name' in voice_data:
        reply('My name is Synthia!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found')
        except:
            reply('Please check your Internet')

    elif 'location' in voice_data:
        reply('Which place are you looking for ?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found')
        except:
            reply('Please check your Internet')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Good bye! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        #sys.exit() always raises SystemExit, Handle it in main loop
        sys.exit()

    #MOUSE CONTROLS
    elif 'move mouse up' in voice_data:
        y = pyautogui.position()[1] - 50
        pyautogui.moveTo(0, y)
        reply('Moved mouse up by 50 pixels')

    elif 'move mouse down' in voice_data:
        y = pyautogui.position()[1] + 50
        pyautogui.moveTo(0, y)
        reply('Moved mouse down by 50 pixels')

    elif 'move mouse left' in voice_data:
        x = pyautogui.position()[0] - 50
        pyautogui.moveTo(x, 0)
        reply('Moved mouse left by 50 pixels')

    elif 'move mouse right' in voice_data:
        x = pyautogui.position()[0] + 50
        pyautogui.moveTo(x, 0)
        reply('Moved mouse right by 50 pixels')
        
    elif 'click mouse' in voice_data:
        pyautogui.click()
        reply('Mouse clicked')

    elif 'double click mouse' in voice_data:
        pyautogui.doubleClick()
        reply('Mouse double clicked')

    elif 'right click mouse' in voice_data:
        pyautogui.rightClick()
        reply('Mouse right clicked')
        
    
    # DYNAMIC CONTROLS
    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target = gc.start)
            t.start()
            reply('Launched Successfully')

    elif ('stop gesture recognition' in voice_data) or ('top gesture recognition' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped')
        else:
            reply('Gesture recognition is already inactive')
        
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')
    
    elif 'open' in voice_data:
        app_name = voice_data.split('open')[-1].strip()
        open_application(app_name)

    elif 'presentation' in voice_data:
        control_presentation(voice_data)

    elif 'open notepad' in voice_data:
        open_application("notepad")
        reply("What would you like me to write in Notepad?")
    
    elif 'write' in voice_data and file_exp_status:
        # Extract the text to write
        text_to_write = voice_data.replace('write', '').strip()
        
        # Type the text in Notepad
        type_in_notepad(text_to_write)
        reply("Text written successfully in Notepad.")
        
    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully')
                    app.ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('You do not have permission to access this folder')
                                    
        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                app.ChatBot.addAppMsg(filestr)
                   
    else: 
        reply('I am not functioned to do this !')

# ------------------Driver Code--------------------

t1 = Thread(target = app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        #take input from GUI
        voice_data = app.ChatBot.popUserInput()
    else:
        #take input from Voice
        voice_data = record_audio()

    #process voice_data
    if 'synthia' in voice_data:
        try:
            #Handle sys.exit()
            respond(voice_data)
        except SystemExit:
            reply("Exit Successfull")
            break
        except:
            #some other exception got raised
            print("EXCEPTION raised while closing.") 
            break
        


