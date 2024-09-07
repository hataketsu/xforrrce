from arcade import Sprite, get_distance_between_sprites
from pyglet.media.codecs.ffmpeg_lib import swscale

from entities.bullet import Bullet
from entities.explosion import BigExplosion


class Ship(Sprite):
    def __init__(self, window, center_x, center_y):
        super().__init__(texture=window.map_textures[48])
        self.window = window
        self.scene = window.scene
        self.center_x = center_x
        self.center_y = center_y
        self.cooldown = 0
        self.hp = 40

    def update(self):
        if self.hp == -1:
            return

        self.fire()

        if self.hp <= 0:
            self.remove_from_sprite_lists()
            self.texture = self.window.map_textures[57]
            self.scene.add_sprite("barrier", self)
            self.window.add_message(
                self.window.tank.center_x, self.window.tank.center_y, "+10 EXP"
            )
            self.hp = -1
            self.scene.add_sprite(
                "explosions", BigExplosion(self.window, self.center_x, self.center_y)
            )

    def fire(self):
        distance_to_tank = get_distance_between_sprites(self, self.window.tank)
        if distance_to_tank < 160 and self.cooldown <= 0:
            bullet = Bullet(self.center_x, self.center_y, enemy=True)
            bullet_speed = 2
            bullet.change_x = (
                (self.window.tank.center_x - self.center_x)
                / distance_to_tank
                * bullet_speed
            )
            bullet.change_y = (
                (self.window.tank.center_y - self.center_y)
                / distance_to_tank
                * bullet_speed
            )
            self.scene.add_sprite("bullets", bullet)
            self.cooldown = 60
        else:
            self.cooldown -= 1

    def draw_custom(self):
        pass
