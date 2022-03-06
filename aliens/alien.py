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
            for j in range(6):
                self.create_alien_at(i, j)

    def create_alien_at(self, x, y):
        alien_width = self.alien.rect.width
        alien_height = self.alien.rect.height


        alien_type = "alienOne"
        pos_x = 0
        pox_y = 0
        if y % 3 == 0:
            alien_type = "alienThree"
            pos_x = alien_width + 2 * alien_width * x
            pos_y = alien_height + 2 * alien_height * y
        elif y % 3 == 1:
            alien_type = "alienTwo"
            pos_x = alien_width + 2 * alien_width * x
            pos_y = alien_height + 2 * alien_height * y
        elif y % 3 == 2:
            alien_type = "alienOne"
            pos_x = alien_width + 2 * alien_width * x
            pos_y = alien_height + 2 * alien_height * y

        alien = Alien(self.game, alien_type=alien_type)

        alien.x = pos_x
        alien.y = pos_y
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

        alien_lives = {'alienOne': 2, 'alienTwo': 4, 'alienThree': 6, 'alienFour': 1}
        self.lives = alien_lives[alien_type]

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

    def change_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def handle_animation(self):
        self.image = self.alien_image_timer.image()
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

    def lose_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.die()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def handle_hit_bottom(self):
        hit = self.rect.bottom >= self.game.settings.screen_height
        if hit:
            self.game.gameStats.lost_ship()
            self.game.reset()
        return hit
