import pygame
from pygame import mixer
from pygame.locals import *
import random

pygame.init()

height = 400
width = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hardest Game')

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("SoundTrack/hardestGameThemeSong.mp3")
mixer.music.play(-1)

#Goal
startPlaceX = [100]
endPlaceX = [480]
endPlaceY = [0,20]

clock = pygame.time.Clock()

tamBlocks = 20 #qntd de pixels que os objetos ocupam -- no caso matrix cada elemento da matrix tem 10px

game_over = False

#player
playerStartX = 40
playerStartY = 300

def startPlayerPosition():
    return [playerStartX, playerStartY]

player = startPlayerPosition()
player_skin = pygame.Surface((tamBlocks,tamBlocks))
player_skin.fill((255,0,0))

# Macro definition for player movement.
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
STOP = 4

my_direction = STOP

# Enemy
x_enemyIni = 400
y_enemyIni = 60

distXBetweenEnemies = 0
distYBetweenEnemies = 100

blue_skin = pygame.Surface((tamBlocks,tamBlocks))
blue_skin.fill((0,0,255))

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImg.append(blue_skin)
    enemyX.append(x_enemyIni)
    enemyY.append(y_enemyIni)
    enemyX_change.append(tamBlocks)
    enemyY_change.append(tamBlocks)
    x_enemyIni += distXBetweenEnemies
    y_enemyIni += distYBetweenEnemies


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def collision(player, i):
    return (player[0] == enemyX[i]) and (player[1] == enemyY[i])

def check_end(player):
    return (player[0] > endPlaceX[0]) and (endPlaceY[0] <= player[1] <= endPlaceY[1])

while not game_over:

    clock.tick(10)
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    my_direction = STOP

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                my_direction = UP
            if event.key == K_DOWN:
                my_direction = DOWN
            if event.key == K_LEFT:
                my_direction = LEFT
            if event.key == K_RIGHT:
                my_direction = RIGHT
            #else:
                #my_direction = STOP


    # Enemy Movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= startPlaceX[0]: #limite maximo para os inimigos se movimentarem
            enemyX_change[i] = tamBlocks
            #enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= endPlaceX[0]: #limite maximo para os inimigos se movimentarem
            enemyX_change[i] = -tamBlocks
            #enemyY[i] += enemyY_change[i]

        enemy(enemyX[i], enemyY[i], i)

    # Check if player collided with enemies
    for i in range(num_of_enemies):
        if(collision(player,i)):
            punchSound = mixer.Sound("SoundTrack/punch.wav")
            punchSound.play()
            player = startPlayerPosition()
            break

    playerChangeY = 0
    playerChangeX = 0

    # Actually make the Player move.
    if my_direction == UP and player[1] > 0:
        playerChangeY = -tamBlocks
    if my_direction == DOWN  and player[1] < height - tamBlocks:
        playerChangeY = tamBlocks
    if my_direction == RIGHT and player[0] < width - tamBlocks:
        playerChangeX = tamBlocks
    if my_direction == LEFT and player[0] > 0:
        playerChangeX = -tamBlocks

    player = (player[0] + playerChangeX, player[1] + playerChangeY)
    #Player movement
    screen.blit(player_skin,player)

    #check if is the end point
    if (check_end(player)):
        game_over = True

    pygame.display.update()
