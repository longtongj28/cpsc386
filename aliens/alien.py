import random
from time import sleep

import pygame as pg
from pygame.sprite import Sprite as Sp, Group

from timer import Timer
from laser import AlienLaser

class AlienFleet:
    def __init__(self, game):
        self.game = game
        self.group = Group()
        self.alien = Alien(game=self.game, alien_type="alienThree")
        self.space_between_row_ships = 70
        self.total_space_per_fleet = 0
        self.create_all_aliens()
        self.last_ufo_time = pg.time.get_ticks()
        self.last_time_fired = pg.time.get_ticks()
        self.alien_lasers = Group()

    def update(self):
        if len(self.group) == 0:
            self.game.reset()
        self.check_fleet_edge()
        for alien in self.group.sprites():
            alien.update()
        self.random_ufo()
        self.random_laser()
        for laser in self.alien_lasers.sprites():
            laser.update()

    def random_laser(self):
        now = pg.time.get_ticks()
        if now - self.last_time_fired > 5000:
            for alien in self.group.sprites():
                if random.randint(0, 10) == 2:
                    alien.fire_laser()
            self.last_time_fired = now

    def random_ufo(self):
        now = pg.time.get_ticks()
        if now - self.last_ufo_time > 10000 and random.randint(0, 10) == 7:
            self.create_alien_at(0, 30, AlienFour(game=self.game))
            self.last_ufo_time = now

    def check_fleet_edge(self):
        for alien in self.group.sprites():
            if not alien.alien_type == 'alienFour':
                if alien.handle_hit_bottom():
                    break
                if alien.check_edges():
                    self.change_fleet_dir()
                    break

    def change_fleet_dir(self):
        self.game.settings.alien_fleet_direction *= -1
        for alien in self.group.sprites():
            if not alien.alien_type == 'alienFour':
                alien.move_down()

    def respawn(self):
        self.game.lasers.group.empty()
        self.alien_lasers.empty()
        self.group.empty()
        self.create_all_aliens()
        self.game.settings.alien_fleet_direction = 1
        self.draw()

    def draw(self):
        for alien in self.group.sprites():
            alien.draw()
        for laser in self.alien_lasers.sprites():
            laser.draw()

    def create_all_aliens(self):
        alienOne = Alien(game=self.game, alien_type="alienOne")
        alienTwo = Alien(game=self.game, alien_type="alienTwo")
        alienThree = Alien(game=self.game, alien_type="alienThree")
        space = self.space_between_row_ships
        self.total_space_per_fleet = alienOne.rect.height + alienTwo.rect.height + alienThree.rect.height + 2 * space
        self.create_row_aliens(self.total_space_per_fleet, alienOne)
        self.create_row_aliens(self.total_space_per_fleet - space - alienOne.rect.height, alienTwo)
        self.create_row_aliens(self.total_space_per_fleet - 2 * space - alienOne.rect.height - alienTwo.rect.height,
                               alienThree)

    def create_row_aliens(self, y, alien):
        for i in range(self.get_num_aliens_x(self.alien)):
            self.create_alien_at(i, y, alien)

    def create_alien_at(self, x, y, alien):
        space_factor_x = 1.25
        a = self.alien
        alien_width = a.rect.width
        pos_y = y
        pos_x = alien_width + space_factor_x * alien_width * x

        if alien.alien_type == 'alienFour':
            alien = AlienFour(self.game)
        else:
            alien = Alien(self.game, alien_type=alien.alien_type)
        alien.x = pos_x
        alien.y = pos_y
        alien.rect.x = alien.x
        alien.rect.y = alien.y

        self.group.add(alien)

    def get_num_aliens_x(self, alien):
        alien_width = alien.rect.width
        game = self.game
        available_space_x = game.settings.screen_width - 1.5 * alien_width
        num_aliens_x = int(available_space_x / (1.25 * alien_width))
        return num_aliens_x

    def get_num_aliens_y(self, alien):
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
        self.alien_type = alien_type

        self.normal_image_list = [pg.image.load(f'images/{alien_type}/{alien_type}{x}.png') for x in range(2)]
        self.death_image_list = [pg.image.load(f'images/{alien_type}Death/{alien_type}Death{x}.png') for x in range(5)]
        self.image_list = self.normal_image_list
        self.alien_normal_timer = Timer(image_list=self.image_list, delay=self.settings.alien_animation_delay)
        self.alien_death_timer = Timer(image_list=self.death_image_list, delay=self.settings.alien_animation_delay,
                                       is_loop=False)
        self.alien_image_timer = self.alien_normal_timer
        self.image = self.image_list[self.alien_image_timer.index]
        self.last_animation_time = pg.time.get_ticks()
        self.dying = False

        alien_lives = {'alienOne': 2, 'alienTwo': 4, 'alienThree': 6, 'alienFour': 1}
        alien_scores = {'alienOne': 10, 'alienTwo': 20, 'alienThree': 40, 'alienFour': random.randint(30, 100)}
        self.lives = alien_lives[alien_type]
        self.score = alien_scores[alien_type]

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
            self.kill()

    def check_edges(self):
        return self.rect.left < 0 or self.rect.right > self.game.settings.screen_width

    def move_down(self):
        self.y += self.game.settings.alien_fleet_drop_speed
        self.rect.y = self.y

    def die(self):
        self.image_list = self.death_image_list
        self.alien_image_timer = self.alien_death_timer
        self.dying = True
        self.game.sound.play_alien_explosion()

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

    def fire_laser(self):
        x = self.rect.centerx
        y = self.rect.bottom
        laser = AlienLaser(game=self.game, x=x, y=y)
        self.game.aliens.alien_lasers.add(laser)
        self.game.sound.play_fire_phaser()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class AlienFour(Alien):
    def __init__(self, game, alien_type="alienFour"):
        super().__init__(game=game, alien_type=alien_type)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.font = pg.font.SysFont(None, 40)
        self.game.sound.play_ufo()

    def update(self):
        speed = self.game.settings.alien_speed_factor * 2
        self.x += speed
        self.rect.x = self.x
        self.handle_animation()
        if self.pass_right():
            self.kill()

    def handle_animation(self):
        self.image = self.alien_image_timer.image()
        if self.dying:
            self.image = self.font.render(f'+{self.score}', True, WHITE, BLACK)
            if self.alien_image_timer.is_expired():
                self.kill()

    def pass_right(self):
        return self.rect.left > self.game.settings.screen_width
