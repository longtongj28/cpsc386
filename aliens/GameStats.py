import pygame as pg


class GameStats:
    def __init__(self, game):
        self.game = game
        self.ships_left = game.settings.total_lives
        self.score = 0
        self.level = 0
        self.reset_stats()
        self.highscore = self.load_high_score()
        print(f"You have {self.ships_left} ships left")

    def __del__(self):
        self.save_high_score()

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        try:
            with open("highscore.txt", "w+") as f:
                f.write(str(round(self.highscore, -1)))  # 314.15 --> 310,  (0) --> 314
        except:
            print("highscore.txt not found...")

    def get_score(self):
        return self.score

    def get_highscore(self):
        return self.highscore

    def get_level(self):
        return self.level

    def get_ships_left(self):
        return self.ships_left

    def reset_stats(self):
        self.ships_left = self.game.settings.total_lives

    def level_up(self):
        self.level += 1
        self.game.settings.alien_speed_factor *=  1.1
        print("leveling up: level is now ", self.level)

    def alien_hit(self, alien):
        self.score += alien.score
        self.highscore = max(self.score, self.highscore)

    def lost_ship(self):
        if self.ships_left > 1:
            print(f'You have {self.ships_left} ships left')
        else:
            print("0 ships left! Game over. Restart to play again!")
        self.ships_left -= 1
