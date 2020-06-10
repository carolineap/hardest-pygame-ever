import pygame
from src.Actions import Actions

class ControllerSimulation:
    def __init__(self):
        pass

    def read_input(self, action):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", 0
    
        x_movement = 0
        x_movement += 1 if action in (Actions.RIGHT, Actions.UP_RIGHT, Actions.DOWN_RIGHT) else 0
        x_movement -= 1 if action in (Actions.LEFT, Actions.UP_LEFT, Actions.DOWN_LEFT) else 0

        y_movement = 0
        y_movement -= 1 if action in (Actions.UP, Actions.UP_RIGHT, Actions.UP_LEFT) else 0
        y_movement += 1 if action in (Actions.DOWN, Actions.DOWN_LEFT, Actions.DOWN_RIGHT) else 0

        return "move", pygame.Vector2(x_movement, y_movement)