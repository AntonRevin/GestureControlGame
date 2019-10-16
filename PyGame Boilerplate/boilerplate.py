"""
    Boilerplate for PyGame application
"""

# Third party imports
import pygame
import cv2

# Local imports
from src.colour import Colour
from src.stream import Stream

# Initialize the game engine
pygame.init()

# Define constants
SCREEN_SIZE = (1280, 720)
WINDOW_TITLE = "PyGame Boilerplate"
FRAME_RATE = 60
CLEAR_COLOUR = Colour.BLACK.value

# Define global variables
carryOn = True
clock = pygame.time.Clock()

# Open the game window
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

# Temporary OpenCV video capture to streamable object test
cam = cv2.VideoCapture(0)
ret_val, img = cam.read()
streamObject = Stream((img.shape[1],img.shape[0]), screen)

# Main program loop
while carryOn:
    
    # Main event loop
    for event in pygame.event.get():
        # User requested program shut-down
        if event.type == pygame.QUIT:
            carryOn = False 

    # Logic
        # Temporary streamable object test
        ret_val, img = cam.read()
        streamObject.update(img)

    # Clear screen
    screen.fill(CLEAR_COLOUR)

    # Draw sprites
    streamObject.draw()

    # Sync
    pygame.display.flip()

    # Wait for requested frame rate
    clock.tick(FRAME_RATE)

# Cleanup upon exit
pygame.quit()
