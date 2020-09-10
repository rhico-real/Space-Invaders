import pygame
import math
import random
import os

from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
image = "C:/Users/Admin/Desktop/Space Invaders/background.png"
background = pygame.image.load(os.path.join(image), 'background.png')

# Background Sound
music = "C:/Users/Admin/Desktop/Space Invaders/bg_music.wav"
mixer.music.load(music)
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
alien = "C:/Users/Admin/Desktop/Space Invaders/alien.png"
icon = pygame.image.load(os.path.join(alien), 'alien.png')
pygame.display.set_icon(icon)

# Player
player = "C:/Users/Admin/Desktop/Space Invaders/player.png"
playerImg = pygame.image.load(os.path.join(player), 'player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemy = "C:/Users/Admin/Desktop/Space Invaders/enemy.png"
    enemyImg.append(pygame.image.load(os.path.join(enemy), 'enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(30)

# Bullet
# ready - you can't see the bullet on the screen
# fire - the bullet is currently moving
bullet = "C:/Users/Admin/Desktop/Space Invaders/bullet.png"
bulletImg = pygame.image.load(os.path.join(bullet), 'bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop

moveLeft = False
moveRight = False

running = True
while running:

    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (5, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
            if event.key == pygame.K_RIGHT:
                moveRight = True
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    laser = "C:/Users/Admin/Desktop/Space Invaders/laser.wav"
                    bullet_sound = mixer.Sound(laser)
                    bullet_sound.play()

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
            if event.key == pygame.K_RIGHT:
                moveRight = False

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if moveLeft:
        playerX -= 5

    if moveRight:
        playerX += 5

    # enemy movement
    for i in range(num_enemies):

        #Game Over
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over_text()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    break
                else:
                    continue

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion = "C:/Users/Admin/Desktop/Space Invaders/explosion.wav"
            explosion_sound = mixer.Sound(explosion)
            explosion_sound.play()

            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
