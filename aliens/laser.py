import pygame as pg
from pygame.sprite import Sprite as Sp
from pygame.sprite import Group
from timer import Timer


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

    def check_laser_bounds(self):
        for laser in self.group.copy():
            if laser.rect.top <= 0:
                laser.die()

    def draw(self):
        for laser in self.group.sprites():
            laser.draw()


class Laser(Sp):
    def __init__(self, game, left_laser=False):
        super(Laser, self).__init__()
        self.game = game
        self.screen = game.screen
        self.left_laser = left_laser

        self.normal_image_list = [pg.image.load(f'images/lasers/laser{x}.png') for x in range(6)]
        self.normal_laser_timer = Timer(image_list=self.normal_image_list, delay=game.settings.laser_animation_delay)
        self.destroy_image_list = [pg.image.load(f'images/lasers/laserExplode{x}.png') for x in range(3)]
        self.destroy_image_timer = Timer(image_list=self.destroy_image_list, delay=100, is_loop=False)
        self.laser_timer = self.normal_laser_timer

        self.image = self.laser_timer.image()
        self.rect = self.image.get_rect()
        self.rect.top = game.ship.rect.top
        self.y = float(self.rect.y)
        self.color = game.settings.laser_color
        self.speed_factor = game.settings.laser_speed_factor
        self.dying = False

        if self.left_laser:
            self.rect.left = game.ship.rect.left
        else:
            self.rect.right = game.ship.rect.right

    def update(self):
        # update the decimal y val, then update the integer pos
        if self.dying and self.laser_timer.is_expired():
            self.kill()
        self.handle_animation()
        self.check_hit()
        if not self.dying:
            self.handle_positioning()

    def handle_positioning(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def handle_animation(self):
        self.image = self.laser_timer.image()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def die(self):
        if not self.dying:
            self.laser_timer = Timer(image_list=self.destroy_image_list, delay=100, is_loop=False)
            self.dying = True
    # def check_hit_barrier(self):

    def check_hit(self):
        for alien in self.game.aliens.group:
            if pg.sprite.collide_mask(self, alien) and not self.dying:
                self.die()
                alien.lose_life()
                self.game.gameStats.alien_hit(alien)

class AlienLaser(Laser):
    def __init__(self, game, x, y):
        super().__init__(game=game)
        self.y = y
        self.rect.x = x

    def handle_animation(self):
        self.image = pg.transform.flip(self.laser_timer.image(),False, True)

    def handle_positioning(self):
        self.y += self.speed_factor
        self.rect.y = self.y
        if self.hit_bottom():
            self.die()

    def hit_bottom(self):
        return self.rect.bottom > self.game.settings.screen_height

    def check_hit(self):
        return pg.sprite.collide_mask(self, self.game.ship) and not self.dying

    # def check_hit_barrier(self, barrier_element):

