"""
    Pong
"""

# Third party imports
import pygame
from os.path import join
from math import sin, pi
from random import random
import numpy as np
import cv2

# Local imports
from src.colour import Colour
from src.entity import Entity
from src.ai import AI
from src.ball import Ball
from src.player import Player
from src.text import Text

# Initialize the game engine
pygame.init()

# Define constants
SCREEN_SIZE = (800, 600)
WINDOW_TITLE = "Pong Game"
FRAME_RATE = 60
CLEAR_COLOUR = Colour.BLACK.value
CAPTURE_SIZE = (640, 320)

# Define global variables
carryOn = True
clock = pygame.time.Clock()

# Open the game window
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

# Create game entities
background = Entity(join('media', 'fancy-court.png'))
enemy = AI(join('media', 'fancy-paddle-grey.png'), followSpeed=4, posX=758, posY=236)
player = Player(join('media', 'fancy-paddle-green.png'), posX=10, posY=236)
ball = Ball(join('media', 'fancy-ball.png'), player, enemy, direction=(1,0), speed=6, leftZone=16, rightZone=800-16)
enemy.target = ball
drawGroup = pygame.sprite.Group()
drawGroup.add(background)
drawGroup.add(enemy)
drawGroup.add(player)
drawGroup.add(ball)

# Game setup
ballStartPosition = (SCREEN_SIZE[0]/2 - ball.rect.w/2, SCREEN_SIZE[1]/2 - ball.rect.h/2)
paddleStartPosition = 236
ball.rect.x = ballStartPosition[0]
ball.rect.y = ballStartPosition[1]
scorePlayer1 = 0
scorePlayer2 = 0

# TEMP CV
lowerBound=np.array([24*(179/359),82*(255/100),31*(255/100)])
upperBound=np.array([52*(179/359),100*(255/100),71*(255/100)])
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_SIZE[0])
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_SIZE[1])
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

# UI
font = pygame.font.Font('freesansbold.ttf', 32)
scoreText = Text(screen, font, str(scorePlayer1) + "-" + str(scorePlayer2), Colour.WHITE.value, (400, 48), center=True)

# Main program loop
while carryOn:
    # Main event loop
    for event in pygame.event.get():
        # User requested program shut-down
        if event.type == pygame.QUIT:
            carryOn = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                carryOn = False
        if event.type == pygame.USEREVENT:
            if "Lose" in event.id:
                ball.posX = ballStartPosition[0]
                ball.posY = ballStartPosition[1]
                rnd = sin(random()*(pi/3) - (pi/6))
                ball.direction = (ball.direction[0], rnd)
                player.rect.y = paddleStartPosition
                enemy.rect.y = paddleStartPosition
                if event.id == "p1Lose":
                    scorePlayer2 += 1
                else:
                    scorePlayer1 += 1
                scoreText.update(str(scorePlayer1) + "-" + str(scorePlayer2))

    # Input control player (TEMP) TODO: Make "opencv smart"
    ret, img = cam.read()
    #img = img[:,range(320-40,320+40),:] # 320x320
    img=cv2.resize(img,(240,120))
    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    maskFinal=maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    tempY = 0
    tempH = 0
    for i in range(len(conts)):
        x,tempY,w,tempH=cv2.boundingRect(conts[i])
    player.rect.y = (tempY + (tempH/2)) * (600/120) - 64
    cv2.imshow("img", img)
    """keystate = pygame.key.get_pressed()
    if keystate[pygame.K_w] or keystate[pygame.K_UP]:
        player.rect.y -= 3
    if keystate[pygame.K_s] or keystate[pygame.K_DOWN]:
        player.rect.y += 3"""

    # Logic
    drawGroup.update()

    # Clear screen
    screen.fill(CLEAR_COLOUR)

    # Draw sprites
    drawGroup.draw(screen)

    # Draw UI
    scoreText.draw()

    # Sync
    pygame.display.flip()

    # Wait for requested frame rate
    clock.tick(FRAME_RATE)
    cv2.waitKey(1)

# Cleanup upon exit
pygame.quit()