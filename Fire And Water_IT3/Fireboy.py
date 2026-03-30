import pygame
from settings import *
import os

class Fireboy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.idle_path = FIREBOY_IDLE_IMAGE_PATH
        self.right_path = FIREBOY_RIGHT_IMAGE_PATH
        self.animations = {}
        self.load_animation_frames()
        self.current_animation = 'idle'
        self.animation_index = 0
        self.image = self.animations[self.current_animation][self.animation_index]
        self.rect = self.image.get_rect(bottomleft=(x, y))

        # pohyb
        self.vel_x = 0
        self.velocity_y = 0
        self.speed = 5

        # fyzika
        self.gravity = 0.5
        self.jump_strength = -12
        self.on_ground = False

    def load_animation_frames(self):
        idle_animations = []
        left_animations = []
        right_animations = []

        cesta = os.path.dirname(self.idle_path)
        pocet = sum(1 for f in os.scandir(cesta) if f.is_file() and f.name.endswith(".png"))

        for i in range(1, pocet):
            img = pygame.image.load(self.idle.format(i))
            img = pygame.transform.scale(
                img,
                (img.get_width() * FIREBOY_SCALE, img.get_height() * FIREBOY_SCALE)
            )
            idle_animations.append(img)

        cesta = os.path.dirname(self.idle_path)
        pocet = sum(1 for f in os.scandir(cesta) if f.is_file() and f.name.endswith(".png"))

        right_animations = [
            pygame.image.load(self.idle_path.format(i))
            for i in range(1, pocet)
        ]
        right_animations = [
            pygame.transform.scale(
                img,
                (img.get_width() * FIREBOY_SCALE, img.get_height() * FIREBOY_SCALE)
            )
            for img in right_animations
        ]

        left_animations = [pygame.transform.flip(img, True, False) for img in right_animations]

        self.animations = {
            'idle': idle_animations,
            'right': right_animations,
            'left': left_animations
        }

    def check_collision(self, level):
        self.on_ground = False

        self.rect.x += self.vel_x
        for row in range(len(level.level_data)):
            for col in range(len(level.level_data[row])):
                tile = level.level_data[row][col]

                if tile == 1:  # zem
                    tile_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    if self.rect.colliderect(tile_rect):
                        if self.vel_x > 0:
                            self.rect.right = tile_rect.left
                        if self.vel_x < 0:
                            self.rect.left = tile_rect.right

        self.rect.y += self.velocity_y
        for row in range(len(level.level_data)):
            for col in range(len(level.level_data[row])):
                tile = level.level_data[row][col]

                tile_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                if tile == 1:  # zem
                    if self.rect.colliderect(tile_rect):
                        if self.velocity_y > 0:  # padá
                            self.rect.bottom = tile_rect.top
                            self.velocity_y = 0
                            self.on_ground = True
                        elif self.velocity_y < 0:  # skok
                            self.rect.top = tile_rect.bottom
                            self.velocity_y = 0

                if tile == 2:  # láva
                    if self.rect.colliderect(tile_rect):
                        print("Fireboy umřel v lávě :(")
                        # reset (můžeš upravit)
                        self.rect.topleft = (100, 100)
                        self.velocity_y = 0

    
    def _movement(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        # pohyb
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
            self.current_animation = 'left'
        elif keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
            self.current_animation = 'right'
        else:
            self.current_animation = 'idle'

        # skok
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_strength
    
    
    
    
    
    
    def update(self, level):
        self._movement()
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        # pohyb
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
            self.current_animation = 'left'
        elif keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
            self.current_animation = 'right'
        else:
            self.current_animation = 'idle'

        # skok
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_strength

        # gravitace
        self.velocity_y += self.gravity
        if self.velocity_y > 10:
            self.velocity_y = 10

        # kolize místo přímého pohybu
        self.check_collision(level)

        # animace
        self.animation_index += 0.1
        if self.animation_index >= len(self.animations[self.current_animation]):
            self.animation_index = 0

        self.image = self.animations[self.current_animation][int(self.animation_index)]


if __name__ == "__main__":
    import main