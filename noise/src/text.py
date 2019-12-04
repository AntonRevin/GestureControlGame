"""
    src.text
    Represents a text object
"""

class Text:

    # Object constructor
    def __init__(self, display, font, content, foreColour, position, antialias=True, backColour=None, center=False, shadow=False, shadowColour=[0,0,0], shadowOffset=5):
        # Set parameters
        self.display = display
        self.font = font
        self.content = content
        self.foreColour = foreColour
        self.position = position
        self.antialias = antialias
        self.backColour = backColour
        self.center = center
        self.shadow = shadow
        self.shadowColour = shadowColour
        self.shadowOffset = shadowOffset

        # Create text object
        self.update(self.content)

    # Draw the text to the display
    def draw(self):
        if self.shadow:
            self.display.blit(self.shadowSurface, self.shadowRect)
        self.display.blit(self.surface, self.rect)

    # Update the text
    def update(self, content):
        # Update variables
        self.content = content

        # Create text object
        self.surface = self.font.render(str(self.content), self.antialias, self.foreColour, self.backColour)
        self.rect = self.surface.get_rect()
        if self.center:
            self.rect.center = (self.position[0] // 1, self.position[1] // 1)
        else:
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]

        if self.shadow:
            self.shadowSurface = self.font.render(str(self.content), self.antialias, self.shadowColour, self.backColour)
            self.shadowRect = self.shadowSurface.get_rect()
            if self.center:
                self.shadowRect.center = (self.position[0] // 1, self.position[1] // 1 + self.shadowOffset)
            else:
                self.shadowRect.x = self.position[0]
                self.shadowRect.y = self.position[1] + self.shadowOffset