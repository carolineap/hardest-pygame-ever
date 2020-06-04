import pygame
from pygame.locals import *
import random

GREEN = (51, 255, 206)
GREY = (198, 198, 198)
BG_COLOR = (138, 150, 255)
SCREEN_SIZE_X = 600
SCREEN_SIZE_Y = 400

pygame.init()

screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
pygame.display.set_caption('Hardest Game')

startPlaceX = [100]
endPlaceX = [480]
endPlaceY = [0,20]

font = pygame.font.Font('freesansbold.ttf', 18)


clock = pygame.time.Clock()

tamBlocks = 30 #qntd de pixels que os objetos ocupam -- no caso matrix cada elemento da matrix tem 10px

#player

tam_player = tamBlocks-10

player_skin = pygame.Surface((tam_player,tam_player))
player_skin.fill((255,255,255)) #White


game_over = False

# Enemy
enemiesImg = []
enemies = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []	
num_of_enemies = 4

distXBetweenEnemies = 0
distYBetweenEnemies = tamBlocks

enemiesAreaY = (num_of_enemies*tamBlocks)

x_enemyIni = SCREEN_SIZE_X - 200
y_enemyIni = (SCREEN_SIZE_Y - enemiesAreaY)/2

play_image = pygame.Surface([(tamBlocks*10), enemiesAreaY])
play_image.fill(GREY)
play_area = play_image.get_rect()
play_area.centerx = SCREEN_SIZE_X/2
play_area.centery = SCREEN_SIZE_Y/2

play_small_image = pygame.Surface([(tamBlocks*2), tamBlocks])
play_small_image.fill(GREY)

play_area_init = play_small_image.get_rect()
play_area_init.center = (play_area.left, play_area.bottom+tamBlocks/2)

play_area_end = play_small_image.get_rect()
play_area_end.center = (play_area.right, play_area.top-tamBlocks/2)

small_image = pygame.Surface([3*tamBlocks, (tamBlocks*2)+enemiesAreaY])
small_image.fill(GREEN)

#Start area
init_area = small_image.get_rect()
init_area.right = play_area_init.left
init_area.centery = SCREEN_SIZE_Y/2

#Finish area
end_area = small_image.get_rect()
end_area.left = play_area_end.right
end_area.centery = SCREEN_SIZE_Y/2


y = y_enemyIni+tamBlocks/2
for i in range(num_of_enemies):
	blue_skin = pygame.Surface([tam_player,tam_player])
	blue_skin.fill((0,0,0))
	blue_skin.set_colorkey((0,0,0))
	pygame.draw.ellipse(blue_skin, (0,0,255),(0, 0, tam_player, tam_player), 0)
	area = blue_skin.get_rect()
	if not i%2:	
		area.left = play_area.left
		enemyX_change.append(1)
	else:
		area.right = play_area.right
		enemyX_change.append(-1)
	area.centery = y
	enemies.append(blue_skin)
	enemiesImg.append(area)
	
	y += distYBetweenEnemies


def check_borders(x, y):
	#return init_area.contains(p) or play_area_init.contains(p) or play_area_end.contains(p) or play_area.contains(p) or end_area.contains(p)
	if x <= play_area.right and x >= play_area.left and y >= play_area.top and y <= play_area.bottom:
		return True
	if x <= init_area.right and x >= init_area.left and y >= init_area.top and y <= init_area.bottom:
		return True
	if x <= end_area.right and x>= end_area.left and y >= end_area.top and y <= end_area.bottom:
		return True
	if x <= play_area_init.right and x >=play_area_init.left and y >= play_area_init.top and y <= play_area_init.bottom:
		return True
	if x <= play_area_end.right and x >=play_area_end.left and y >= play_area_end.top and y <= play_area_end.bottom:
		return True


def draw_background():
	screen.fill((BG_COLOR))
	screen.blit(play_image, play_area)
	screen.blit(play_small_image, play_area_init)
	screen.blit(play_small_image, play_area_end)
	screen.blit(small_image, init_area)
	screen.blit(small_image, end_area)

def enemy(i):
	#print(enemies[i].get_rect().centery)
	screen.blit(enemies[i], enemiesImg[i])

def collision(player, i):
	print(enemiesImg[i])
	return enemiesImg[i].colliderect(player)

def check_end(player):
	return (player[0] > endPlaceX[0]) and (endPlaceY[0] <= player[1] <= endPlaceY[1])

def move_enemy(i):
	enemiesImg[i].centerx = enemiesImg[i].centerx + (tam_player)*enemyX_change[i]
	if (enemiesImg[i].right >= play_area.right):
		enemyX_change[i] = -1
	elif (enemiesImg[i].left <= play_area.left):
		enemyX_change[i] = 1
	enemy(i)

deaths = 0

a = player_skin.get_rect()
a.x = init_area.centerx
a.y = init_area.centery
player = [a.x, a.y]



while True:
	clock.tick(10)


	draw_background()

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()

	old = player

	if event.type == KEYDOWN:
		if event.key == K_UP:
			player = (player[0], player[1] - tam_player)
		if event.key == K_DOWN:
			player = (player[0], player[1] + tam_player)
		if event.key == K_LEFT:
			player = (player[0] - tam_player, player[1])
		if event.key == K_RIGHT:
			player = (player[0] + tam_player, player[1])


	a.x = player[0]
	a.y = player[1]
	
	if not check_borders(a.x, a.y):
		a.x = old[0]
		a.y = old[1]
		player = old

	#limite maximo para os inimigos se movimentarem
	# Enemy Movement
	for i in range(num_of_enemies):
		# enemyX[i] += enemyX_change[i]
		# if enemyX[i] <= startPlaceX[0]: #limite maximo para os inimigos se movimentarem
		#     enemyX_change[i] = tamBlocks
		#     #enemyY[i] += enemyY_change[i]
		#     enemyImg[i].get_rect
		# elif enemyX[i] >= endPlaceX[0]: #limite maximo para os inimigos se movimentarem
		#     enemyX_change[i] = -tamBlocks
		#     #enemyY[i] += enemyY_change[i]

		#enemy(enemyX[i], enemyY[i], i)
		move_enemy(i)


	for i in range(num_of_enemies):
		if(collision(a, i)):
			deaths+=1
			a.x = init_area.centerx
			a.y = init_area.centery
			player = [a.x, a.y]


	score_font = font.render('Deaths: %s' % (deaths), True, (255, 255, 255))
	score_rect = score_font.get_rect()
	score_rect.topleft = (600 - 120, 10)
	screen.blit(score_font, score_rect)
			
	screen.blit(player_skin,player)

	if (check_end(player)):
		game_over = True
	#print(player[0], " ",  endPlaceX[0], " ", endPlaceY[0], " ", player[1], " ", endPlaceY[1])
	pygame.display.update()