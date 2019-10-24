"""
    src.ball
"""

# Third party imports
from pygame import sprite, image, event, USEREVENT
from math import sin, pi

class Ball(sprite.Sprite):
    
    # Object constructor
    def __init__(self, imageFileName, player1, player2, posX=0, posY=0, direction=(0,0), speed=1, leftZone=10, rightZone=790):
        # Call the parent constructor
        super().__init__()

        # Load image
        self.image = image.load(imageFileName).convert_alpha()

        # Create rect
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.posX = posX
        self.posY = posY

        # Specific variables
        self.player1 = player1
        self.player2 = player2
        self.direction = direction
        self.speed = speed
        self.leftZone = leftZone
        self.rightZone = rightZone - self.rect.w

    def update(self):
        # Update ball position
        self.posX += self.direction[0] * self.speed
        self.posY += self.direction[1] * self.speed
        self.rect.x = round(self.posX)
        self.rect.y = round(self.posY)

        # Check for collision with players
        if self.rect.x < 400:
            playerX = self.player1.rect.x + 32
            playerY = self.player1.rect.y
            #playerW = self.player1.rect.w
            playerH = self.player1.rect.h

            if self.posX - playerX <= 0 and self.rect.y >= playerY - 32 - 16 and self.rect.y + 32 <= playerY + playerH + 32:
                bounceAngle = ((playerY + (playerH/2) - self.posY - (self.rect.h/2))/64)*(pi/2)*-1
                self.direction = (-1*self.direction[0], sin(bounceAngle))
                self.posX = playerX
        else:
            playerX = self.player2.rect.x - 32
            playerY = self.player2.rect.y
            #playerW = self.player2.rect.w
            playerH = self.player2.rect.h
            
            if self.posX - playerX >= 0 and self.rect.y >= playerY - 32 - 16 and self.rect.y + 32 <= playerY + playerH + 32:
                bounceAngle = ((playerY + (playerH/2) - self.posY - (self.rect.h/2))/64)*(pi/2)*-1
                self.direction = (-1*self.direction[0], sin(bounceAngle))
                self.posX = playerX
        
        # Check for "goals"
        if self.rect.x < self.leftZone:
            event.post(event.Event(USEREVENT, id="p1Lose"))
        elif self.rect.x > self.rightZone:
            event.post(event.Event(USEREVENT, id="p2Lose"))
        
        # Bounce on edges of play area
        if self.posY <= 1:
            self.posY = 1
            self.direction = (self.direction[0], -1*self.direction[1])
        elif self.posY >= 600 - self.rect.h - 1:
            self.posY = 600 - self.rect.h - 1
            self.direction = (self.direction[0], -1*self.direction[1])
