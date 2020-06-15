import math
import pygame


class Screen:
    def __init__(self, width=1366, height=768, background_color=(10, 20, 10)):
        self.width = width
        self.height = height
        self.background_color = background_color

        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(self.background_color)

    def update_screen(self, level, mean_graph_surface, best_graph_surface):
        self.screen.fill(self.background_color)

        level_screen_x = math.ceil((self.width - level.width) / 2)
        level_screen_y = math.ceil((self.height - level.height) / 2)
        self.screen.blit(level.surface, (level_screen_x, level_screen_y))

        self.screen.blit(mean_graph_surface, (50, 50))
        self.screen.blit(best_graph_surface, (50, 400))
