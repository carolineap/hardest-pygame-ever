import copy

import pygame
from src.Controls import Controls


class Controller:
    def __init__(self):
        pass

    def read_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", 0

        keys_pressed = pygame.key.get_pressed()
        # print(keys_pressed)
        controls = self.controls_pressed(keys_pressed)
        # print(controls)
        # controls = self.filter_controls(controls)

        if Controls.EXIT in controls:
            return "exit", 0

        x_movement = 0
        x_movement += 1 if Controls.RIGHT in controls else 0
        x_movement -= 1 if Controls.LEFT in controls else 0

        y_movement = 0
        y_movement -= 1 if Controls.UP in controls else 0
        y_movement += 1 if Controls.DOWN in controls else 0

        # print((x_movement, y_movement))

        return "move", pygame.Vector2(x_movement, y_movement)

    def controls_pressed(self, keys_pressed):
        controls = []

        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            controls.append(Controls.UP)
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            controls.append(Controls.DOWN)
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            controls.append(Controls.LEFT)
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            controls.append(Controls.RIGHT)
        if keys_pressed[pygame.K_ESCAPE]:
            controls.append(Controls.EXIT)

        return controls
