import pygame as pg


class GameStats:
    def __init__(self, game):
        self.game = game
        self.ships_left = game.settings.total_lives
        print(f"You have {self.ships_left} ships left")

    def lost_ship(self):
        if self.ships_left > 1:
            self.ships_left -= 1
            print(f'You have {self.ships_left} ships left')
        else:
            self.game.active = False
            print("0 ships left! Game over. Restart to play again!")
