"""
    Pong
"""

# Third party imports
import pygame
from os.path import join
from math import sin, pi
from random import random

# Local imports
from src.colour import Colour
from src.entity import Entity
from src.ai import AI
from src.ball import Ball
from src.player import Player

# Initialize the game engine
pygame.init()

# Define constants
SCREEN_SIZE = (800, 600)
WINDOW_TITLE = "Pong Game"
FRAME_RATE = 120
CLEAR_COLOUR = Colour.BLACK.value
CAPTURE_SIZE = (1280, 720)

# Define global variables
carryOn = True
clock = pygame.time.Clock()

# Open the game window
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

# Create game entities
background = Entity(join('media', 'fancy-court.png'))
enemy = AI(join('media', 'fancy-paddle-grey.png'), posX=758, posY=236)
player = Player(join('media', 'fancy-paddle-green.png'), posX=10, posY=236)
ball = Ball(join('media', 'fancy-ball.png'), player, enemy, direction=(1,0), speed=3, leftZone=32, rightZone=800-32)
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

    # Input control player (TEMP) TODO: Make "opencv smart"
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_w] or keystate[pygame.K_UP]:
        player.rect.y -= 3
    if keystate[pygame.K_s] or keystate[pygame.K_DOWN]:
        player.rect.y += 3

    # Logic
    drawGroup.update()

    # Clear screen
    screen.fill(CLEAR_COLOUR)

    # Draw sprites
    drawGroup.draw(screen)

    # Sync
    pygame.display.flip()

    # Wait for requested frame rate
    clock.tick(FRAME_RATE)

# Cleanup upon exit
pygame.quit()