from Fireboy import Fireboy
import os
from settings import *

class WaterGirl(Fireboy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.idle_path = WATERGIRL_IDLE_IMAGE_PATH
        self.right_path = WATERGIRL_RIGHT_IMAGE_PATH
        self.load_animation_frames()

    def _movement(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        # pohyb
        if keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.current_animation = 'left'
        elif keys[pygame.K_d]:
            self.vel_x = self.speed
            self.current_animation = 'right'
        else:
            self.current_animation = 'idle'

        # skok
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_strength
