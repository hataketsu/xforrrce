import random

from arcade import Sprite

from resource import Resource

CLOUD_SPEED = 0.1


class Cloud(Sprite):
    def __init__(self, window, center_x, center_y):
        super().__init__(texture=Resource.cloud_texture)
        self.window = window
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = 0
        self.change_y = 0
        self.time = 60 * 4

    def update(self):
        if self.time > 60 * 4:
            self.change_x = (random.random() * 2 - 1) * CLOUD_SPEED
            self.change_y = (random.random() * 2 - 1) * CLOUD_SPEED
            self.time = 0
        self.time += 1
        super().update()
