import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()

        self.image_orig = pygame.image.load('laser.png').convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (50, 60))

        self.image = pygame.transform.rotate(self.image_orig, angle - 90)
        self.rect = self.image.get_rect(center = (x, y))

        self.pos = pygame.Vector2(x, y)
        self.speed = 10

        # calculate the direction of the movement based on angle
        rad = math.radians(angle)
        self.vel = pygame.Vector2(math.cos(rad) * self.speed, -math.sin(rad) * self.speed)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos

        screen = pygame.display.get_surface()
        if not screen.get_rect().collidepoint(self.pos):
            self.kill()
