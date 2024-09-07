import arcade
from arcade import Sprite

from resource import Resource


class Explosion(Sprite):
    def __init__(self, center_x, center_y):
        super().__init__(
            texture=Resource.explo1_textures[0], center_x=center_x, center_y=center_y
        )
        self.textures = Resource.explo1_textures
        self.cur_texture_index = 0
        self.cur_texture = self.textures[self.cur_texture_index]
        self.time = 0
        arcade.play_sound(Resource.explode_sound)

    def update(self):
        self.time += 1
        if self.time % 3 == 0:
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.textures):
                self.remove_from_sprite_lists()
            else:
                self.cur_texture = self.textures[self.cur_texture_index]
                self.set_texture(self.cur_texture_index)
        super().update()
