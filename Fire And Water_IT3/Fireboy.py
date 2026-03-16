import pygame
from settings import *
import os

class Fireboy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animations = {}
        self.load_animation_frames()
        self.current_animation = 'idle'
        self.animation_index = 0
        self.image = self.animations[self.current_animation][self.animation_index]
        self.rect = self.image.get_rect(bottomleft=(x, y))

        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_strength = -12
        self.on_ground = True
        self.ground_y = y #výška země

    def load_animation_frames(self):
        idle_animations = []
        left_animations = []
        right_animations = []

        cesta = os.path.dirname(FIREBOY_IDLE_IMAGE_PATH)
        pocet = sum(1 for f in os.scandir(cesta) if f.is_file() and f.name.endswith(".png"))

        for i in range(1, pocet):
            img = pygame.image.load(FIREBOY_IDLE_IMAGE_PATH.format(i))
            img = pygame.transform.scale(img, (img.get_width() * FIREBOY_SCALE, img.get_height() * FIREBOY_SCALE))
            idle_animations.append(img)

        cesta = os.path.dirname(FIREBOY_RIGHT_IMAGE_PATH)
        pocet = sum(1 for f in os.scandir(cesta) if f.is_file() and f.name.endswith(".png"))

        right_animations = [pygame.image.load(FIREBOY_RIGHT_IMAGE_PATH.format(i)) for i in range(1, pocet)]
        right_animations = [pygame.transform.scale(img, (img.get_width() * FIREBOY_SCALE, img.get_height() * FIREBOY_SCALE)) for img in right_animations]

        left_animations = [pygame.transform.flip(img, True, False) for img in right_animations]

        self.animations = {
            'idle': idle_animations,
            'right': right_animations,
            'left': left_animations
        }

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.current_animation = 'left'
            self.rect.x -= 5
        elif keys[pygame.K_RIGHT]:
            self.current_animation = 'right'
            self.rect.x += 5
        else:
            self.current_animation = 'idle'

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.velocity_y = 0
            self.on_ground = True


        self.animation_index += 0.1
        if self.animation_index >= len(self.animations[self.current_animation]):
            self.animation_index = 0

        self.image = self.animations[self.current_animation][int(self.animation_index)]


if __name__ == "__main__":
    import main