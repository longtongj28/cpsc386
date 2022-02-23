import pygame as pg
from pygame.sprite import Sprite as Sp
from pygame.sprite import Group


class LasersGroup:
    def __init__(self, game):
        self.group = Group()
        self.game = game

    def reset(self):
        self.group.empty()

    def update(self):
        for laser in self.group.sprites():
            laser.update()
        self.check_laser_bounds()
        self.check_collisions()

    def check_collisions(self):
        collisions = pg.sprite.groupcollide(self.group, self.game.aliens.group, True, True)

    def check_laser_bounds(self):
        for laser in self.group.copy():
            if laser.rect.bottom <= 0:
                self.group.remove(laser)

    def draw(self):
        for laser in self.group.sprites():
            laser.draw()


class Laser(Sp):
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
