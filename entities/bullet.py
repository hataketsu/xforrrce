from arcade import Sprite

from resource import Resource


class Bullet(Sprite):
    def __init__(self, center_x, center_y):
        super().__init__(texture=Resource.shot_textures[0], center_x=center_x, center_y=center_y)
        self.textures = Resource.shot_textures
        self.cur_texture_index = 0
        self.cur_texture = self.textures[self.cur_texture_index]
        self.time = 0

    def update(self):
        self.time += 1
        if self.time % 3 == 0:
            self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
            self.cur_texture = self.textures[self.cur_texture_index]
            self.set_texture(self.cur_texture_index)
        super().update()
