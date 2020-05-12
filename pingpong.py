# Korovin Bogdan (ROYALWING) (c) 2020
# royalwing911@gmail.com

import rwcommon
import random

class Ball:

    x = 0
    y = 0

    accelx = 0
    accely = 0

    def __init__(self):
        self.reset()

    def reset(self):
        self.x, self.y = rwcommon.getScreenSize()
        self.x /= 2
        self.y /= 2
        self.accelx = 0
        self.accely = 0

    def launch(self):
        self.accelx = random.randint(0, 1)
        if self.accelx == 0:
            self.accelx = -1
        self.accely = random.randint(0, 1)
        if self.accely == 0:
            self.accely = -1

        speed = random.randint(1, 2)
        self.accelx *= speed
        self.accely *= speed

    def Tick(self, deltaTime):
        self.x += self.accelx
        self.y += self.accely

class Player:
    
    position = 0
    score = 0
    side = 0 # 0 - left, 1 - right
    barwidth = 4
    accel = 0

    def __init__(self, side):
        self.side = side
        self.reset()

    def reset(self, resetScore=False):
        w, h = rwcommon.getScreenSize()
        self.accel = 0
        if resetScore:
            self.score = 0
        self.position = h/2

    def render(self, game):
        w, h = rwcommon.getScreenSize()
        x = 0
        if self.side == 1:
            x = w

        for y in range(int(self.position-self.barwidth/2), int(self.position+self.barwidth/2)):
            game.SetPixel(x, y, "#")

        game.DrawText(x, 0, str(self.score))
    
    def Tick(self, deltaTime):
        w, h = rwcommon.getScreenSize()
        self.position += int(self.accel*2)
        if self.position-(self.barwidth/2) < 0:
            self.position = self.barwidth/2
        if self.position+(self.barwidth/2) > h:
            self.position = h - (self.barwidth/2)
        pass
    

    def OnKeyPressed(self, key):
        if self.side == 0:
            if key.name == 'w':
                self.accel-=1
            elif key.name == 's':
                self.accel+=1
        elif self.side == 1:
            if key.name == 'up':
                self.accel-=1
            elif key.name == 'down':
                self.accel+=1

    def OnKeyReleased(self, key):
        if self.side == 0:
            if key.name == 'w':
                self.accel+=1
            elif key.name == 's':
                self.accel-=1
        elif self.side == 1:
            if key.name == 'up':
                self.accel+=1
            elif key.name == 'down':
                self.accel-=1

    def isHere(self, inx, iny):
        w, h = rwcommon.getScreenSize()
        x = 0
        if self.side == 1:
            x = w-1

        if x == inx and abs(iny - self.position) < self.barwidth:
            return True
        return False


STATE_WELLCOME = 0
STATE_WAITING = 1
STATE_PLAYING = 2 

class PingPongGame(rwcommon.Game):

    ball = None

    gameState = 0

    player1 = None
    player2 = None

    def __init__(self):
        super().__init__()
        self.ball = Ball()
        self.player1 = Player(0)
        self.player2 = Player(1)
        self.OnStateChanged(0, 0)
        pass

    def GoToState(self, state):
        prevState = self.gameState
        self.gameState = state
        self.OnStateChanged(prevState, state)

    def OnStateChanged(self, prev, next):
        if next == STATE_WAITING:
            self.ResetKeyPressed()
            self.player1.reset(prev==STATE_WELLCOME)
            self.player2.reset(prev==STATE_WELLCOME)
            self.ball.reset()
        elif next == STATE_PLAYING:
            self.ball.launch()
        pass

    def Tick(self, deltaTime):

        w, h = rwcommon.getScreenSize()

        if self.gameState == STATE_PLAYING:
            self.player1.Tick(deltaTime)
            self.player2.Tick(deltaTime)

            if self.ball.x == 0:
                if self.player1.isHere(self.ball.x, self.ball.y):
                    self.ball.accelx *= -1
                    self.ball.accely += self.player1.accel
                else:
                    self.player2.score+=1
                    if self.player2.score > 9:
                        self.GoToState(STATE_WELLCOME)
                        return
                    self.ball.reset()
                    self.GoToState(STATE_WAITING)
            if self.ball.x == w-1:
                if self.player2.isHere(self.ball.x, self.ball.y):
                    self.ball.accelx *= -1
                    self.ball.accely += self.player2.accel
                else:
                    self.player1.score+=1
                    if self.player1.score > 9:
                        self.GoToState(STATE_WELLCOME)
                        return
                    self.ball.reset()
                    self.GoToState(STATE_WAITING)
                    
            self.ball.Tick(deltaTime)


    def Render(self, deltaTime):
        w, h = rwcommon.getScreenSize()
        if self.gameState == STATE_WELLCOME:

            titley = int(h/2)-4
            titlex = int(w/2)-4
            self.DrawText(titlex, titley, "PING-PONG")
            presstexty = h - 4
            presstextx = int(w/2)-13
            self.DrawText(presstextx, presstexty, "Press SPACEBAR to continue")

            return



        if self.ball.x > w:
            self.ball.x = w-1
            self.ball.accelx *= -1
        if self.ball.y > h:
            self.ball.y = h-1
            self.ball.accely *= -1

        
        if self.ball.x < 0:
            self.ball.x = 1
            self.ball.accelx *= -1
        if self.ball.y < 0:
            self.ball.y = 1
            self.ball.accely *= -1


        self.SetPixel(self.ball.x, self.ball.y, 'O')

        self.player1.render(self)
        self.player2.render(self)

        if self.gameState == STATE_WAITING:
            presstexty = h / 2
            presstextx = int(w/2)-12
            self.DrawText(presstextx, presstexty, "Press SPACEBAR to start")

        pass

    def onKeyPressed(self, key):
        if key.name == 'space':
            if self.gameState == STATE_WELLCOME:
                self.GoToState(STATE_WAITING)
                return
            elif self.gameState == STATE_WAITING:
                self.GoToState(STATE_PLAYING)
                return

        self.player1.OnKeyPressed(key)
        self.player2.OnKeyPressed(key)

    def onKeyReleased(self, key):
        self.player1.OnKeyReleased(key)
        self.player2.OnKeyReleased(key)


Game = PingPongGame()
Game.Run()