import pygame as pg


class Settings:
    def __init__(self):
        self.total_lives = 10

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_image = pg.image.load('images/game_bg.jpeg')
        self.ship_speed_factor = 10
        self.ship_fire_delay = 200
        self.ship_image_animation_delay = 200
        self.ship_death_animation_delay = 50
        self.laser_animation_delay = 70
        self.alien_animation_delay = 100

        self.laser_color = (0, 191, 255)
        self.laser_speed_factor = 10
        self.laser_width = 5
        self.laser_height = 20
        self.lasers_allowed = 100

        self.alien_speed_factor = 5
        self.alien_fleet_drop_speed = 10
        self.alien_fleet_direction = 1
