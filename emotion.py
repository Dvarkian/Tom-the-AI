
from cv2 import * # importing OpenCV library
from deepface import DeepFace
import random
from ioUtils import getSyns
import time
from settings import settings
import time

cam_port = 0 # If you have multiple camera connected with current device, assign a value in cam_port variable according to that
cam = VideoCapture(cam_port) # initialize the camera

#print(cam)

last = ""
flip = ""

threshold = 98
# 81 too low



def retort(message): # Output a message to the frontend.

    with open("intermediaryBackToFront.txt", "a", encoding="utf-8") as intermediary: 
        intermediary.write("\n[EMOTION] " + message) # Append message to the intermediary file.


def output(emotion):
    
    if "away" in emotion:
        text = random.choice([random.choice(["leaving", "departing", "going"])])
        time.sleep(10)
    else:
        #text = random.choice(getSyns([emotion]))
        text = emotion.replace("fear", "afraid")
        text = text.replace("surprise", "surprised")
    
    text = "Emotion: I am " + text + "."

    if "neutral" in text:
        return
    else:
        retort(text)
        time.sleep(8)
        #print(text)


retort("Loaded")

while True:

    if not settings("cam") or "off" in settings("cam") or not settings("windowOpen"):
        time.sleep(3)
        continue
    
    # reading the input using the camera
    result, image = cam.read()
    #print(image)
    
    if result:

        try:
            
            result = DeepFace.analyze(image, actions=['emotion'])
            emotion = result['dominant_emotion']

            if "y" in emotion:
                thresh = threshold - (100 - threshold)
            else:
                thresh = threshold
                
            if emotion != last and (result['emotion'][emotion] > thresh or last == "away" and result['emotion'][emotion] > threshold / 2):
                last = emotion
                #print(emotion, result['emotion'][emotion])
                output(emotion)
                continue

        except ValueError:
            emotion = "away"

            if emotion != last:
                last = emotion
                output(emotion)
            
    # If captured image is corrupted, moving to else part
    else:
        print(result)
        time.sleep(2)
        #break



