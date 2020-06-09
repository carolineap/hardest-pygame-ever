import math
import pygame


class Score:
    def __init__(self, width=1366, height=50, background_color=(10, 20, 10)):
        self.width = width
        self.height = height
        self.background_color = background_color

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.background_color)

        self.font = pygame.font.Font('freesansbold.ttf', 28)
        self.deaths = 0

    def update_score(self, screen):
        self.surface.fill(self.background_color)
        score_font = self.font.render('Deaths: %s' % (self.deaths), True, (255, 255, 255))
        score_rect = score_font.get_rect()
        print('score_rect', score_rect)

        score_rect.center = ((self.width) / 2, (self.height) / 2)
        self.surface.blit(score_font, score_rect)

        score_screen_x = 0
        score_screen_y = 0
        screen.blit(self.surface, (score_screen_x, score_screen_y))
