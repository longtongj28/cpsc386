import pygame as pg


class Sound:
    def __init__(self):
        pg.mixer.init()
        self.alien_phaser = pg.mixer.Sound('sounds/alien_laser.wav')
        self.ship_photon = pg.mixer.Sound('sounds/ship_laser.mp3')
        self.alien_explosion = pg.mixer.Sound('sounds/alien_death.wav')
        self.ship_explosion = pg.mixer.Sound('sounds/ship_death.mp3')
        self.end_theme = pg.mixer.Sound('sounds/theme_song_2.mp3')
        self.ufo = pg.mixer.Sound('sounds/alien_four_sound.wav')

    def play_music(self, music, volume=0.3):
        pg.mixer.music.unload()            # stop previous music playing before beginning another
        pg.mixer.music.load(music)
        pg.mixer.music.set_volume(volume)
        pg.mixer.music.play(-1, 0.0)

    def busy(self): return pg.mixer.get_busy()
    def play_sound(self, sound): pg.mixer.Sound.play(sound)

    def play_bg(self): self.play_music('sounds/theme_song_2.mp3')
    def play_bg_2(self): self.play_music('sounds/theme_song_1.mp3')
    def play_game_over(self):
        self.stop_bg()     # no more background music
        self.play_sound(self.end_theme)
        while self.busy():    # stays here until end_theme finishes playing
            pass

    def stop_bg(self): pg.mixer.music.stop()

    def play_ufo(self): self.play_sound(self.ufo)
    def stop_ufo(self): pg.mixer.Sound.set_volume(0)
    def play_fire_phaser(self): self.play_sound(self.alien_phaser)
    def play_fire_photon(self): self.play_sound(self.ship_photon)
    def play_alien_explosion(self): self.play_sound(self.alien_explosion)
    def play_ship_explosion(self):
        pg.mixer.stop()
        self.play_sound(self.ship_explosion)


