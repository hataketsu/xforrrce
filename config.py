from pyglet.math import Vec2

CELL_WIDTH = 24
ZOOM_SCALE = 3
CAMERA_WIDTH = CELL_WIDTH * 15
CAMERA_HEIGHT = CELL_WIDTH * 12
SCREEN_WIDTH = int(CAMERA_WIDTH * ZOOM_SCALE)
SCREEN_HEIGHT = int(CAMERA_HEIGHT * ZOOM_SCALE)
SCREEN_TITLE = "XForce"


class Direction:
    up = Vec2(0, 1)
    down = Vec2(0, -1)
    left = Vec2(-1, 0)
    right = Vec2(1, 0)
    stand = Vec2(0, 0)


class KeyBoardPress:
    is_up = False
    is_down = False
    is_left = False
    is_right = False
