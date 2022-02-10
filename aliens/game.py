import pygame as pg
import sys

from pygame.sprite import Sprite as sp, Group

import game_functions as gf
from vector import Vector


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (150, 150, 150)
        self.ship_speed_factor = 10

        self.laser_color = (136, 8, 8)
        self.laser_speed_factor = 4
        self.laser_width = 5
        self.laser_height = 20
        self.lasers_allowed = 5


class Alien:
    def __init__(self): pass

    def update(self): pass

    def draw(self): pass


class Laser(sp):
    def __init__(self, game):
        super(Laser, self).__init__()
        self.game = game
        self.screen = game.screen
        self.rect = pg.Rect(0, 0, game.settings.laser_width, game.settings.laser_height)
        self.rect.centerx = game.ship.rect.centerx
        self.rect.top = game.ship.rect.top
        self.y = float(self.rect.y)
        self.color = game.settings.laser_color
        self.speed_factor = game.settings.laser_speed_factor

    def update(self):
        # update the decimal y val, then update the integer pos
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)


class Ship:
    def __init__(self, game, settings):
        self.settings = settings
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
        if rect.centerx - rect.width / 2 <= 0:
            rect.centerx = rect.width / 2

        if rect.centerx + rect.width / 2 >= settings.screen_width:
            rect.centerx = settings.screen_width - rect.width / 2

        if rect.centery + rect.height / 2 >= settings.screen_height:
            rect.centery = settings.screen_height - rect.height / 2

        if rect.centery - rect.height / 2 <= 0:
            rect.centery = rect.height / 2

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


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        pg.display.set_caption("Alien Invasion")
        self.ship = Ship(game=self, settings=self.settings)
        self.lasers = Group()

    def update(self):
        self.ship.update()
        self.lasers.update()

    def play(self):
        finished = False
        while not finished:
            self.update()
            gf.update_screen(game=self)
            gf.check_events(game=self)  # exits game if QUIT pressed
            gf.manage_lasers(game=self)

def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
