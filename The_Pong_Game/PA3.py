"""
Created by Zeynep ÖZDEMİR, ÖZGE MERCANOĞLU SİNCAN
"""
# https://github.com/sefasarac
from graphics import *
import random
import math

# Do not change these following 4 variables
margin = 10  # height of the paddle from the ground
moveIncrement = 15  # paddle movement
ballRadius = 15
BOUNCE_WAIT = 1200

BALL_COUNT = 1 # If we change this, the number of ball changes!

class Timer:
    def __init__(self):
        self.value = 0


class Paddle:

    def __init__(self, color, width, height, coordx, win):
        self.color = color
        self.width = width
        self.height = height
        self.x = coordx
        self.shape = Rectangle(Point(self.x - int(self.width / 2), win.getHeight() - margin - self.height),
                               Point(self.x + int(self.width / 2), win.getHeight() - margin))
        self.shape.setFill(self.color)
        self.window = win
        self.shape.draw(self.window)

    def move_left(self):   # move paddle to the left by the amount of global variable moveIncrement
        # TODO: control that it does not exceed the window
        if(self.x - int(self.width/2) < 0):
            return
        self.x -= moveIncrement
        self.shape.move(-moveIncrement, 0)

    def move_right(self):  # move paddle to the right by the amount of global variable moveIncrement
        # TODO: control that it does not exceed the window
        if(self.x+int(self.width/2) > 300):
            return
        self.x += moveIncrement
        self.shape.move(moveIncrement, 0)


# TODO
# class Bubbles:
    # Define it by yourself to implement bubbles in the assignment
class Bubble:
    def __init__(self, coordx, coordy, color, radius, win):
        self.shape = Circle(Point(coordx, coordy), radius)
        self.x = coordx
        self.y = coordy
        self.color = color
        self.radius = radius
        self.window = win
        self.shape.setFill(self.color)
        self.shape.draw(self.window)

    def deleteBubble(self):
        self.shape.undraw()


class Ball:

    def __init__(self, coordx, coordy, color, radius, x_direction, speed, win):
        self.shape = Circle(Point(coordx, coordy), radius)
        self.x = coordx
        self.y = coordy
        self.xMovement = 0  # Current x movement
        self.yMovement = 0  # Current y movement
        self.color = color
        self.window = win
        self.shape.setFill(self.color)
        self.shape.draw(self.window)
        self.radius = radius
        self.timer = 0
        # Initial x direction. This variable will be 0 or 1. 1:right 0:left
        self.x_direction = x_direction
        self.speed = speed

    def is_moving(self):
        if(self.yMovement == 0 and self.xMovement == 0):
            return False
        return True

    def bounce(self, gameTimer, minX, maxX, maxY):
        # Calculating x-axis ball movement and bouncing
        # minX: min x coord. of paddle
        # maxX: max x coord. of paddle
        # maxY: max y coord. at which the ball can be move. If it goes further, it falls to the ground.

        global BOUNCE_WAIT
        gameOver = False

        if gameTimer >= self.timer + BOUNCE_WAIT:
            self.timer = gameTimer

            if (self.x <= 15):
                self.xMovement = 1

            elif (self.x >= 285):
                self.xMovement = -1

            if (self.y <= 15):
                self.yMovement = +1
            if(self.y >= maxY-margin and minX < self.x < maxX):
                self.yMovement = -1
            elif(self.y >= 585):
                gameOver = True
            if self.xMovement == 1:
                self.x += self.speed
            elif self.xMovement == -1:
                self.x -= self.speed
            if self.yMovement == -1:
                self.y -= self.speed
            elif self.yMovement == 1:
                self.y += self.speed
            self.shape.move(self.xMovement * self.speed,
                            self.yMovement * self.speed)

            return gameOver

    def carpisma(self, bubbleList):
        for bubble in bubbleList:
            uzaklik = math.sqrt((bubble.x-self.x)**2 + (bubble.y-self.y)**2)
            if(uzaklik <= 45):
                bubble.deleteBubble()
                bubbleList.remove(bubble)
            if(len(bubbleList) == 0):
                return True


def main():
    win = GraphWin("19290322 Pong Game", 300, 600)  # Replace your student id
    lives = 2
    win.setBackground("Black")
    myPaddle = Paddle("White", 100, 15, 150, win)

    ColorsList = ["Cyan", "Red", "Green", "Yellow"]
    BallList = list()
    for i in range(BALL_COUNT):
        rand_speed = random.randint(5, 20)  # random speed for ball
        # Note that the speed of the balls may vary depending on the hardware. If it is too fast or too slow, you can change the speed range for yourself while testing.
        # However, if you change these range, do not forget to reset these values to the initial limits before sending us.

        # This variable will be 0 or 1 randomly.
        rand_direction = random.randint(0, 1)
        ball = Ball(myPaddle.x - int(myPaddle.width/2) + i*30, win.getHeight() - margin -
                    myPaddle.height - ballRadius, ColorsList[i % 4], ballRadius, rand_direction, rand_speed, win)
        BallList.append(ball)

    # TODO:
    # You must add all necessary codes for the game to run.
    BaloonList = list()
    BaloonColors = ["Purple", "Yellow", "Green"]
    ColorCounter = 0
    BaloonRadius = 30
    xBubble, yBubble = 30, 30
    for i in range(1, 16):
        baloon = Bubble(xBubble, yBubble,
                        BaloonColors[ColorCounter], BaloonRadius, win)

        BaloonList.append(baloon)
        xBubble += BaloonRadius*2
        if(i % 5 == 0):
            yBubble += 60
            xBubble = 30
            ColorCounter += 1
            if(ColorCounter > 2):
                ColorCounter -= 1

    livesCounter = Text(
        Point(win.getWidth() - int(win.getWidth() / 5), 250), f'Lives -- {lives}')
    livesCounter.setTextColor("Cyan")
    livesCounter.setSize(15)
    livesCounter.draw(win)
    gameTimer = Timer()

    gameOver = False
    kazandi_mi = False
    while lives > 0:
        while not gameOver:
            if(kazandi_mi == True):
                break
            keyPress = win.checkKey()
            if keyPress == 'a':
                myPaddle.move_left()

            if keyPress == 'd':
                myPaddle.move_right()

            if keyPress == 'l':  # balls will move faster
                for item in BallList:
                    item.speed += 1

            # Balls will move slower. Note that in our case min speed is 2.
            if keyPress == 'k':
                for item in BallList:
                    if item.speed > 2:
                        item.speed -= 1

            if keyPress == 's':  # Initial movement of balls
                for item in BallList:
                    if(not item.is_moving()):
                        if item.x_direction == 1:   # it means ball moves to right in x direction
                            item.xMovement = 1
                        else:                   # it means ball moves to left in x direction
                            item.xMovement = -1
                        item.yMovement = -1  # at initial ball moves up in y direction

            gameTimer.value += 1
            for item in BallList:
                gameOver = item.bounce(gameTimer.value, (myPaddle.x-int(myPaddle.width/2)),
                                       (myPaddle.x+int(myPaddle.width/2)), win.getHeight() - margin - myPaddle.height)
                kazandi_mi = item.carpisma(BaloonList)
                if(kazandi_mi == True):
                    break
                if gameOver == True:
                    lives -= 1
                    break
        if(lives == 0 or kazandi_mi == True):
            break
        if(gameOver == True):
            # ekrandaki her objeyi silme
            for baloon in BaloonList:
                baloon.deleteBubble()
            BaloonList.clear()
            myPaddle.shape.undraw()
            for ball in BallList:
                ball.shape.undraw()
            BallList.clear()
            livesCounter.setText(f'Lives -- {lives}')
            # ekrandaki her objeyi geri oluşturma
            # paddle
            myPaddle = Paddle("White", 100, 15, 150, win)
            # toplar
            BallList = list()
            for i in range(BALL_COUNT):
                rand_speed = random.randint(5, 20)
                rand_direction = random.randint(0, 1)
                ball = Ball(myPaddle.x - int(myPaddle.width/2) + i*30, win.getHeight() - margin -
                            myPaddle.height - ballRadius, ColorsList[i % 4], ballRadius, rand_direction, rand_speed, win)
                BallList.append(ball)
            # balonlar
            ColorCounter = 0
            BaloonRadius = 30
            xBubble, yBubble = 30, 30
            for i in range(1, 16):
                baloon = Bubble(xBubble, yBubble,
                                BaloonColors[ColorCounter], BaloonRadius, win)

                BaloonList.append(baloon)
                xBubble += BaloonRadius*2
                if(i % 5 == 0):
                    yBubble += 60
                    xBubble = 30
                    ColorCounter += 1
                    if(ColorCounter > 2):
                        ColorCounter -= 1
            gameOver = False
    for baloon in BaloonList:
        baloon.deleteBubble()
    BaloonList.clear()
    myPaddle.shape.undraw()
    for ball in BallList:
        ball.shape.undraw()
    BallList.clear()
    livesCounter.setText(f'Lives -- {lives}')
    textGameOver = Text(Point(win.getWidth()/2, 300), "GAME OVER")
    textGameOver.setTextColor("Red")
    textGameOver.setSize(25)
    textGameOver.draw(win)
    textKazandi_mi = Text(Point(win.getWidth()/2, 350), "YOU LOST")
    if kazandi_mi == True:
        textKazandi_mi.setText("YOU WIN")
    textKazandi_mi.setTextColor("Red")
    textKazandi_mi.setSize(25)
    textKazandi_mi.draw(win)
    textPressKey = Text(Point(win.getWidth()/2, 400), "Press Any Key to Quit")
    textPressKey.setTextColor("Red")
    textPressKey.setSize(20)
    textPressKey.draw(win)
    win.getKey()

main()
# https://github.com/sefasarac