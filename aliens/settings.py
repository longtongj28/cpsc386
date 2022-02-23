class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (50, 50, 50)
        self.ship_speed_factor = 10

        self.laser_color = (200, 8, 8)
        self.laser_speed_factor = 5
        self.laser_width = 5
        self.laser_height = 20
        self.lasers_allowed = 20

        self.alien_speed_factor = 5
        self.alien_fleet_drop_speed = 10
        self.alien_fleet_direction = 1
