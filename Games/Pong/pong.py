"""
    Pong
"""

# Third party imports
from os.path import join
from math import sin, pi
from random import random
import pygame
import numpy as np

# Local imports
from src.colour import Colour
from src.entity import Entity
#from src.ai import AI
from src.ball import Ball
from src.player import Player
from src.text import Text
from src.camerahandler import CameraHandler

# Initialize the game engine
pygame.init()

# Define constants
SCREEN_SIZE = (800, 600)
WINDOW_TITLE = "Pong Game"
FRAME_RATE = 60
CLEAR_COLOUR = Colour.BLACK.value
CAPTURE_SIZE = (640, 320)
CV_LOWER_BOUNDARY = np.array([24*(179/359), 82*(255/100), 31*(255/100)])
CV_UPPER_BOUNDARY = np.array([52*(179/359), 100*(255/100), 71*(255/100)])
CV_OPEN_KERNEL = np.ones((5, 5))
CV_CLOSE_KERNEL = np.ones((20, 20))

# Define global variables
carryOn = True
clock = pygame.time.Clock()

# Open the game window
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

# Create game entities
background = Entity(join('media', 'fancy-court.png'))
#enemy = AI(join('media', 'fancy-paddle-grey.png'), followSpeed=4, posX=758, posY=236)
player1 = Player(join('media', 'fancy-paddle-green.png'), posX=10, posY=236)
player2 = Player(join('media', 'fancy-paddle-green.png'), posX=758, posY=236)
ball = Ball(join('media', 'fancy-ball.png'), player1, player2, direction=(1, 0), speed=6, leftZone=16, rightZone=800-16)
drawGroup = pygame.sprite.Group()
drawGroup.add(background)
drawGroup.add(player1)
drawGroup.add(player2)
drawGroup.add(ball)

# Game setup
ballStartPosition = (SCREEN_SIZE[0]/2 - ball.rect.w/2, SCREEN_SIZE[1]/2 - ball.rect.h/2)
paddleStartPosition = 236
ball.rect.x = ballStartPosition[0]
ball.rect.y = ballStartPosition[1]
scorePlayer1 = 0
scorePlayer2 = 0

# Machine vision setup
cameraHandler = CameraHandler(CAPTURE_SIZE, CV_LOWER_BOUNDARY, CV_UPPER_BOUNDARY, CV_OPEN_KERNEL, CV_CLOSE_KERNEL)
cameraHandler.startCameraStream()

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
                player1.rect.y = paddleStartPosition
                player2.rect.y = paddleStartPosition
                if event.id == "p1Lose":
                    scorePlayer2 += 1
                else:
                    scorePlayer1 += 1
                scoreText.update(str(scorePlayer1) + "-" + str(scorePlayer2))

    # OpenCV player control logic
    player1.rect.y, player2.rect.y = cameraHandler.findControlHeight(SCREEN_SIZE[1])

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

# Cleanup upon exit
pygame.quit()