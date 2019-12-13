"""
    src.stream
    A PyGame surface object which can accept a cv2 image stream
"""

# Third party imports
from pygame import surface, surfarray
from numpy import rot90

class Stream:

    # Object constructor
    def __init__(self, size, display, position=(0,0)):
        # Store object parameters
        self.size = size
        self.display = display
        self.position = position

        # Create PyGame surface object
        self.surface = surface.Surface(self.size, 0, self.display)

    # Update the surface with a new image
    def update(self, imageData):
        # Image data from cv2 is stored in [h,w,(BGR)] format,
        #   to convert it to [w,h,(RGB)] we need to first rotate it
        #   and then reverse the order of the RGB values.
        surfarray.blit_array(self.surface, rot90(imageData)[:, :, ::-1])

    # Draw the image to the display
    def draw(self):
        self.display.blit(self.surface, self.position)
