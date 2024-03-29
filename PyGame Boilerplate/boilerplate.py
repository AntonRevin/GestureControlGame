"""
    Boilerplate for PyGame application
"""

# Third party imports
import pygame
import cv2

# Local imports
from src.colour import Colour
from src.stream import Stream
from src.text import Text

# Initialize the game engine
pygame.init()

# Define constants
SCREEN_SIZE = (1280, 720)
WINDOW_TITLE = "PyGame Boilerplate"
FRAME_RATE = 60
CLEAR_COLOUR = Colour.BLACK.value
CAPTURE_SIZE = (1280, 720)

# Define global variables
carryOn = True
clock = pygame.time.Clock()

# Open the game window
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

# Temporary OpenCV video capture to streamable object test
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_SIZE[0])
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_SIZE[1])
streamObject = Stream(CAPTURE_SIZE, screen)

# Create Text object
font = pygame.font.Font('freesansbold.ttf', 32)
txt = Text(screen, font, "Test", Colour.WHITE.value, (40,40))

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

    # Logic
    # Temporary streamable object test
    ret_val, img = cam.read()
    streamObject.update(img)

    # Clear screen
    screen.fill(CLEAR_COLOUR)

    # Draw sprites
    streamObject.draw()
    txt.draw()

    # Sync
    pygame.display.flip()

    # Wait for requested frame rate
    clock.tick(FRAME_RATE)

# Cleanup upon exit
pygame.quit()
