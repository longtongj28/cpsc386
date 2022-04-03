import pygame
from settings import *


class MapGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def scroll_left(self):
        for sprite in self.sprites():
            sprite.camera_offset()

class TilesGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

class Tile(pygame.sprite.Sprite):
    def __init__(self, surface, width, height, x, y, groups):
        super().__init__(groups)
        self.surface = surface
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        # self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x*TILE_SIZE_SCALED
        self.rect.y = y*TILE_SIZE_SCALED

    def camera_offset(self):
        self.rect.x -= MAP_SCROLL_SPEED*SCREEN_SCALE

    def update(self):
        self.draw()

    def draw(self):
        self.surface.blit(self.image, self.rect)

class FloorTile(Tile):
    def __init__(self, surface, width, height, x, y, groups):
        super().__init__(surface, width, height, x, y, groups)

class GreenTube(Tile):
    def __init__(self, surface, width, height, x, y, groups):
        width *= TILE_SIZE_SCALED
        height *= TILE_SIZE_SCALED
        super().__init__(surface, width, height, x, y, groups)

class QuestionTile(Tile):
    def __init__(self, surface, width, height, x, y, groups):
        super().__init__(surface, width, height, x, y, groups)

class BrickTile(Tile):
    def __init__(self, surface, width, height, x, y, groups):
        super().__init__(surface, width, height, x, y, groups)

class StoneFloorTile(Tile):
    def __init__(self, surface, width, height, x, y, groups):
        super().__init__(surface, width, height, x, y, groups)