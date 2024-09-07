import arcade

from config import CELL_WIDTH


class Resource:
    tank_textures = arcade.load_spritesheet(
        "res/img/tank4.png", CELL_WIDTH, CELL_WIDTH, 1, 4
    )
    explo1_textures = arcade.load_spritesheet("res/img/explo1.png", 16, 16, 1, 5)
    map_textures = arcade.load_spritesheet(
        "res/img/t2.png", CELL_WIDTH, CELL_WIDTH, 1, 1896 // CELL_WIDTH
    )
    shot_textures = arcade.load_spritesheet("res/img/shot.png", 6, 6, 2, 4)
    spot_textures = arcade.load_spritesheet("res/img/spot.png", 32, 32, 1, 3)
    fire_sound = arcade.load_sound("res/sound/shoot.wav")
    explode_sound = arcade.load_sound("res/sound/explo.wav")
