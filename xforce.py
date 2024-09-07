import arcade
from arcade import Sprite, TileMap, SpriteList, gl

from config import *
from entities.explosion import Explosion
from entities.spot import Spot
from entities.tank import Tank
from font import FONTSS_FONT, FSSS_FONT
from resource import Resource


def add_virtual_walls():
    virtual_walls = SpriteList()
    for i in range(0, MAP_WIDTH, CELL_WIDTH):
        virtual_walls.append(
            Sprite(
                texture=Resource.map_textures[-1],
                center_x=i + CELL_WIDTH / 2,
                center_y=-CELL_WIDTH / 2,
                image_width=CELL_WIDTH,
                image_height=CELL_WIDTH,
            )
        )
        virtual_walls.append(
            Sprite(
                texture=Resource.map_textures[-1],
                center_x=i + CELL_WIDTH / 2,
                center_y=MAP_WIDTH + CELL_WIDTH / 2,
                image_width=CELL_WIDTH,
                image_height=CELL_WIDTH,
            )
        )
    for i in range(0, MAP_HEIGHT, CELL_WIDTH):
        virtual_walls.append(
            Sprite(
                texture=Resource.map_textures[-1],
                center_x=-CELL_WIDTH / 2,
                center_y=i + CELL_WIDTH / 2,
                image_width=CELL_WIDTH,
                image_height=CELL_WIDTH,
            )
        )
        virtual_walls.append(
            Sprite(
                texture=Resource.map_textures[-1],
                center_x=MAP_HEIGHT + CELL_WIDTH / 2,
                center_y=i + CELL_WIDTH / 2,
                image_width=CELL_WIDTH,
                image_height=CELL_WIDTH,
            )
        )
    return virtual_walls


class XforceGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.tile_map = None
        self.scene = None
        self.tank = None
        self.camera = arcade.Camera()
        self.gui_camera = arcade.Camera()
        self.camera.scale = 1 / ZOOM_SCALE
        self.physics_engine = None

    def setup(self):
        self.tile_map: TileMap = arcade.load_tilemap(
            "res/map0.tmx",
            layer_options={
                "obstacles": {"use_spatial_hash": True},
                "water": {"use_spatial_hash": True},
            },
        )
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list("spots")
        self.scene.add_sprite_list("tank")
        self.scene.add_sprite_list("virtual_walls", sprite_list=add_virtual_walls())
        self.scene.add_sprite_list("bullets")

        self.tank = Tank(scene=self.scene)
        self.scene.add_sprite("tank", self.tank)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw(filter=gl.NEAREST)
        self.tank.draw_hp()
        self.gui_camera.use()
        FSSS_FONT.draw(f"0123456789.,:!?()-'/AB\n"
                         f"CDEFGHIJKLMNOPQRSTUV\n"
                         f"WXYZÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ\n"
                         f"ÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ<>$%", 15, 10, 6)

    def update(self, delta_time):
        self.scene.update()
        self.update_bullets()
        self.center_camera()

    def update_bullets(self):
        for bullet in self.scene["bullets"]:
            for wall in self.scene["obstacles"]:
                if arcade.check_for_collision(bullet, wall):
                    bullet.remove_from_sprite_lists()
                    self.scene.add_sprite(
                        "explosions", Explosion(bullet.center_x, bullet.center_y)
                    )
                    wall.remove_from_sprite_lists()
                    self.scene.add_sprite("spots", Spot(wall.center_x, wall.center_y))
                    break
            for wall in self.scene["virtual_walls"]:
                if arcade.check_for_collision(bullet, wall):
                    bullet.remove_from_sprite_lists()
                    break

    def center_camera(self):
        camera_position_x = self.tank.center_x - SCREEN_WIDTH // 2
        min_x = int(-CAMERA_WIDTH / 2 * (ZOOM_SCALE - 1))
        max_x = min_x + MAP_WIDTH - CAMERA_WIDTH
        camera_position_x = max(min_x, min(camera_position_x, max_x))
        camera_position_y = self.tank.center_y - SCREEN_HEIGHT // 2
        min_y = int(-CAMERA_HEIGHT / 2 * (ZOOM_SCALE - 1))
        max_y = min_y + MAP_HEIGHT - CAMERA_HEIGHT
        camera_position_y = max(min_y, min(camera_position_y, max_y))
        self.camera.move_to(
            Vec2(
                camera_position_x,
                camera_position_y,
            )
        )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            KeyBoardPress.is_up = True
        elif symbol == arcade.key.DOWN:
            KeyBoardPress.is_down = True
        elif symbol == arcade.key.LEFT:
            KeyBoardPress.is_left = True
        elif symbol == arcade.key.RIGHT:
            KeyBoardPress.is_right = True
        elif symbol == arcade.key.ESCAPE:
            arcade.close_window()
        if symbol == arcade.key.SPACE:
            self.tank.fire()

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
    window = XforceGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
