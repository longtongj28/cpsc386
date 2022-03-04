from time import sleep

import pygame as pg
from pygame.sprite import Sprite as Sp, Group

from cpsc386.aliens.timer import Timer


class AlienFleet:
    def __init__(self, game):
        self.game = game
        self.alien = Alien(self.game)
        self.group = Group()
        self.num_aliens_per_row = self.get_num_aliens_x()
        self.num_aliens_per_col = self.get_num_aliens_y()
        self.create_all_aliens()

    def update(self):
        if len(self.group) == 0:
            self.game.reset()
        self.check_fleet_edge()
        for alien in self.group.sprites():
            alien.update()

    def check_fleet_edge(self):
        for alien in self.group.sprites():
            if alien.handle_hit_bottom():
                break
            if alien.check_edges():
                self.change_fleet_dir()
                break

    def change_fleet_dir(self):
        self.game.settings.alien_fleet_direction *= -1
        for alien in self.group.sprites():
            alien.move_down()

    def respawn(self):
        self.game.lasers.group.empty()
        self.group.empty()
        self.create_all_aliens()
        self.game.settings.alien_fleet_direction = 1
        self.draw()

    def draw(self):
        for alien in self.group.sprites():
            alien.draw()

    def create_all_aliens(self):
        for i in range(self.num_aliens_per_row):
            for j in range(self.num_aliens_per_col):
                self.create_alien_at(i, j)

    def create_alien_at(self, x, y):
        alien_width = self.alien.rect.width
        alien_height = self.alien.rect.height
        alien = Alien(self.game)

        alien.x = alien_width + 2 * alien_width * x
        alien.y = alien_height + 2 * alien_height * y
        alien.rect.x = alien.x
        alien.rect.y = alien.y

        self.group.add(alien)

    def get_num_aliens_x(self):
        alien_width = Alien(self.game).rect.width
        game = self.game
        available_space_x = game.settings.screen_width - 2 * alien_width
        num_aliens_x = int(available_space_x / (2 * alien_width))
        return num_aliens_x

    def get_num_aliens_y(self):
        settings = self.game.settings
        alien_height = self.alien.rect.height
        ship_height = self.game.ship.rect.height

        available_space_y = (settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))

        return number_rows

    def move_down(self):
        for alien in self.group.sprites():
            alien.move_down()


class Alien(Sp):
    def __init__(self, game, alien_type="alienOne"):
        super(Alien, self).__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings

        self.normal_image_list = [pg.image.load(f'images/{alien_type}/{alien_type}{x}.png') for x in range(2)]
        self.death_image_list = [pg.image.load(f'images/{alien_type}Death/{alien_type}Death{x}.png') for x in range(5)]
        self.image_list = self.normal_image_list
        self.alien_normal_timer = Timer(image_list=self.image_list, delay=self.settings.alien_animation_delay)
        self.alien_death_timer = Timer(image_list=self.death_image_list, delay=self.settings.alien_animation_delay, is_loop=False)
        self.alien_image_timer = self.alien_normal_timer
        self.image = self.image_list[self.alien_image_timer.index]
        self.last_animation_time = pg.time.get_ticks()
        self.dying = False

        self.rect = self.image.get_rect()

        # integer coords
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        speed = self.game.settings.alien_speed_factor
        direction = self.game.settings.alien_fleet_direction
        self.x += speed * direction
        self.rect.x = self.x
        self.handle_animation()

    def handle_animation(self):
        self.image = self.image_list[self.alien_image_timer.index]
        self.alien_image_timer.next_frame()
        if self.dying and self.alien_image_timer.is_expired():
            self.remove(self.game.aliens.group)

    def check_edges(self):
        return self.rect.left <= 0 or self.rect.right >= self.game.settings.screen_width

    def move_down(self):
        self.y += self.game.settings.alien_fleet_drop_speed
        self.rect.y = self.y

    def die(self):
        self.image_list = self.death_image_list
        self.alien_image_timer = self.alien_death_timer
        self.dying = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def handle_hit_bottom(self):
        hit = self.rect.bottom >= self.game.settings.screen_height
        if hit:
            self.game.gameStats.lost_ship()
            self.game.reset()
        return hit
