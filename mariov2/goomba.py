from timer import Timer
import pygame
from tile import *
from settings import TILE_SIZE, TILE_SIZE_SCALED
from spritesheet import *
import copy

class GoombaGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

class Goomba(Tile):
    def __init__(self, map, surface, x, y, groups, width=TILE_SIZE_SCALED, height=TILE_SIZE_SCALED):
        super().__init__(surface, width, height, x, y, groups)
        self.map = map
        self.spritesheet = GoombaSpriteSheet()
        self.image = self.spritesheet.get_sprite('goomba0')
        # self.image = pygame.Surface((60,60))
        self.rect = self.image.get_rect()
        self.rect.x = x*TILE_SIZE_SCALED
        self.rect.y = y*TILE_SIZE_SCALED
        self.img_list = [self.spritesheet.get_sprite('goomba0'), self.spritesheet.get_sprite('goomba0',True)]
        self.death_image = self.spritesheet.get_sprite('goomba2')
        self.img_timer = Timer(image_list=self.img_list)
        self.dx = -1
        self.max_distance = 200
        self.died = False

    def check_hit_tile(self):
        c2 = copy.copy(self.rect)
        c2.x += self.dx
        for tile in self.map.tiles.sprites():
            if tile.rect.colliderect(c2):
                if self.dx < 0:
                    self.rect.left = tile.rect.right
                    self.dx *= -1
                elif self.dx > 0:
                    self.rect.right = tile.rect.left
                    self.dx *= -1

    def die(self):
        if not self.died:
            self.rect.y += 30
            self.dx = 0
            self.died = True
        # super().kill()

    def handle_collision(self):
        self.check_hit_tile()

    def update(self):
        self.handle_collision()
        self.rect.x += self.dx
        if self.died:
            self.image = self.death_image
        else:
            self.image = self.img_timer.image()
        return super().update()