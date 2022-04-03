import pygame
from goomba import *
from settings import *
from tile import *
from lvlmeta import *

WHITE = (255,255,255)
BLACK = (0,0,0)
class Map:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.map_assets = MapGroup()
        self.tiles = TilesGroup()
        self.goombas = GoombaGroup()
        # 3376 x 480 original pane
        self.dim_x = 3376
        self.dim_y = 480
        self.world11_img = pygame.image.load('images/world11.png')
        # self.draw_grid(self.world11_img)
        # Crop part of the original image onto a surface, then scale that image into the display
        # The camera coord is the rectangle that will be displayed
        self.surface = pygame.Surface((self.dim_y, self.dim_y/2))
        self.camera_coord = [0, 0, self.dim_y, self.dim_y/2]
        self.surface.blit(self.world11_img, (0, 0), self.camera_coord)
        # 211 horizontal and 30 boxes vertical, 16 x 16 boxes, display is *3 scale
        self.picture = pygame.transform.scale(self.surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.create_map(WORLD_ONE, LVL_ONE)

    def draw_camera(self):
        self.surface.blit(self.world11_img, (0, 0), self.camera_coord)
        self.picture = pygame.transform.scale(self.surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw_grid(self, surface):
        tile_size = 16
        font = pygame.font.Font('freesansbold.ttf', 8)
        for x in range(0,int(self.dim_x/tile_size)):
            pygame.draw.line(surface, WHITE, (x*tile_size, 0), (x*tile_size, SCREEN_HEIGHT))
            for y in range(0, int(self.dim_y/tile_size)):
                pygame.draw.line(surface, WHITE, (0, y*tile_size), (SCREEN_WIDTH, y*tile_size))
                text = font.render(f'{x},{y}', True, BLACK, WHITE)
                textRect = text.get_rect()
                textRect.topleft = (x*tile_size, y*tile_size)
                surface.blit(text, textRect)

    def create_map(self, world, level):
        platforms = [(16,9), (20,9), (22,5), (21,9), (22,9), (23,9), (24,9)]
        map = []
        for i in range(15):
            map.append([])
            for j in range(30):
                map[i].append(0)
        for i in range(30):
            map[-1][i] = 1
            map[-2][i] = 1
        for x,y in platforms:
            map[y][x] = 1
        
        # see levelmeta.py
        for name, locations in WORLDS[world][level].items():
            if name == 'floor':
                for index_arrs in locations:
                    for x in index_arrs:
                        FloorTile(self.screen, TILE_SIZE_SCALED, TILE_SIZE_SCALED, x,NUM_TILES-2, [self.tiles, self.map_assets])
                        FloorTile(self.screen, TILE_SIZE_SCALED, TILE_SIZE_SCALED, x,NUM_TILES-1, [self.tiles, self.map_assets])
            if name == 'green_tube':
                for tubes in locations:
                    width, height = tubes[0], tubes[1]
                    for x in tubes[2]:
                        GreenTube(self.screen, width, height, x, NUM_TILES-2-height, [self.tiles, self.map_assets])
            if name == 'question':
                for x,y in locations:
                    QuestionTile(self.screen, TILE_SIZE_SCALED, TILE_SIZE_SCALED, x, y, [self.tiles, self.map_assets])
            if name == 'bricks':
                for x,y in locations:
                    BrickTile(self.screen, TILE_SIZE_SCALED, TILE_SIZE_SCALED, x, y, [self.tiles, self.map_assets])
            if name=='stone':
                for x,y in locations:
                    StoneFloorTile(self.screen, TILE_SIZE_SCALED, TILE_SIZE_SCALED, x, y, [self.tiles, self.map_assets])
            if name =='goomba':
                for y, xarr in locations:
                    for x in xarr:
                        print((x,y))
                        Goomba(self, self.screen, x=x, y=y, groups=[self.goombas, self.map_assets])

    def player_at_middle(self):
        return self.game.player.rect.right > SCREEN_WIDTH/2

    def reached_end(self):
        return self.camera_coord[0] + self.dim_y > self.dim_x

    def update(self):
        # if the player gets to >= cam_pos_x middle of the screen,
        if self.player_at_middle() and not self.game.player.died and not self.reached_end():
        # change the camera coordinates to:
        # cam_pos_x = cam_pos_x + (player_pox_x - cam_pos_middle_x)
            self.camera_coord[0] += MAP_SCROLL_SPEED
            self.map_assets.scroll_left()
            self.draw_camera()
        self.draw()

    def draw(self):
        self.screen.blit(self.picture, (0,0))
        self.map_assets.update()