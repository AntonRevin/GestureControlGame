"""
    src.text
    Represents a text object
"""

class Text:

    # Object constructor
    def __init__(self, display, font, content, foreColour, position, antialias=True, backColour=None, center=False):
        # Set parameters
        self.display = display
        self.font = font
        self.content = content
        self.foreColour = foreColour
        self.position = position
        self.antialias = antialias
        self.backColour = backColour
        self.center = center

        # Create text object
        self.surface = self.font.render(str(self.content), self.antialias, self.foreColour, self.backColour)
        self.rect = self.surface.get_rect()
        if self.center:
            self.rect.center = (self.position[0] // 1, self.position[1] // 1)
        else:
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]

    # Draw the text to the display
    def draw(self):
        self.display.blit(self.surface, self.rect)