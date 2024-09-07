import PIL
import arcade
from arcade import gl, Sprite


class Font:
    def __init__(self, image, widths, space, chars):
        self.image = image
        self.widths = widths
        self.space = space
        self.chars = chars
        self.fonts = []
        image_width, image_height = PIL.Image.open(image).size
        self.font_height = image_height // len(self.chars)
        textures = arcade.load_spritesheet(
            self.image, image_width, self.font_height, 1, len(self.chars)
        )
        for index in range(len(textures)):
            texture = textures[index]
            width = self.widths[index]
            self.fonts.append(
                Sprite(
                    texture=texture, image_width=width, image_height=self.font_height
                )
            )

    def draw(self, text, x_pos, y_pos, scale=1):
        original_x_pos = x_pos
        center_y = y_pos + self.font_height * scale / 2
        for char in str.upper(text):
            if char == "\n":
                center_y += self.font_height * scale + self.space * scale
                x_pos = original_x_pos
                continue
            char_index = self.chars.find(char)
            if char_index >= 0:
                char_sprite = self.fonts[char_index]
                char_sprite.center_x = x_pos + self.widths[char_index] * scale / 2
                char_sprite.center_y = center_y
                char_sprite.scale = scale
                char_sprite.draw(filter=gl.NEAREST)
                x_pos += self.widths[char_index] * scale + self.space * scale


FSSS_FONT = Font(
    "res/font/fsss.png",
    [
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        7,
        5,
        3,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        7,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        7,
        5,
        5,
        5,
        3,
    ],
    2,
    "0123456789+-%$:ABCDEFGHIJKLMNOPQRSTUVWXYZ.",
)

FONTSS_FONT = Font(
    "res/font/fontSS.png",
    [
        5,
        2,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        3,
        3,
        3,
        3,
        5,
        4,
        4,
        4,
        2,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        4,
        5,
        5,
        5,
        6,
        5,
        5,
        5,
        5,
        5,
        5,
        4,
        5,
        6,
        6,
        6,
        6,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        4,
        4,
        4,
        4,
        4,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        6,
        6,
        6,
        6,
        6,
        5,
        5,
        5,
        6,
        5,
    ],
    4,
    "0123456789.,:!?()-'/ABCDEFGHIJKLMNOPQRSTUVWXYZÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ<>$%",
)
