import pygame
from pygame import mixer
from pygame.locals import *
import random
import background as bg

pygame.init()

height = 400
width = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hardest Game')

blocks_size = 30 #qntd de pixels que os objetos ocupam -- no caso matrix cada elemento da matrix tem 10px
tam_player = blocks_size-10
num_of_enemies = 4

# Background
background = bg.get_background(blocks_size, num_of_enemies*blocks_size, width, height)

# Sound
mixer.music.load("SoundTrack/hardestGameThemeSong.mp3")
mixer.music.play(-1)

clock = pygame.time.Clock()

game_over = False

player_skin = pygame.Surface((tam_player,tam_player))
player_skin.fill((255,0,0))

# Macro definition for player movement.
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
STOP = 4

my_direction = STOP

enemies_direction = []

font = pygame.font.Font('freesansbold.ttf', 18)
score = 0

def make_enemy_skin():
	blue_skin = pygame.Surface([tam_player,tam_player])
	blue_skin.fill((0,0,0))
	blue_skin.set_colorkey((0,0,0))
	pygame.draw.ellipse(blue_skin, (0,0,255),(0, 0, tam_player-2, tam_player-2), 0)
	return blue_skin

def make_enemies():
	enemies = []
	enemies_rect = []
	y_enemy_init = (height - (num_of_enemies*blocks_size))/2
	y = y_enemy_init+blocks_size/2
	for i in range(num_of_enemies):
		enemy = make_enemy_skin()
		rect = enemy.get_rect()
		if not i%2:	
			rect.left = background.play_area.left
			enemies_direction.append(1)
		else:
			rect.right = background.play_area.right
			enemies_direction.append(-1)	
		rect.centery = y	
		enemies.append(enemy)
		enemies_rect.append(rect)
		y += blocks_size
	return enemies, enemies_rect
	
def move_enemy(i):
	enemies_rect[i].centerx = enemies_rect[i].centerx + (tam_player)*enemies_direction[i]
	if (enemies_rect[i].right >= background.play_area.right):
		enemies_direction[i] = -1
	elif (enemies_rect[i].left <= background.play_area.left):
		enemies_direction[i] = 1
	enemy(i)

def enemy(i):
	screen.blit(enemies[i], enemies_rect[i])

def collision(player, i):
	return enemies_rect[i].colliderect(player)

def check_end():
	return background.check_final(player_rect)

def show_score():
	score_font = font.render('Deaths: %s' % (score), True, (255, 255, 255))
	score_rect = score_font.get_rect()
	score_rect.topleft = (600 - 120, 10)
	screen.blit(score_font, score_rect)

def startPlayerPosition():
	player_rect.x = background.init_area.centerx
	player_rect.y = background.init_area.centery
	return [player_rect.x, player_rect.y]

enemies, enemies_rect = make_enemies()
player_rect = player_skin.get_rect()
player = startPlayerPosition()

while not game_over:

	clock.tick(10)
	background.draw_background(screen)
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
		move_enemy(i)

	# Check if player collided with enemies
	for i in range(num_of_enemies):
		if(collision(player_rect, i)):
			punchSound = mixer.Sound("SoundTrack/punch.wav")
			punchSound.play()
			score += 1 #number of deaths
			player = startPlayerPosition()
			break

	playerChangeY = 0
	playerChangeX = 0

	test_move_rec = player_rect.copy()

	move = tam_player

	while move: #get max move possible
		if my_direction == UP:
			test_move_rec.top = test_move_rec.top - move
		if my_direction == DOWN:
			test_move_rec.bottom = test_move_rec.bottom + move
		if my_direction == LEFT:
			test_move_rec.left = test_move_rec.left - move
		if my_direction == RIGHT:
			test_move_rec.right = test_move_rec.right + move

		if background.check_borders(test_move_rec):
			player_rect = test_move_rec.copy()
			break
		else:
			move -= 5
			test_move_rec = player_rect.copy()

	screen.blit(player_skin, player_rect)

	show_score()
	#check if is the end point
	if (check_end()):
		game_over = True

	pygame.display.update()
