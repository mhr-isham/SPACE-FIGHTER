#imports
import math
import random
import pygame
from pygame import mixer


# initialize the pygame
pygame.init()

# create the screen 
screen = pygame.display.set_mode((800, 600))

#background
background = pygame.image.load('background.png')

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("SPACE FIGHTER")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy range
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png')) 
    enemyX.append(random.randint(0,730))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
#Ready - you can't see the bullet
#Fire - The bullet is currently moving
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('Open 24 Display St.ttf', 32)

textX = 10
textY = 10

#GAME OVER TEXT
game_over_font_customize = pygame.font.Font('Minecrafter.ttf', 64)

def show_score(x,y):
    score = font.render("Score: " + str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    game_over_font = game_over_font_customize.render("GAME OVER",True,(255,255,255))
    screen.blit(game_over_font, (200,250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

#collision check
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB
    screen.fill((32, 181, 214))
    #background Image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # keystroke press detection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

#checking boundaries of enemy

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    #enemy movement
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 470:
            if enemyX[i] > 370:
                mixer.music.stop()
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] +=enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] +=enemyY_change[i]
        #collision
        collision = iscollision(enemyX[i], enemyY[i],bulletX,bulletY)
        if collision:
            enemy_kill_Sound = mixer.Sound("explosion.wav")
            enemy_kill_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,730)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
