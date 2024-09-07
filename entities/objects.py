from enum import Enum

from attr import dataclass


class TileType(str, Enum):
    DESTRUCTIBLE = "destructible"
    INDESTRUCTIBLE = "indestructible"
    BARRIER = "barrier"
    GROUND = "ground"


@dataclass
class TileObject:
    name: str
    tile_id: int
    tile_type: str


TILES = [
    TileObject(name="ground", tile_id=0, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=1, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=2, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=3, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=4, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=5, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=6, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=7, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=8, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=9, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=10, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=11, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=12, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=13, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=14, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=15, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=16, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=17, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=18, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=19, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=20, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=21, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=22, tile_type=TileType.GROUND),
    TileObject(name="ground", tile_id=23, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=24, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=25, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=26, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=27, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=28, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=29, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=30, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=31, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=32, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=33, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=34, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=35, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=36, tile_type=TileType.BARRIER),
    TileObject(name="ground", tile_id=37, tile_type=TileType.BARRIER),
    TileObject(name="heli_base", tile_id=38, tile_type=TileType.GROUND),
    TileObject(name="bush", tile_id=39, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="house", tile_id=40, tile_type=TileType.INDESTRUCTIBLE),
    TileObject(name="house", tile_id=41, tile_type=TileType.BARRIER),
    TileObject(name="pole", tile_id=42, tile_type=TileType.BARRIER),
    TileObject(name="pole", tile_id=43, tile_type=TileType.BARRIER),
    TileObject(name="gunner_ground", tile_id=44, tile_type=TileType.GROUND),
    TileObject(name="gunner", tile_id=45, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="sentry", tile_id=46, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="sentry", tile_id=47, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="ship", tile_id=48, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="log", tile_id=49, tile_type=TileType.BARRIER),
    TileObject(name="barrier", tile_id=50, tile_type=TileType.BARRIER),
    TileObject(name="rail", tile_id=51, tile_type=TileType.GROUND),
    TileObject(name="rail", tile_id=52, tile_type=TileType.GROUND),
    TileObject(name="sentry_ground", tile_id=53, tile_type=TileType.GROUND),
    TileObject(name="sentry_ground", tile_id=54, tile_type=TileType.GROUND),
    TileObject(name="sentry_ground", tile_id=55, tile_type=TileType.GROUND),
    TileObject(name="sentry_ground", tile_id=56, tile_type=TileType.GROUND),
    TileObject(name="ship_ground", tile_id=57, tile_type=TileType.GROUND),
    TileObject(name="hole", tile_id=58, tile_type=TileType.GROUND),
    TileObject(name="box", tile_id=59, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="barrel", tile_id=60, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="wall", tile_id=61, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="wall", tile_id=61, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="wall", tile_id=62, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="wall", tile_id=63, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="house", tile_id=64, tile_type=TileType.INDESTRUCTIBLE),
    TileObject(name="house", tile_id=65, tile_type=TileType.INDESTRUCTIBLE),
    TileObject(name="house", tile_id=66, tile_type=TileType.INDESTRUCTIBLE),
    TileObject(name="house", tile_id=67, tile_type=TileType.INDESTRUCTIBLE),
    TileObject(name="house", tile_id=68, tile_type=TileType.INDESTRUCTIBLE),
    TileObject(name="house", tile_id=69, tile_type=TileType.INDESTRUCTIBLE),
    TileObject(name="house", tile_id=70, tile_type=TileType.INDESTRUCTIBLE),
    TileObject(name="house", tile_id=71, tile_type=TileType.INDESTRUCTIBLE),
    TileObject(name="bush", tile_id=72, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="house", tile_id=73, tile_type=TileType.INDESTRUCTIBLE),
    TileObject(name="car", tile_id=74, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="car", tile_id=75, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="car", tile_id=76, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="silo", tile_id=77, tile_type=TileType.DESTRUCTIBLE),
    TileObject(name="base", tile_id=78, tile_type=TileType.GROUND),
    TileObject(name="base", tile_id=79, tile_type=TileType.GROUND),
]

ID_TO_TILE = {tile.tile_id: tile for tile in TILES}
