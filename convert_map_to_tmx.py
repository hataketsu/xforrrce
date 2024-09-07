from map import MapInfo


template = """<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" tiledversion="1.11.0" orientation="orthogonal" renderorder="left-down" width="WIDTH_PLACEHOLDER" height="HEIGHT_PLACEHOLDER" tilewidth="24" tileheight="24" infinite="0" nextlayerid="5" nextobjectid="1">
 <tileset firstgid="1" source="tTILE_PLACEHOLDER.tsx"/>
 <layer id="1" name="ground" width="WIDTH_PLACEHOLDER" height="HEIGHT_PLACEHOLDER">
  <data encoding="csv">
  DATA_PLACEHOLDER
</data>
 </layer>
</map>
"""


def convert_map_to_tmx(map_index):
    input_file = "./res/map/map" + str(map_index)
    output_file = "./res/map" + str(map_index) + ".tmx"
    with open(input_file, "rb") as f:
        data = f.read()
    tile_map, width, height = MapInfo().get_map_info(map_index)[:3]
    buf = []
    for c in data:
        c = min(c, 79)
        buf.append(str(c))
    data = ",".join(buf)
    output = (
        template.replace("WIDTH_PLACEHOLDER", str(width))
        .replace("HEIGHT_PLACEHOLDER", str(height))
        .replace("DATA_PLACEHOLDER", data)
        .replace("TILE_PLACEHOLDER", str(tile_map))
    )
    with open(output_file, "w") as f:
        f.write(output)


for i in range(1, 32):
    convert_map_to_tmx(i)
