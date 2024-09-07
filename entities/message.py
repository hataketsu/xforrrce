from arcade import Sprite

from font import FSSS_FONT
from resource import Resource


class Message:
    def __init__(self, center_x, center_y, text):
        self.center_x = center_x
        self.center_y = center_y
        self.text = text
        self.time_to_live = 60

    def draw(self):
        self.time_to_live -= 1
        self.center_x += 1/2
        self.center_y += 1/2
        FSSS_FONT.draw(
            self.text,
            self.center_x,
            self.center_y,
            scale=1,
        )