import pygame as pg


# Referenced from Professor McCarthy's Timer class source code
class Timer:
    def __init__(self, image_list, start_index=0, delay=100, is_loop=True):
        self.image_list = image_list
        self.delay = delay
        self.is_loop = is_loop
        self.last_time_switched = pg.time.get_ticks()
        self.frames = len(image_list)
        self.start_index = start_index
        self.index = start_index if start_index < len(image_list) - 1 else 0

    def next_frame(self):
        # if a one-pass timer that has finished      # <-- SANITY check to see if it's an expired one-time pass timer
        if not self.is_loop and self.index == len(self.image_list):
            return
        now = pg.time.get_ticks()
        if now - self.last_time_switched >= self.delay:
            self.index += 1
            if self.is_loop:
                self.index %= self.frames
            self.last_time_switched = now

    def is_expired(self):  # <-- MODIFIED is_expired to work better with next_frame
        return not self.is_loop and self.index == len(self.image_list )

    def reset(self):
        self.index = self.start_index  # <--- ADDED new reset() method, e.g., Ship will reset its explosion timer
# each time the game is restarted
