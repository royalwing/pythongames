# Korovin Bogdan (ROYALWING) (c) 2020
# royalwing911@gmail.com

import os
import platform
import time
import keyboard

def cleanScreen():
    system_name = platform.system()
    if system_name == 'Linux':
        os.system("clr")
    elif system_name == 'Windows':
        os.system("cls")

def getScreenSize():
    return (48, 24)

def getCurrentMillis():
    return time.time()*1000

def pixelPosToID(x, y):
    w, h = getScreenSize()
    if x <= 0:
        x = 0
    elif x > w-1:
        x = w-1
    if y <= 0:
        y = 0
    elif y > h-1:
        y = h-1

    return int(x + w * y)

def pixelIDToPos(id):
    w, h = getScreenSize()
    return (id - (id%w), id%w)

class Game:

    lastUpdateTime = 0.0
    screenMem = []

    pressedKeys = []

    def __init__(self):
        self.lastUpdateTime = getCurrentMillis()
        x,y = getScreenSize()
        self.screenMem = [' ']*(x*y)
        keyboard.on_release(self._onKeyReleased, True)
        keyboard.on_press(self._onKeyPressed, True)
        pass

    def _onKeyPressed(self, key):
        try:
            self.pressedKeys.index(key.name)
        except:
            self.pressedKeys.append(key.name)
            self.onKeyPressed(key)

    def _onKeyReleased(self, key):
        try:
            if self.pressedKeys.index(key.name) > -1:
                self.pressedKeys.remove(key.name)
                self.onKeyReleased(key)
        except:
            pass
    
    def ResetKeyPressed(self):
        self.pressedKeys = []

    def onKeyPressed(self, key):
        pass

    def onKeyReleased(self, key):
        pass

    def Run(self):
        while(True):
            w, h = getScreenSize()
            self.screenMem = [' ']*(w*h)
            now = getCurrentMillis()
            deltaTime = now - self.lastUpdateTime
            self.lastUpdateTime = now
            self.Tick(deltaTime)
            self.Render(deltaTime)
            cleanScreen()
            scrmem = "".join(self.screenMem)
            finalStr = ""
            for y in range(0, h):
                id = pixelPosToID(0, y)
                finalStr += scrmem[id:id+w] + "\n"
            print(finalStr)
            time.sleep(0.016) #trying to reach 60fps
        pass

    def SetPixel(self, x, y, status):
        ID = pixelPosToID(x, y)
        self.screenMem[ID] = status
        pass

    def Tick(self, deltaTime):
        pass

    def Render(self, deltaTime):
        pass