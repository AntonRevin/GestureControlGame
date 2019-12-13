# Third party imports
from os.path import join
from math import sin, pi
from random import random
import pygame
import numpy as np
import cv2
import time

# Local imports
from src.cameraHandler import CameraHandler
from src.stream import Stream
from src.colour import Colour
from src.text import Text

# Initialize the game engine
pygame.init()

# Define constants
SCREEN_SIZE = (1280, 720)
WINDOW_TITLE = "Calibration"
FRAME_RATE = 60
CLEAR_COLOUR = Colour.BLACK.value
CAPTURE_SIZE = (1280, 720)

# Define global variables
clock = pygame.time.Clock()
startCalibrate = False
calibrated = False
playGame = False
carryOn = True

# Create game window
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

# MV setup
cameraHandler = CameraHandler(CAPTURE_SIZE)
cameraHandler.startCameraStream()

# UI
font = pygame.font.Font('freesansbold.ttf', 32)
calibrateText = Text(screen, font, "[SPACE] to Calibrate Background", Colour.WHITE.value, (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2), center=True, shadow=True)
stream = Stream(CAPTURE_SIZE, screen)

# Main program loop
while carryOn:
    # Main event loop
    for event in pygame.event.get():
        # User requested program shut-down
        if event.type == pygame.QUIT:
            carryOn = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                carryOn = False
            if event.key == pygame.K_SPACE: # Calibrate
                startCalibrate = True
            if event.key == pygame.K_RETURN: # Start game 
                if calibrated:
                    playGame = True
    
    # Game logic
    if playGame and calibrated:
        pass
    else: # Calibration Logic
        if startCalibrate:
            screen.fill(CLEAR_COLOUR)
            calibrateText = Text(screen, font, "STARTING CALIBRATION", Colour.WHITE.value, (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2), center=True, shadow=True)
            calibrateText.draw()
            pygame.display.flip()
            time.sleep(2)
            screen.fill(CLEAR_COLOUR)
            calibrateText = Text(screen, font, "CALIBRATING...", Colour.WHITE.value, (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2), center=True, shadow=True)
            calibrateText.draw()
            pygame.display.flip()
            cameraHandler.calibrateBackground(60)
            startCalibrate = False
            calibrated = True
            calibrateText = Text(screen, font, "[SPACE] to Recalibrate Background - or [ENTER] to Accept", Colour.WHITE.value, (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2), center=True, shadow=True)

    # Collect new frame
    cameraHandler.fetchFrame()

    # Clear screen
    screen.fill(CLEAR_COLOUR)

    # Game drawing
    if playGame and calibrated:
        pass
    else:
        # Update stream object
        stream.update(cameraHandler.frame)
        stream.draw()
        calibrateText.draw()

    # Sync
    pygame.display.flip()

    # Wait for requested frame rate
    clock.tick(FRAME_RATE)

# Cleanup
pygame.quit()

