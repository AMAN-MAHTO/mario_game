vertical_tile_number = 11
TILE_SIZE = 64

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = vertical_tile_number * TILE_SIZE

TILE_IMAGE_PATH = {
    'tarrain':'../graphics/terrain/terrain_tiles.png',
    "grass":'../graphics/decoration/grass/grass.png',
    "crates":['../graphics/terrain/crate.png'],
    "fb_palms":["../graphics/terrain/palm_large/large_1.png","../graphics/terrain/palm_small/small_1.png"],
    "bg_palms":["../graphics/terrain/palm_bg/bg_palm_1.png"],
    "coins":"../graphics/coins/coin_tiles.png",
    "enemies":"../graphics/enemy/setup_tile.png",
    "player":"../graphics/character/setup_tiles.png",
    
}

CAMERA_BODERS ={
    'left':100,
    'right':200,
    'top':100,
    'bottom':200
}