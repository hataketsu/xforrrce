import random

import arcade
from arcade import Sprite, TileMap, SpriteList, gl

from config import *
from entities.cloud import Cloud
from entities.explosion import Explosion
from entities.message import Message
from entities.objects import ID_TO_TILE, TileType
from entities.sentry import Sentry
from entities.spot import Spot
from entities.tank import Tank
from font import FSSS_FONT
from map import MapInfo
from resource import Resource


class XforceGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.cloud = None
        self.map_textures = None
        self.tile_set_index = None
        self.tile_map = None
        self.scene = None
        self.tank = None
        self.camera = arcade.Camera()
        self.gui_camera = arcade.Camera()
        self.camera.scale = 1 / ZOOM_SCALE
        self.physics_engine = None
        self.map_width = 0
        self.map_height = 0
        self.map_index = 30
        self.key_map = {
            arcade.key.UP: False,
            arcade.key.DOWN: False,
            arcade.key.LEFT: False,
            arcade.key.RIGHT: False,
            arcade.key.SPACE: False,
        }
        self.messages = []

    def setup(self):
        self.tile_map: TileMap = arcade.load_tilemap(f"res/map{self.map_index}.tmx")
        self.tile_set_index = MapInfo().get_map_info(self.map_index)[0]
        self.map_textures = arcade.load_spritesheet(
            f"res/img/t{self.tile_set_index}.png",
            CELL_WIDTH,
            CELL_WIDTH,
            1,
            1896 // CELL_WIDTH,
        )
        self.map_width = self.tile_map.width * CELL_WIDTH
        self.map_height = self.tile_map.height * CELL_WIDTH
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list(
            "indestructible",
            use_spatial_hash=True,
            sprite_list=self.add_virtual_walls(self.map_width, self.map_height),
        )
        self.scene.add_sprite_list("destructible", use_spatial_hash=True)
        self.scene.add_sprite_list("enemies", use_spatial_hash=True)
        self.scene.add_sprite_list("barrier", use_spatial_hash=True)
        self.scene.add_sprite_list("spots")
        self.scene.add_sprite_list("tank")
        self.scene.add_sprite_list("bullets")
        self.scene.add_sprite_list("cloud")

        self.tank = Tank(window=self)
        self.scene.add_sprite("tank", self.tank)
        for i in range(7):
            self.scene.add_sprite("cloud", Cloud(
                self,
                center_x=random.randint(0, self.map_width),
                center_y=random.randint(0, self.map_height),
            ))
        for sprite in self.scene["ground"]:
            if "tile_id" not in sprite.properties:
                continue
            tile_id = sprite.properties["tile_id"]
            tile_object = ID_TO_TILE[tile_id]
            if tile_object.tile_type == TileType.DESTRUCTIBLE:
                self.scene.add_sprite(
                    "ground",
                    Sprite(
                        texture=self.map_textures[0],
                        center_x=sprite.center_x,
                        center_y=sprite.center_y,
                    ),
                )
                if tile_object.name == "sentry":
                    sprite.remove_from_sprite_lists()
                    sentry = Sentry(self, sprite.center_x, sprite.center_y)
                    self.scene.add_sprite("enemies", sentry)
                else:
                    self.scene.add_sprite("destructible", sprite)
            elif tile_object.tile_type == TileType.INDESTRUCTIBLE:
                self.scene.add_sprite("indestructible", sprite)
            elif tile_object.tile_type == TileType.BARRIER:
                self.scene.add_sprite("barrier", sprite)

    def add_virtual_walls(self, map_width, map_height):
        virtual_walls = SpriteList()
        for i in range(0, map_width, CELL_WIDTH):
            virtual_walls.append(
                Sprite(
                    texture=self.map_textures[-1],
                    center_x=i + CELL_WIDTH / 2,
                    center_y=-CELL_WIDTH / 2,
                    image_width=CELL_WIDTH,
                    image_height=CELL_WIDTH,
                )
            )
            virtual_walls.append(
                Sprite(
                    texture=self.map_textures[-1],
                    center_x=i + CELL_WIDTH / 2,
                    center_y=map_height + CELL_WIDTH / 2,
                    image_width=CELL_WIDTH,
                    image_height=CELL_WIDTH,
                )
            )
        for i in range(0, map_height, CELL_WIDTH):
            virtual_walls.append(
                Sprite(
                    texture=self.map_textures[-1],
                    center_x=-CELL_WIDTH / 2,
                    center_y=i + CELL_WIDTH / 2,
                    image_width=CELL_WIDTH,
                    image_height=CELL_WIDTH,
                )
            )
            virtual_walls.append(
                Sprite(
                    texture=self.map_textures[-1],
                    center_x=map_width + CELL_WIDTH / 2,
                    center_y=i + CELL_WIDTH / 2,
                    image_width=CELL_WIDTH,
                    image_height=CELL_WIDTH,
                )
            )
        return virtual_walls

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw(filter=gl.NEAREST)
        self.tank.draw_hp()

        for message in self.messages:
            message.draw()
            if message.time_to_live <0:
                self.messages.remove(message)

        self.gui_camera.use()
        FSSS_FONT.draw(f"HP: {self.tank.hp}", 10, 10 , 4)

        # for sprite in self.scene["ground"]:
        #     if "tile_id" not in sprite.properties:
        #         continue
        #     tile_id = sprite.properties["tile_id"]
        #
        #     FSSS_FONT.draw(
        #         str(tile_id),
        #         sprite.center_x,
        #         sprite.center_y,
        #         scale=1,
        #     )

    def update(self, delta_time):
        self.scene.update()
        self.update_bullets()
        self.center_camera()

    def update_bullets(self):
        for bullet in self.scene["bullets"]:
            if not bullet.enemy:
                for wall in self.scene["destructible"]:
                    if arcade.check_for_collision(bullet, wall):
                        bullet.remove_from_sprite_lists()
                        self.scene.add_sprite(
                            "explosions", Explosion(bullet.center_x, bullet.center_y)
                        )
                        wall.remove_from_sprite_lists()
                        self.scene.add_sprite("spots", Spot(wall.center_x, wall.center_y))
                        break
                for enemy in self.scene["enemies"]:
                    if arcade.check_for_collision(bullet, enemy):
                        bullet.remove_from_sprite_lists()
                        self.scene.add_sprite(
                            "explosions", Explosion(bullet.center_x, bullet.center_y)
                        )
                        enemy.hp -= bullet.damage
                        self.add_message(enemy.center_x, enemy.center_y, f"-{bullet.damage}HP")
                        break
                for wall in self.scene["indestructible"]:
                    if arcade.check_for_collision(bullet, wall):
                        bullet.remove_from_sprite_lists()
                        self.scene.add_sprite(
                            "explosions", Explosion(bullet.center_x, bullet.center_y)
                        )
                        break
            else:
                if arcade.check_for_collision(bullet, self.tank):
                    bullet.remove_from_sprite_lists()
                    self.scene.add_sprite(
                        "explosions", Explosion(bullet.center_x, bullet.center_y)
                    )
                    self.tank.hp -= bullet.damage
                    self.add_message(self.tank.center_x, self.tank.center_y, f"-{bullet.damage}HP")
                    if self.tank.hp <= 0:
                        self.tank.remove_from_sprite_lists()
                        self.scene.add_sprite(
                            "explosions", Explosion(self.tank.center_x, self.tank.center_y)
                        )
                for wall in self.scene["indestructible"]:
                    if arcade.check_for_collision(bullet, wall):
                        bullet.remove_from_sprite_lists()
                        self.scene.add_sprite(
                            "explosions", Explosion(bullet.center_x, bullet.center_y)
                        )
                        break
    def center_camera(self):
        camera_position_x = self.tank.center_x - SCREEN_WIDTH // 2
        min_x = int(-CAMERA_WIDTH / 2 * (ZOOM_SCALE - 1))
        max_x = min_x + self.map_width - CAMERA_WIDTH
        camera_position_x = max(min_x, min(camera_position_x, max_x))
        camera_position_y = self.tank.center_y - SCREEN_HEIGHT // 2
        min_y = int(-CAMERA_HEIGHT / 2 * (ZOOM_SCALE - 1))
        max_y = min_y + self.map_height - CAMERA_HEIGHT
        camera_position_y = max(min_y, min(camera_position_y, max_y))
        self.camera.move_to(
            Vec2(
                camera_position_x,
                camera_position_y,
            )
        )

    def on_key_press(self, symbol: int, modifiers: int):
        self.key_map[symbol] = True
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()


    def on_key_release(self, symbol: int, modifiers: int):
        self.key_map[symbol] = False

    def add_message(self, center_x, center_y, message):
        self.messages.append(Message(center_x, center_y, message))
def main():
    window = XforceGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
