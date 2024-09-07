from math import radians, sin, cos

import arcade
from arcade import (
    Sprite,
    get_distance_between_sprites,
    check_for_collision,
    PointList,
    are_polygons_intersecting,
)

from entities.bullet import Bullet
from entities.explosion import BigExplosion


class Sentry(Sprite):
    def __init__(self, window, center_x, center_y):
        super().__init__(texture=window.map_textures[46])
        self.window = window
        self.scene = window.scene
        self.center_x = center_x
        self.center_y = center_y
        self.cooldown = 0
        self.hp = 100
        self.radar_angle = 0
        self.radar_hitbox = None

    def update(self):
        if self.hp == -1:
            return
        x1 = self.center_x + 160 * cos(radians(self.radar_angle))
        y1 = self.center_y + 160 * sin(radians(self.radar_angle))
        x2 = self.center_x + 160 * cos(radians(self.radar_angle + 20))
        y2 = self.center_y + 160 * sin(radians(self.radar_angle + 20))
        self.radar_hitbox = ((self.center_x, self.center_y), (x1, y1), (x2, y2))
        if are_polygons_intersecting(
            self.radar_hitbox, self.window.tank.get_adjusted_hit_box()
        ):
            self.fire()
        else:
            self.radar_angle = (self.radar_angle + 1) % 360

        if self.hp <= 0:
            self.remove_from_sprite_lists()
            self.texture = self.window.map_textures[56]
            self.scene.add_sprite("barrier", self)
            self.window.add_message(
                self.window.tank.center_x, self.window.tank.center_y, "+10 EXP"
            )
            self.hp = -1
            self.scene.add_sprite(
                "explosions", BigExplosion(self.window, self.center_x, self.center_y)
            )

    def fire(self):
        if self.cooldown <= 0:
            distance_to_tank = get_distance_between_sprites(self, self.window.tank)
            bullet = Bullet(self.center_x, self.center_y, enemy=True)
            bullet_speed = 3
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
        # draw 2 lines from the center to the edge of the radar
        x1 = self.center_x + 160 * cos(radians(self.radar_angle))
        y1 = self.center_y + 160 * sin(radians(self.radar_angle))
        x2 = self.center_x + 160 * cos(radians(self.radar_angle + 30))
        y2 = self.center_y + 160 * sin(radians(self.radar_angle + 30))
        arcade.draw_line(
            self.center_x, self.center_y, x1, y1, arcade.color.BLUE_GRAY, 0.4
        )
        arcade.draw_line(
            self.center_x, self.center_y, x2, y2, arcade.color.BLUE_GRAY, 0.4
        )
