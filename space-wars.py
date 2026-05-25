import pygame
import random
import math
from spaceship import Spaceship
from bullet import Bullet
from enemy import Enemy
FPS = 120
CLOCK = pygame.time.Clock()
pygame.init()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

SCREEN_X = 800
SCREEN_Y = 600

SURFACE = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.RESIZABLE)
pygame.display.set_caption("Primeiro Jogo")

x = 0
y = 0

SPEED = 1
WIDHT = 50

dtX = SPEED
dtY = SPEED

COR = (0,0,0)
BLACK = (0,0,0)

MENU = 'menu'
GAME = 'game'
GAME_OVER = 'game_over'

actual_state = MENU


bg_image = pygame.image.load("space.jpg").convert()
scroll_x = 0
scroll_y = 0


text_font = pygame.font.Font('font/starjedi/Starjedi.ttf', 40)
text_color = 'yellow'

paragraph_font = pygame.font.Font('font/starjedi/Starjedi.ttf', 20)

SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 3000)

score = 0
score_surf = text_font.render(f'Score: {score}', False, text_color)
score_rect = score_surf.get_rect(center = (150,  50))

menu_surf = text_font.render('star wars v', False, text_color)
menu_rect = menu_surf.get_rect(center = (0, 0))

gameover_surf = text_font.render('WASTED', False, text_color)
gameover_rect = gameover_surf.get_rect(center = (0, 0))

pygame.mixer.init()
shoot_song = pygame.mixer.Sound('droid-blaster.mp3')
shoot_song.set_volume(0.4)


all_sprites = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
enemy_bullets_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
spaceship = Spaceship()
all_sprites.add(spaceship)

def random_pos():
    return (random.randint(0,SCREEN_X),random.randint(0,SCREEN_Y))

def spawn_enemies():
    border = random.randint(0, 3)

    if border == 0: x, y = random.randint(0, SCREEN_X), -50
    elif border == 1: x, y = random.randint(0, SCREEN_X), SCREEN_Y + 50
    elif border == 2: x, y = -50, random.randint(0, SCREEN_Y)
    else: x, y = SCREEN_X + 50, random.randint(0, SCREEN_Y)

    new_enemy = Enemy(spaceship, enemy_bullets_group, shoot_song)
    new_enemy.pos = pygame.Vector2(x, y)
    new_enemy.rect.center = new_enemy.pos

    enemies_group.add(new_enemy)

while True:
    SCREEN_X, SCREEN_Y = pygame.display.get_surface().get_size()
    
    bg_image = pygame.transform.scale(bg_image, (SCREEN_X, SCREEN_Y))
    bg_image2 = pygame.transform.scale(bg_image, (SCREEN_X, SCREEN_Y))

    life_surf = text_font.render(f'Life: {spaceship.life}', False, text_color)
    life_rect = life_surf.get_rect(center = (120,  100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        
        if actual_state == MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not spaceship.alive(): all_sprites.add(spaceship) # reset player when inicialize
                actual_state = GAME
        elif actual_state == GAME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                new_shoot = Bullet(spaceship.rect.centerx, spaceship.rect.centery, spaceship.angle) 
                bullets_group.add(new_shoot)
                print('atirou')

                shoot_song.play()

                #recoil
                force_recoil = 1
                rad = math.radians(spaceship.angle)
                spaceship.vel.x -= math.cos(rad) * force_recoil
                spaceship.vel.y += math.sin(rad) * force_recoil
            
            if event.type == SPAWN_ENEMY:
                spawn_enemies()
                print('novo inimigo')
        elif actual_state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                spaceship = Spaceship()
                all_sprites.empty()
                all_sprites.add(spaceship)
                enemies_group.empty()
                bullets_group.empty()
                enemy_bullets_group.empty()
                score = 0
                score_surf = text_font.render(f'Score: {score}', False, text_color)
                actual_state = MENU

        
    if actual_state == GAME:
        bullets_group.update()
        enemy_bullets_group.update()
        all_sprites.update()
        enemies_group.update()

        if hits_player:
            spaceship.life -= len(hits_player)
            print('perdeuy vida')
        
            life_surf = text_font.render(f'Life: {spaceship.life}', False, text_color)

        if hits:
            for enemy_hited, bullets in hits.items():
                enemy_hited.life -= len(bullets)
                if enemy_hited.life == 0:
                    score += len(bullets)
                print('veio auqi')
                
                score_surf = text_font.render(f'Score: {score}', False, text_color)

            if spaceship.life <= 0:
                actual_state = GAME_OVER

    SURFACE.fill(WHITE) # BACKGROUND
    SURFACE.blit(bg_image, (scroll_x, scroll_y))
    SURFACE.blit(bg_image2, (scroll_x, scroll_y + SCREEN_Y -2))
    scroll_y -= 1

    if actual_state == GAME:
        enemies_group.draw(SURFACE)
        all_sprites.draw(SURFACE)
        bullets_group.draw(SURFACE)
        enemy_bullets_group.draw(SURFACE)

        SURFACE.blit(score_surf, score_rect)
        SURFACE.blit(life_surf, life_rect)

        if spaceship.life <= 0:
            actual_state = GAME_OVER
    elif actual_state == MENU:
        SURFACE.blit(menu_surf, (SCREEN_X//2 - menu_rect.width//2, SCREEN_Y//2))
        instruction = paragraph_font.render('Pressione ESPAÇ0 para iniciar', False, WHITE)
        SURFACE.blit(instruction, (SCREEN_X//2 - instruction.get_width()//2, SCREEN_Y//2 + 60))
    elif actual_state == GAME_OVER:
        SURFACE.blit(gameover_surf, (SCREEN_X//2 - gameover_rect.width, SCREEN_Y//2))
    

    if scroll_y <= -SCREEN_Y: # if the scroll_Y is less than screen_Y, return to the initial position
        scroll_y = 0

    # check if any bullet of the group hited any enemy of the group
    hits = pygame.sprite.groupcollide(enemies_group, bullets_group, False, True)

    hits_player = pygame.sprite.spritecollide(spaceship, enemy_bullets_group, True)

    


    
    
    
    pygame.display.update()
    CLOCK.tick(FPS)
