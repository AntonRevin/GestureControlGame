"""
    Boilerplate for PyGame application
"""

# Third party imports
import pygame

# Local imports
from src.colour import Colour

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

# Main program loop
while carryOn:
    
    # Main event loop
    for event in pygame.event.get():
        # User requested program shut-down
        if event.type == pygame.QUIT:
            carryOn = False 

    # Logic

    # Clear screen
    screen.fill(CLEAR_COLOUR)

    # Draw sprites

    # Sync
    pygame.display.flip()

    # Wait for requested frame rate
    clock.tick(FRAME_RATE)

# Cleanup upon exit
pygame.quit()
