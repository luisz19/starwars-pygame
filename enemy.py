import pygame
import math
import random
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):

    def __init__(self, target, enemy_bullets_group, shoot_song):
        super().__init__()

        self.target = target
        self.enemy_bullets_group = enemy_bullets_group
        self.shoot_song = shoot_song
        
        self.image_orig = pygame.image.load('destroyer.png').convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (80, 100))

        screen = pygame.display.get_surface()
        screen_x, screen_y = screen.get_size()

        self.image = self.image_orig
        self.rect = self.image.get_rect(center=(screen_x // 2, screen_y // 2))

        self.last_shoot = pygame.time.get_ticks()
        self.shoot_interval = random.randint(500 ,2000)

        self.angle = 0

        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 0.6
        self.life = 1

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_interval:
            self.last_shoot = now
            new_shoot = Bullet(self.rect.centerx, self.rect.centery, self.angle)
            self.enemy_bullets_group.add(new_shoot)

            self.shoot_song.play()
    
    def update(self):

        # get the player direction
        direction = pygame.Vector2(self.target.rect.center) - self.pos

        if direction.length() > 0:
            direction = direction.normalize()
            self.pos += direction * self.speed
            
        self.rect.center = self.pos

        delta_x = self.target.rect.centerx - self.pos.x
        delta_y = self.target.rect.centery - self.pos.y

        rad = math.atan2(-delta_y, delta_x)
        self.angle = math.degrees(rad)

        self.image = pygame.transform.rotozoom(self.image_orig, self.angle - 90, 1)

        self.rect = self.image.get_rect(center=self.pos)

        if self.life <= 0:
            self.kill()
            print('morreu')

        self.shoot()
