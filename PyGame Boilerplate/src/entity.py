"""
    src.entity
    Wrapper for the PyGame Sprite object
"""

# Third party imports
import pygame

#
class Entity(pygame.sprite.Sprite):

    # Object constructor
    def __init__(self, imageFileName, posX=0, posY=0):
        # Call the parent constructor
        super.__init__()

        # Load image
        self.image = pygame.image.load(imageFileName).convert_alpha()

        # Create rect
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
    