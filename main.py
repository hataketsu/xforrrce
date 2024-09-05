import random

import arcade
from arcade import Sprite
from pyglet.math import Vec2

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
SCREEN_TITLE = "XForce"


class Direction:
    up = Vec2(0, 1)
    down = Vec2(0, -1)
    left = Vec2(-1, 0)
    right = Vec2(1, 0)
    stand = Vec2(0, 0)


class Resource:
    tank_textures = arcade.load_spritesheet("img/tank1.png", 24, 24, 1, 4)
    explo1_textures = arcade.load_spritesheet("img/explo1.png", 24, 24, 1, 5)


class Tank(arcade.Sprite):
    def __init__(self):
        super().__init__(texture=Resource.tank_textures[0])
        self.textures = Resource.tank_textures
        self.center_x = 24 + 12
        self.center_y = 24 + 12
        self.direction = Direction.up

    def update(self):
        self.change_x = self.direction[0]
        self.change_y = self.direction[1]
        super().update()

        if self.direction == Direction.up:
            self.set_texture(3)
        elif self.direction == Direction.down:
            self.set_texture(1)
        elif self.direction == Direction.right:
            self.set_texture(0)
        elif self.direction == Direction.left:
            self.set_texture(2)

        if random.randint(0,
                          100) < 3 or self.center_x < 0 or self.center_x > 24 * 20 or self.center_y < 0 or self.center_y > 24 * 20:
            self.direction = random.choice(
                [Direction.up, Direction.down, Direction.left, Direction.right, Direction.stand, Direction.stand,
                 Direction.stand])


class Explosion(arcade.Sprite):
    def __init__(self):
        super().__init__(texture=Resource.explo1_textures[0])
        self.textures = Resource.explo1_textures
        self.center_x = 24 + 12
        self.center_y = 24 + 12
        self.frame = 0
        self.frame_per_second = 10

    def update(self):
        self.update_animation()

    def update_animation(self, delta_time: float = 1 / 60):
        self.frame += delta_time
        if int(self.frame * self.frame_per_second) >= len(self.textures):
            self.kill()
        else:
            self.set_texture(int(self.frame * self.frame_per_second))

    def on_update(self, delta_time):
        print("update")


class Map(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        with open("./map/map0", 'rb') as f:
            self.map_bytes = f.read()
        self.map = []
        self.map_width = 20
        self.map_height = 20
        for i in range(self.map_width):
            self.map.append([])
            for j in range(self.map_height):
                self.map[i].append(self.map_bytes[i * self.map_width + j])
        self.textures = arcade.load_spritesheet("img/t1.png", 24, 24, 1, 1896 // 24)

        for i in range(self.map_width):
            for j in range(self.map_height):
                index = self.map_bytes[i * self.map_width + j] - 1
                if index >= len(self.textures):
                    index = -1
                sprite = Sprite(texture=self.textures[index])
                sprite.center_x = j * 24 + 12
                sprite.center_y = 24 * 20 - i * 24 - 12
                self.append(sprite)


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.tank = Tank()
        self.map = Map()
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.map.draw()
        self.tank.draw()

    def update(self, delta_time):
        self.tank.update()
        self.map.update()
        camera_position_x = max(0, min(self.tank.center_x - SCREEN_WIDTH // 2, 24 * 20 - SCREEN_WIDTH))
        camera_position_y = max(0, min(self.tank.center_y - SCREEN_HEIGHT // 2, 24 * 20 - SCREEN_HEIGHT))
        camera_position = Vec2(camera_position_x, camera_position_y)
        self.camera.move_to(camera_position)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        if symbol == arcade.key.SPACE:
            explosion = Explosion()
            explosion.center_x = self.tank.center_x
            explosion.center_y = self.tank.center_y
            self.map.append(explosion)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
