import pygame

from settings import *

class SpriteSheet:
    def __init__(self, filename, coord_dict):
        self.sheet = pygame.image.load(filename)
        self.dict = coord_dict
    
    def get_sprite(self, type, flipped=False):
        info = self.dict[type]
        sur = pygame.Surface((info[2], info[3]), pygame.SRCALPHA, 32)
        sur = sur.convert_alpha()
        # sur = pygame.Surface((info[2], info[3]))
        sur.blit(self.sheet, (0, 0), self.dict[type])
        if flipped:
            sur = pygame.transform.flip(sur, True, False)
        return sur

class MarioSpriteSheet(SpriteSheet):
    def __init__(self):
        filename='images/mario.gif'
        coord_dict={'mario0': (25, 25, 50, 70), 'mario1': (85, 30, 50, 65), 'mario2':(150, 25, 60, 65), 'mario3':(350, 25, 70, 70)}
        super().__init__(filename=filename, coord_dict=coord_dict)

class GoombaSpriteSheet(SpriteSheet):
    def __init__(self):
        filename = 'images/goomba.png'
        coord_dict = {'goomba0': (0,0, 165, 165), 'goomba2': (420, 55, 165, 90)}
        super().__init__(filename=filename, coord_dict=coord_dict)

    def get_sprite(self, type, flipped=False):
        res = super().get_sprite(type, flipped)
        info = self.dict[type]
        if type == 'goomba0':
            return pygame.transform.scale(res, (TILE_SIZE_SCALED, TILE_SIZE_SCALED))
        else:
            return pygame.transform.scale(res, (TILE_SIZE_SCALED, info[3]/info[2]*TILE_SIZE_SCALED))