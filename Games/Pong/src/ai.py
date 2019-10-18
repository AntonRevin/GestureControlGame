"""
    src.ai
    AI paddle
"""

# Third party imports
from pygame import sprite, image
from math import copysign

class AI(sprite.Sprite):

    # Object constructor
    def __init__(self, imageFileName, followSpeed=1, deadZone=8, posX=0, posY=0):
        # Call the parent constructor
        super().__init__()

        # Load image
        self.image = image.load(imageFileName).convert_alpha()

        # Create rect
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY

        # Specific variables
        self.target = None
        self.followSpeed = followSpeed
        self.deadZone = deadZone

    def update(self):
        # TODO: make the AI more aggressive by targeting the edge of the bat.
        delta = self.target.rect.y - self.rect.y - 64
        if abs(delta) >= self.deadZone:
            self.rect.y += copysign(self.followSpeed, delta) 
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= 600 - 128:
            self.rect.y = 600 - 128

