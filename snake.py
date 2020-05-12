from rwcommon import *

class Snake:
    game = None
    PositionHistory = []
    Acceleration = Vector2D(1, 0)
    Length = 1
    TotalSpeed = 1

    def __init__(self, game, Position, Length=1):
        self.game = game
        self.PositionHistory.append(Position)
        self.Length = Length
        if self.Length > 1:
            for i in range(1, self.Length):
                self.PositionHistory.append(Position-Vector2D(i, 0))

    def Tick(self, dt):
        w, h = getScreenSize()
        self.PositionHistory.insert(0,self.PositionHistory[0])
        self.PositionHistory[0] = self.PositionHistory[0] + (self.Acceleration * Vector2D(2 , 1) * self.TotalSpeed)
        if self.PositionHistory[0].x > w:
            self.PositionHistory[0].x -= w
        elif self.PositionHistory[0].x < 0:
            self.PositionHistory[0].x += w
        
        if self.PositionHistory[0].y > h:
            self.PositionHistory[0].y -= h
        elif self.PositionHistory[0].y < 0:
            self.PositionHistory[0].y += h

        while len(self.PositionHistory) > self.Length:
            del self.PositionHistory[-1]

    def Render(self, dt):
        for Position in self.PositionHistory:
            self.game.SetPixel(Position, 'O')
        pass

class Food:
    game = None
    Position = Vector2D()
    Value = 1
    def __init__(self, game):
        self.game = game
    def Render(self, dt):
        self.game.SetPixel(self.Position, 'x')


class WellcomeState(StateMachine.State):
    def OnStateRender(self, dt):
        w, h = getScreenSize()
        self.game.DrawText(w/2-3, h/2, "Snake")
        self.game.DrawText(w/2-13, h-4, "Press SPACEBAR to Start")
        pass

class WaitingState(StateMachine.State):
    def OnStateRender(self, dt):
        self.game.snake.Render(dt)

    def OnStateTick(self, dt):
        pass

class PlayingState(StateMachine.State):

    def OnStateEntered(self):
        self.game.RespawnFood()

    def OnStateRender(self, dt):
        self.game.snake.Render(dt)

    def OnStateTick(self, dt):
        self.game.snake.Tick(dt)
        if self.game.food != None:
            for pos in self.game.snake.PositionHistory:
                if pos == self.game.food.Position:
                    self.game.snake.Length += 1
                    self.game.RespawnFood()
                    break

class SnakeGame(Game):
    snake = None
    food = None
    gameState = StateMachine()

    def __init__(self):
        super().__init__()
        w, h = getScreenSize()
        self.snake = Snake(self, Vector2D(w/2, h/2),3)
        self.gameState.GoToState(PlayingState(self))
    
    def Tick(self, deltaTime):
        self.gameState.Tick(deltaTime)

    def Render(self, deltaTime):
        self.gameState.Render(deltaTime)
        if self.food != None:
            self.food.Render(deltaTime)

    def onKeyPressed(self, key):
        if key.name == 'w' and self.snake.Acceleration.y == 0:
            self.snake.Acceleration = Vector2D(0, -1)
        elif key.name == 's' and self.snake.Acceleration.y == 0:
            self.snake.Acceleration = Vector2D(0, 1)
        elif key.name == 'a' and self.snake.Acceleration.x == 0:
            self.snake.Acceleration = Vector2D(-1, 0)
        elif key.name == 'd' and self.snake.Acceleration.x == 0:
            self.snake.Acceleration = Vector2D(1, 0)

    def RespawnFood(self):
        self.food = Food(self)
        self.food.Position = getRandomPoint()

SnakeGame().Run()