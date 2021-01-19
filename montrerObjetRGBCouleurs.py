# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 09:36:00 2019

@author: Dr. Mocanu
"""

import sys
reload(sys)
import time
sys.setdefaultencoding("utf-8")
sys.path.insert(0, './.naoweb')
from libnao import *
set_monitoring(True)
init('localhost')

# Imports pour calcul
import math
import almath

# Imports pour requêtes au serveur
import requests
import json

# Imports NAOqi
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

import random
import sqlite3
import numpy as np
import Image


Projet = None


class ProjetModule(ALModule):
    """ Module du projet NAO

    """
    def __init__(self, name):
        ALModule.__init__(self, name)

        self.tts = ALProxy("ALTextToSpeech")
        camera = ALProxy("ALVideoDevice")
         
        handle = camera.subscribeCamera("ProjetModule", 0, 0, 11, 5)
        rand = random.randint(0,8)
        couleurs = initialiserCouleurs(rand)
        col = couleurs[3]
        
        dire("montre moi un objet %s et appui sur la tête" % (col))
        while not appui_tete():
            continue
        img = camera.getImageRemote(handle)
        camera.unsubscribe(handle)
        
        imageWidth = img[0]
        imageHeight = img[1]
        array = img[6]
        im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
        pixels = np.array(im)

        count = verifierCouleur(pixels, couleurs)
           
        if count > 450:
           dire("bravo")
        else:
           dire("non, ce n'est pas %s" % (col))
   
def initialiserCouleurs(num):
    if num == 0:
        colors = [0, 1, 2, "rouge"]
    elif num == 1:
        colors = [1, 0, 2, "vert"]
    elif num == 2:
        colors = [2, 1, 0, "bleu"]
    elif num == 3:
        colors = [0, 1, 2, "jaune"]
    elif num == 4:
        colors = [0, 2, 1, "rose"]
    elif num == 5:
        colors = [2, 1, 0, "cyan"]
    elif num == 6:
        colors = [0, 1, 2, "orange"]
    elif num == 7:
        colors = [0, 1, 2, "noir"]
    elif num == 8:
        colors = [0, 1, 2, "gris"]
        
    return colors
    

    
def verifierCouleur(pixels, colors):
    count = 0
    primaryColor = colors[0]
    secondaryColor1 = colors[1]
    secondaryColor2 = colors[2]     
    col = colors[3]

    if col == "rouge" or col == "vert" or col == "bleu":
        for py in range(20, 100):
            for px in range(20,140):
                if pixels[py][px][primaryColor] >= 170 and pixels[py][px][secondaryColor1] <= 80 and pixels[py][px][secondaryColor2] <= 80:
                    count = count + 1  
    elif col == "jaune":
        for py in range(20, 100):
            for px in range(20,140):
                if pixels[py][px][primaryColor] >= 180  and pixels[py][px][secondaryColor2] <= 120:
                    if (pixels[py][px][primaryColor] - 35) <= pixels[py][px][secondaryColor1] <= (pixels[py][px][primaryColor] + 35):
                        count = count + 1 
    elif col == "rose" or col == "cyan":
        for py in range(20, 100):
            for px in range(20,140):
                if pixels[py][px][primaryColor] >= 180 and pixels[py][px][secondaryColor1] >= 140 and pixels[py][px][secondaryColor2] <= 120:
                    if pixels[py][px][secondaryColor1] <= pixels[py][px][primaryColor]:
                        count = count + 1 
    elif col == "orange":
         for py in range(20, 100):
            for px in range(20,140):
                if pixels[py][px][primaryColor] >= 170 and 110 <= pixels[py][px][secondaryColor1] <= 215 and pixels[py][px][secondaryColor2] <= 60:
                    if pixels[py][px][secondaryColor1] <= pixels[py][px][primaryColor] - 40:
                        count = count + 1
    elif col == "noir":
         for py in range(20, 100):
            for px in range(20,140):
                if pixels[py][px][primaryColor] <= 50 and pixels[py][px][secondaryColor1] <= 50 and pixels[py][px][secondaryColor2] <= 50:
                        count = count + 1
    elif col == "gris": 
         for py in range(20, 100):
            for px in range(20,140):
                if 96 <= pixels[py][px][primaryColor] <= 170:
                    if (pixels[py][px][primaryColor] - 20) <= pixels[py][px][secondaryColor1] <= (pixels[py][px][primaryColor] + 20):
                        if (pixels[py][px][primaryColor] - 20) <= pixels[py][px][secondaryColor2] <= (pixels[py][px][primaryColor] + 20):
                            count = count + 1
                    
    return count

    
    
def main():
    """ Main entry point

    """
    print "Hello la monde"
    myBroker = ALBroker("myBroker",
                        "0.0.0.0",   # listen to anyone
                        0,           # find a free port and use it
                        nao_ip,         # parent broker IP
                        PORT)       # parent broker port

    global Projet
    Projet = ProjetModule("Projet")
    
    myBroker.shutdown()
    sys.exit(0)




if __name__ == "__main__":
    main()

