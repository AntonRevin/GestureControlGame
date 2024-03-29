"""
    src.entity
    Wrapper for the PyGame Sprite object
"""

# Third party imports
from pygame import sprite, image

class Entity(sprite.Sprite):

    # Object constructor
    def __init__(self, imageFileName, posX=0, posY=0):
        # Call the parent constructor
        super().__init__()

        # Load image
        self.image = image.load(imageFileName).convert_alpha()

        # Create rect
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
    