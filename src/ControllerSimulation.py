import pygame
from src.Actions import Actions

class ControllerSimulation:
    def __init__(self):
        pass

    def read_input(self, action):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", 0

        return "move", pygame.Vector2(action[0], action[1])