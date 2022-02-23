from laser import Laser
from vector import Vector
import pygame as pg


class Ship:
    def __init__(self, game):
        self.settings = game.settings
        self.game = game
        self.screen = game.screen
        self.image = pg.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.center = Vector(self.rect.centerx, self.rect.centery)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.v = Vector()

    def moving(self, vector):
        self.v = vector

    def inc_add(self, other):
        self.v += other

    def clamp(self):
        settings = self.settings
        rect = self.rect

        hit = {'LEFT': rect.centerx - rect.width / 2 <= 0,
               'RIGHT': rect.centerx + rect.width / 2 >= settings.screen_width,
               'BOTTOM': rect.centery + rect.height / 2 >= settings.screen_height,
               'TOP': rect.centery - rect.height / 2 <= 0}

        positions = {'LEFT': rect.width / 2,
                     'RIGHT': settings.screen_width - rect.width / 2,
                     'BOTTOM': settings.screen_height - rect.height / 2,
                     'TOP': rect.height / 2}

        if hit['LEFT']:
            rect.centerx = positions['LEFT']

        if hit['RIGHT']:
            rect.centerx = positions['RIGHT']

        if hit['BOTTOM']:
            rect.centery = positions['BOTTOM']

        if hit['TOP']:
            rect.centery = positions['TOP']

    def update(self):
        rect = self.rect
        center = self.center
        v = self.v

        center.x = rect.centerx + v.x
        center.y = rect.centery + v.y

        rect.centerx = center.x
        rect.centery = center.y
        self.clamp()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.centerx = self.settings.screen_width/2
        self.rect.centery = self.settings.screen_height - self.rect.width/2
        self.draw()

    def fire_laser(self):
        game = self.game
        if len(game.lasers.group) < game.settings.lasers_allowed:
            new_laser = Laser(game)
            game.lasers.group.add(new_laser)
