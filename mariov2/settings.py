# 3x scale from 480 x 240
SCREEN_WIDTH =  1440
SCREEN_HEIGHT = 720
SCREEN_SCALE = 3

TILE_SIZE = 16
TILE_SIZE_SCALED = TILE_SIZE*SCREEN_SCALE
NUM_TILES = SCREEN_HEIGHT/TILE_SIZE_SCALED

RUN_SPEED = 7
JUMP_SPEED = 15

MAP_SCROLL_SPEED = RUN_SPEED/SCREEN_SCALE