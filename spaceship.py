import pygame
import math

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image_orig = pygame.image.load('falcon.png').convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (80, 100))

        screen = pygame.display.get_surface()
        screen_x, screen_y = screen.get_size()
        
        self.image = self.image_orig
        self.rect = self.image.get_rect(center=(screen_x // 2, screen_y // 2))

        self.pos = pygame.Vector2(self.rect.center)
        self.vel = pygame.Vector2(0, 0)
        self.aceleration = 0.4
        self.friction = 0.96
        self.angle = 0
        self.life = 10
        

    def update(self):
        screen = pygame.display.get_surface()
        screen_x, screen_y = screen.get_size()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.vel.y -= self.aceleration
        if keys[pygame.K_s]: self.vel.y += self.aceleration
        if keys[pygame.K_a]: self.vel.x -= self.aceleration
        if keys[pygame.K_d]: self.vel.x += self.aceleration

        self.vel *= self.friction
        self.pos += self.vel
        self.rect.center = self.pos

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = math.degrees(math.atan2(-rel_y, rel_x)) # math.atan is the angle in radians. -rel_y (axis y inversion)

        self.image = pygame.transform.rotozoom(self.image_orig, self.angle - 90, 1)
        self.rect = self.image.get_rect(center=self.pos)

        # without borders
        if self.rect.left > screen_x: self.pos.x = 0
        elif self.rect.right < 0: self.pos.x = screen_x
        if self.rect.top > screen_y: self.pos.y = 0
        elif self.rect.bottom < 0: self.pos.y = screen_y

        if self.life <= 0:
            self.kill()
            print('morrido')
