from laser import Laser
from vector import Vector
import pygame as pg
from timer import Timer


class Ship:
    def __init__(self, game):
        self.settings = game.settings
        self.game = game
        self.screen = game.screen

        self.normal_image_list = [pg.image.load(f'images/ship/ship{x}.png') for x in range(4)]
        self.death_image_list = [pg.image.load(f'images/ship_death/ship_death{x}.png') for x in range(15)]
        self.image_list = self.normal_image_list
        self.ship_normal_timer = Timer(image_list=self.image_list,
                                       delay=self.settings.ship_image_animation_delay)
        self.ship_image_timer = self.ship_normal_timer
        self.image = self.image_list[self.ship_image_timer.index]
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.center = Vector(self.rect.centerx, self.rect.centery)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.v = Vector()

        self.firing = False
        self.left_laser = True
        self.last_fire_time = pg.time.get_ticks()
        self.last_death_frame_time = 0
        self.dying = False

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
        self.handle_positioning()
        self.clamp()
        self.handle_animation()
        self.handle_collision()

    def alternate_laser(self):
        self.left_laser = not self.left_laser

    def handle_collision(self):
        if pg.sprite.spritecollideany(self, self.game.aliens.group) and not self.dying:
            self.die()

    def handle_positioning(self):
        if self.dying:
            return

        rect = self.rect
        center = self.center
        v = self.v

        center.x = rect.centerx + v.x
        center.y = rect.centery + v.y

        rect.centerx = center.x
        rect.centery = center.y

    def die(self):
        self.ship_image_timer = Timer(image_list=self.death_image_list,
                                      delay=self.settings.ship_death_animation_delay,
                                      is_loop=False)
        self.image_list = self.death_image_list
        self.dying = True
        self.hold_fire_off()

    def handle_animation(self):
        self.image = self.image_list[self.ship_image_timer.index]
        self.ship_image_timer.next_frame()
        if self.firing:
            delay = self.settings.ship_fire_delay
            now = pg.time.get_ticks()
            if now - self.last_fire_time >= delay:
                self.alternate_laser()
                self.fire_laser()
                self.last_fire_time = now
        if self.ship_image_timer.is_expired():
            self.game.reset()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def reset(self):
        self.rect.centerx = self.settings.screen_width / 2
        self.rect.centery = self.settings.screen_height - self.rect.width / 2

        self.dying = False
        self.image_list = self.normal_image_list
        self.ship_image_timer = self.ship_normal_timer
        self.ship_image_timer.reset()
        self.draw()

    def hold_fire_on(self):
        self.firing = True
        if self.dying:
            self.hold_fire_off()

    def hold_fire_off(self):
        self.firing = False

    def fire_laser(self):
        game = self.game
        if len(game.lasers.group) < game.settings.lasers_allowed:
            new_laser = Laser(game, self.left_laser)
            game.lasers.group.add(new_laser)
