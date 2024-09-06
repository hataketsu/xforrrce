import random
import time

import arcade
from arcade import Sprite, TileMap, SpriteList, PhysicsEngineSimple, gl
from arcade.examples.asteroid_smasher import SCALE
from arcade.physics_engines import _move_sprite
from pyglet.math import Vec2

CELL_WIDTH = 24
MAP_WIDTH = CELL_WIDTH * 20
MAP_HEIGHT = CELL_WIDTH * 20
ZOOM_SCALE = 2
CAMERA_WIDTH = CELL_WIDTH * 15
CAMERA_HEIGHT = CELL_WIDTH * 12
SCREEN_WIDTH = CAMERA_WIDTH * ZOOM_SCALE
SCREEN_HEIGHT = CAMERA_HEIGHT * ZOOM_SCALE
SCREEN_TITLE = "XForce"


class Direction:
    up = Vec2(0, 1)
    down = Vec2(0, -1)
    left = Vec2(-1, 0)
    right = Vec2(1, 0)
    stand = Vec2(0, 0)


class Resource:
    tank_textures = arcade.load_spritesheet("img/tank1.png", CELL_WIDTH, CELL_WIDTH, 1, 4)
    explo1_textures = arcade.load_spritesheet("img/explo1.png", 16, 16, 1, 5)
    map_textures = arcade.load_spritesheet("img/t2.png", CELL_WIDTH, CELL_WIDTH, 1, 1896 // CELL_WIDTH)
    shot_textures = arcade.load_spritesheet("img/shot.png", 6, 6, 2, 4)
    spot_textures = arcade.load_spritesheet("img/spot.png", 32, 32, 1, 3)


class KeyBoardPress:
    is_up = False
    is_down = False
    is_left = False
    is_right = False


class Tank(arcade.Sprite):
    def __init__(self):
        super().__init__(texture=Resource.tank_textures[0])
        self.textures = Resource.tank_textures
        self.center_x = CELL_WIDTH + CELL_WIDTH / 2
        self.center_y = CELL_WIDTH + CELL_WIDTH / 2
        self.direction = Direction.right
        self.fire_direction = None
        self.auto_direction = None
        self.auto_direction_time = 0

    def update(self):
        if KeyBoardPress.is_up and not KeyBoardPress.is_down:
            self.direction = Direction.up
            self.auto_direction = Direction.stand
        elif KeyBoardPress.is_down and not KeyBoardPress.is_up:
            self.direction = Direction.down
            self.auto_direction = Direction.stand
        elif KeyBoardPress.is_right and not KeyBoardPress.is_left:
            self.direction = Direction.right
            self.auto_direction = Direction.stand
        elif KeyBoardPress.is_left and not KeyBoardPress.is_right:
            self.direction = Direction.left
            self.auto_direction = Direction.stand
        else:
            if self.auto_direction:
                self.direction = self.auto_direction
            else:
                self.direction = Direction.stand
            #
            # if self.auto_direction_time < time.time():
            #     self.auto_direction_time = time.time() + random.randint(1, 3)
            #     self.auto_direction = random.choice(
            #         [Direction.up, Direction.down, Direction.left, Direction.right, Direction.stand, Direction.stand])

        if self.direction == Direction.up:
            self.fire_direction = Direction.up
            self.set_texture(3)
        elif self.direction == Direction.down:
            self.fire_direction = Direction.down
            self.set_texture(1)
        elif self.direction == Direction.right:
            self.fire_direction = Direction.right
            self.set_texture(0)
        elif self.direction == Direction.left:
            self.fire_direction = Direction.left
            self.set_texture(2)
        elif self.direction == Direction.stand:
            pass
        self.hit_box = self.texture.hit_box_points

        self.change_x = self.direction[0]
        self.change_y = self.direction[1]
        super().update()


class Explosion(Sprite):
    def __init__(self, center_x, center_y):
        super().__init__(texture=Resource.explo1_textures[0], center_x=center_x, center_y=center_y)
        self.textures = Resource.explo1_textures
        self.center_x = 0
        self.center_y = 0
        self.cur_texture_index = 0
        self.cur_texture = self.textures[self.cur_texture_index]
        self.time = 0

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


class Spot(Sprite):
    def __init__(self, center_x, center_y):
        super().__init__(texture=Resource.spot_textures[0], center_x=center_x, center_y=center_y)
        self.textures = Resource.spot_textures
        self.center_x = 0
        self.center_y = 0
        self.cur_texture_index = 0
        self.cur_texture = self.textures[self.cur_texture_index]
        self.time = 0

    def update(self):
        self.time += 1
        if self.time % (60*10) == 0:
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.textures):
                self.remove_from_sprite_lists()
            else:
                self.cur_texture = self.textures[self.cur_texture_index]
                self.set_texture(self.cur_texture_index)
        super().update()


class Bullet(Sprite):
    def __init__(self):
        super().__init__(texture=Resource.shot_textures[0])
        self.textures = Resource.shot_textures
        self.center_x = 0
        self.center_y = 0
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


class CustomPhysicsEngineSimple(PhysicsEngineSimple):

    def update(self):
        return _move_sprite(self.player_sprite, self.walls, ramp_up=True)


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(int(SCREEN_WIDTH), int(SCREEN_HEIGHT), SCREEN_TITLE)

        self.tile_map: TileMap = None
        self.scene = None
        self.tank = None
        self.camera = arcade.Camera()
        self.camera.scale = 1 / ZOOM_SCALE
        self.physics_engine = None

    def setup(self):
        self.tile_map = arcade.load_tilemap("map0.tmx", layer_options={
            "obstacles": {"use_spatial_hash": True},
            "water": {"use_spatial_hash": True}
        })
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.tank = Tank()
        self.scene.add_sprite_list("spots")
        self.scene.add_sprite("tank", self.tank)
        virtual_walls = SpriteList()
        for i in range(0, MAP_WIDTH, CELL_WIDTH):
            virtual_walls.append(
                Sprite(texture=Resource.map_textures[-1], center_x=i + CELL_WIDTH / 2, center_y=-CELL_WIDTH / 2,
                       image_width=CELL_WIDTH,
                       image_height=CELL_WIDTH))
            virtual_walls.append(
                Sprite(texture=Resource.map_textures[-1], center_x=i + CELL_WIDTH / 2,
                       center_y=MAP_WIDTH + CELL_WIDTH / 2, image_width=CELL_WIDTH,
                       image_height=CELL_WIDTH))
        for i in range(0, MAP_HEIGHT, CELL_WIDTH):
            virtual_walls.append(
                Sprite(texture=Resource.map_textures[-1], center_x=-CELL_WIDTH / 2, center_y=i + CELL_WIDTH / 2,
                       image_width=CELL_WIDTH,
                       image_height=CELL_WIDTH))
            virtual_walls.append(
                Sprite(texture=Resource.map_textures[-1], center_x=MAP_HEIGHT + CELL_WIDTH / 2,
                       center_y=i + CELL_WIDTH / 2, image_width=CELL_WIDTH,
                       image_height=CELL_WIDTH))
        self.scene.add_sprite_list("virtual_walls", sprite_list=virtual_walls)
        self.scene.add_sprite_list("bullets")

        self.physics_engine = CustomPhysicsEngineSimple(self.tank,
                                                        [self.scene['obstacles'], self.scene['water'], virtual_walls])

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw(filter=gl.NEAREST)
        # self.scene.draw_hit_boxes()

    def update(self, delta_time):
        self.scene.update()

        self.physics_engine.update()
        for bullet in self.scene['bullets']:
            for wall in self.scene['obstacles']:
                if arcade.check_for_collision(bullet, wall):
                    print("hit obstacles")
                    bullet.remove_from_sprite_lists()
                    self.scene.add_sprite("explosions", Explosion(bullet.center_x, bullet.center_y))
                    wall.remove_from_sprite_lists()
                    self.scene.add_sprite("spots", Spot(wall.center_x, wall.center_y))
                    break
            for wall in self.scene['virtual_walls']:
                if arcade.check_for_collision(bullet, wall):
                    print("hit virtual wall")
                    bullet.remove_from_sprite_lists()
                    self.scene.add_sprite("explosions", Explosion(bullet.center_x, bullet.center_y))
                    break

        camera_position_x = self.tank.center_x - SCREEN_WIDTH // 2
        min_x = -CAMERA_WIDTH / 2 * (ZOOM_SCALE - 1)
        max_x = min_x + MAP_WIDTH - CAMERA_WIDTH
        camera_position_x = max(min_x, min(camera_position_x, max_x))
        camera_position_y = self.tank.center_y - SCREEN_HEIGHT // 2
        min_y = -CAMERA_HEIGHT / 2 * (ZOOM_SCALE - 1)
        max_y = min_y + MAP_HEIGHT - CAMERA_HEIGHT
        camera_position_y = max(min_y, min(camera_position_y, max_y))
        self.camera.move_to((camera_position_x, camera_position_y, ))

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            KeyBoardPress.is_up = True
        elif symbol == arcade.key.DOWN:
            KeyBoardPress.is_down = True
        elif symbol == arcade.key.LEFT:
            KeyBoardPress.is_left = True
        elif symbol == arcade.key.RIGHT:
            KeyBoardPress.is_right = True
        elif symbol == arcade.key.Q:
            arcade.close_window()
        if symbol == arcade.key.SPACE:
            bullet = Bullet()
            bullet.center_x = self.tank.center_x
            bullet.center_y = self.tank.center_y
            bullet.change_x = self.tank.fire_direction[0] * 3
            bullet.change_y = self.tank.fire_direction[1] * 3
            self.scene.add_sprite("bullets", bullet)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            KeyBoardPress.is_up = False
        elif symbol == arcade.key.DOWN:
            KeyBoardPress.is_down = False
        elif symbol == arcade.key.LEFT:
            KeyBoardPress.is_left = False
        elif symbol == arcade.key.RIGHT:
            KeyBoardPress.is_right = False


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
