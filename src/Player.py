import math
import pygame
import random
from src.Controller import Controller


class Player:
    def __init__(self, initial_pos: pygame.Vector2, controller=Controller()):
        self.position = initial_pos

        self.controller = controller

        self.width = 20
        self.height = 20

        self.velocity = pygame.Vector2(100, 100)

        self.color = (255, random.randint(0, 255), 0)
        self.current_level = None

        self.dead = False

        self.poison = 0

    def set_init_pos(self, init_pos_vec : pygame.Vector2):
        self.position = init_pos_vec

    def set_current_level(self, level):
        self.current_level = level

    def set_dead(self, boolean):
        self.dead = boolean

    def move(self, mov_vector : pygame.Vector2, dt : float):
        # if mov_vector.length() != 0:
        #     norm_vector = mov_vector.normalize()
        # else:
        norm_vector = mov_vector

        delta = pygame.Vector2()
        delta.x = self.velocity.x * norm_vector.x * dt
        delta.y = self.velocity.y * norm_vector.y * dt

        position_x_y = self.position + delta
        collision_box_x_y = pygame.Rect(position_x_y.x, position_x_y.y, self.width, self.height)
        if self.current_level.main_area.contains(collision_box_x_y) and self.current_level.check_if_inside(collision_box_x_y):
            self.position = position_x_y
            return

        min_delta = pygame.Vector2(norm_vector)

        position_x_y = self.position + min_delta
        #print(position_x_y)
        collision_box_x_y = pygame.Rect(position_x_y.x, position_x_y.y, self.width, self.height)
        if self.current_level.main_area.contains(collision_box_x_y) and self.current_level.check_if_inside(
                collision_box_x_y):
            self.position = position_x_y
            return

        position_x = pygame.Vector2(self.position)
        position_x.x += delta.x
        collision_box_x = pygame.Rect(position_x.x, position_x.y, self.width, self.height)
        if self.current_level.main_area.contains(collision_box_x) and self.current_level.check_if_inside(
                collision_box_x):
            self.position = position_x
            return

        position_y = pygame.Vector2(self.position)
        position_y.y += delta.y
        collision_box_y = pygame.Rect(position_y.x, position_y.y, self.width, self.height)
        if self.current_level.main_area.contains(collision_box_y) and self.current_level.check_if_inside(
                collision_box_y):
            self.position = position_y
            return


    def draw_player(self, surface : pygame.Surface):
        ret = pygame.draw.rect(surface, self.color, (self.position.x, self.position.y, self.width, self.height))

    def collision_box(self):
        return pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    def is_dead(self, enemies):
        player_box = self.collision_box()
        for enemy in enemies:
            if player_box.colliderect(enemy.collision_box()):
                self.dead = True
                return True

        return False

    def get_rect(self):
        return pygame.Rect(self.position.x, self.position.y, self.width, self.height)