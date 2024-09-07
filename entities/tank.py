import arcade
from arcade import PhysicsEngineSimple, Scene, Window

from config import CELL_WIDTH, Direction
from entities.bullet import Bullet
from font import FSSS_FONT
from resource import Resource

BAR_WIDTH = int(CELL_WIDTH * 0.8)
BAR_HEIGHT = 2


class Tank(arcade.Sprite):
    def __init__(self, window:Window):
        super().__init__(texture=Resource.tank_textures[0])
        self.window = window
        self.scene = window.scene
        self.textures = Resource.tank_textures
        self.center_x = CELL_WIDTH + CELL_WIDTH / 2
        self.center_y = CELL_WIDTH + CELL_WIDTH / 2
        self.direction = Direction.right
        self.fire_direction = None
        self.auto_direction = None
        self.auto_direction_time = 0
        self.hp = 100
        self.cooldown = 0
        self.physics_engine = PhysicsEngineSimple(
            self,
            [
                self.scene["destructible"],
                self.scene["barrier"],
                self.scene["indestructible"],
                self.scene["enemies"],
            ],
        )
        self.window.add_message(self.center_x, self.center_y, "Starttt")

    def update(self):
        if self.window.key_map[arcade.key.UP] and not self.window.key_map[arcade.key.DOWN]:
            self.direction = Direction.up
            self.auto_direction = Direction.stand
        elif self.window.key_map[arcade.key.DOWN] and not self.window.key_map[arcade.key.UP]:
            self.direction = Direction.down
            self.auto_direction = Direction.stand
        elif self.window.key_map[arcade.key.RIGHT] and not self.window.key_map[arcade.key.LEFT]:
            self.direction = Direction.right
            self.auto_direction = Direction.stand
        elif self.window.key_map[arcade.key.LEFT] and not self.window.key_map[arcade.key.RIGHT]:
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
        self.cooldown -=1
        if self.window.key_map[arcade.key.SPACE] and self.cooldown <=0:
            self.fire()
            self.cooldown = 20

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
        self.physics_engine.update()
        super().update()

    def draw_hp(self):
        # Draw HP bar, white background, green bar
        arcade.draw_rectangle_filled(
            self.center_x,
            self.center_y + BAR_WIDTH / 2 + 5,
            BAR_WIDTH,
            BAR_HEIGHT,
            arcade.color.WHITE,
        )
        arcade.draw_rectangle_filled(
            self.center_x - BAR_WIDTH / 2 + BAR_WIDTH * self.hp / 100 / 2,
            self.center_y + BAR_WIDTH / 2 + 5,
            BAR_WIDTH * self.hp / 100,
            BAR_HEIGHT,
            arcade.color.GREEN,
        )

    def fire(self):
        bullet = Bullet(self.center_x, self.center_y, damage=20)
        bullet.change_x = self.fire_direction[0] * 2
        bullet.change_y = self.fire_direction[1] * 2
        self.scene.add_sprite("bullets", bullet)
        arcade.play_sound(Resource.fire_sound)
