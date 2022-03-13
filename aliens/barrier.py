import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint
from timer import CommandTimer


# from alien import Alien
# from stats import Stats


class Barriers:
    def __init__(self, game):
        self.game = game
        # self.alien_fleet = game.alien_fleet
        self.group = Group()
        self.create_barriers()

    def update(self):
        for barrier in self.group.sprites():
            barrier.update()

    def draw(self):
        for barrier in self.group.sprites():
            barrier.draw()

    def create_barriers(self):
        screen_width = self.game.settings.screen_width
        screen_height = self.game.settings.screen_height
        space_apart = screen_width / 5
        width = space_apart * 0.5

        wh = [int(width), int(width)]
        for i in range(5):
            ul = [space_apart*i + width/2, int(screen_height * 0.7)]
            barrier = Barrier(game=self.game, ul=ul, wh=wh)
            self.group.add(barrier)


class Barrier(Sprite):
    def __init__(self, game, ul, wh):
        super().__init__()
        # img_list = [pg.image.load(f'images/barrier/barrier{x}.png') for x in range(5)]
        self.game = game
        self.group = Group()
        self.ul = ul
        self.wh = wh
        for row in range(0,wh[0], 4):
            for col in range(0,wh[1],4):
                be = BarrierElement(game=game,
                                    ul=(ul[0] + col, ul[1] + row), wh=(10, 10))
                self.group.add(be)

    def update(self):
        collisions = pg.sprite.groupcollide(self.group, self.game.lasers.group, False, False)
        collisions2 = pg.sprite.groupcollide(self.group, self.game.aliens.alien_lasers, False, False)
        for be in collisions:
            for laser in collisions[be]:
                laser.die()
            be.kill()
        for be in collisions2:
            for laser in collisions2[be]:
                laser.die()
            be.kill()


    def draw(self):
        for be in self.group.sprites():
            be.draw()


class BarrierElement(Sprite):
    def __init__(self, game, ul, wh):
        super().__init__()
        self.game = game
        self.ul = ul
        self.wh = wh
        self.rect = pg.Rect(ul[0], ul[1], wh[0], wh[1])
        # self.timer = CommandTimer(image_list=img_list, is_loop=False)
        # self.image = pg.image.load('images/barrier/barrier0.png')#self.timer.image()

    # def update(self):
    #     if self.hit():
    #         self.die()
    #
    #
    # def hit(self):
    #     return pg.sprite.spritecollideany(self, self.game.lasers.group)
    #     # self.timer.next_frame()
    #     # self.image = self.timer.image()
    #     # if self.timer.is_expired():
    #     self.kill()
    def die(self):
        self.kill()

    def draw(self):
        # image = self.timer.image()
        # rect = self.image.get_rect()
        # rect.x, rect.y = self.rect.x, self.rect.y
        self.game.screen.fill((120,120,120), self.rect)
