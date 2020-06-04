import pygame
from pygame.locals import *

GREEN = (51, 255, 206)
GREY = (198, 198, 198)
BG_COLOR = (138, 150, 255)

class BackgroundPhaseOne():

	def __init__(self, blocks_size, enemies_area_y, screen_size_x, screen_size_y):
		self.play_image = pygame.Surface([(blocks_size*10), enemies_area_y])
		self.play_image.fill(GREY)
		self.play_area = self.play_image.get_rect()
		self.play_area.center = (screen_size_x/2, screen_size_y/2)

		self.play_small_image = pygame.Surface([(blocks_size*2), blocks_size])
		self.play_small_image.fill(GREY)

		self.play_area_init = self.play_small_image.get_rect()
		self.play_area_init.center = (self.play_area.left, self.play_area.bottom+blocks_size/2)

		self.play_area_end = self.play_small_image.get_rect()
		self.play_area_end.center = (self.play_area.right, self.play_area.top-blocks_size/2)

		self.small_image = pygame.Surface([3*blocks_size, (blocks_size*2)+enemies_area_y])
		self.small_image.fill(GREEN)

		#Start area
		self.init_area = self.small_image.get_rect()
		self.init_area.right = self.play_area_init.left
		self.init_area.centery = screen_size_y/2

		#Finish area
		self.end_area = self.small_image.get_rect()
		self.end_area.left = self.play_area_end.right
		self.end_area.centery = screen_size_y/2

	def check_borders(self, player_rect):
		return 	self.play_area.contains(player_rect) or self.play_area_init.contains(player_rect) or self.play_area_end.contains(player_rect) or self.init_area.contains(player_rect) or self.end_area.contains(player_rect)

	def check_final(self, player_rect):
		return self.end_area.contains(player_rect)

	def draw_background(self, screen):
		screen.fill((BG_COLOR))
		screen.blit(self.play_image, self.play_area)
		screen.blit(self.play_small_image, self.play_area_init)
		screen.blit(self.play_small_image, self.play_area_end)
		screen.blit(self.small_image, self.init_area)
		screen.blit(self.small_image, self.end_area)

def get_background(blocks_size, enemies_area_y, width, height):
	return BackgroundPhaseOne(blocks_size, enemies_area_y, width, height)