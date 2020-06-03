import pygame
from pygame.locals import *
import random

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Hardest Game')

# Background
background = pygame.image.load('background.png')

startPlaceX = [100]
endPlaceX = [480]
endPlaceY = [0,20]

clock = pygame.time.Clock()

tamBlocks = 20 #qntd de pixels que os objetos ocupam -- no caso matrix cada elemento da matrix tem 10px

#player
player = [300, 300]
player_skin = pygame.Surface((tamBlocks,tamBlocks))
player_skin.fill((255,255,255)) #White

x_enemyIni = 400
y_enemyIni = 60

distXBetweenEnemies = 0
distYBetweenEnemies = 100

blue_skin = pygame.Surface((tamBlocks,tamBlocks))
blue_skin.fill((0,0,255)) #White

game_over = False

# Enemy
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
    #screen.blit(startPlace_skin,startPlace)
    #screen.blit(endPlace_skin, endPlace)


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if event.type == KEYDOWN:
        if event.key == K_UP:
            player = (player[0], player[1] - tamBlocks)
        if event.key == K_DOWN:
            player = (player[0], player[1] + tamBlocks)
        if event.key == K_LEFT:
            player = (player[0] - tamBlocks, player[1])
        if event.key == K_RIGHT:
            player = (player[0] + tamBlocks, player[1])

    #limite maximo para os inimigos se movimentarem
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

    for i in range(num_of_enemies):
        if(collision(player,i)):
            game_over = True
            break

    screen.blit(player_skin,player)

    if (check_end(player)):
        game_over = True
    print(player[0], " ",  endPlaceX[0], " ", endPlaceY[0], " ", player[1], " ", endPlaceY[1])
    pygame.display.update()
