"""
    src.player
"""

# Third party imports
from pygame import sprite, image

class Player(sprite.Sprite):

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

    # Update function
    def update(self):
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y >= 600 - 128:
            self.rect.y = 600 - 128
