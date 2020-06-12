import math
import pygame


class Enemy:
    def __init__(self, initial_pos : pygame.Vector2, initial_direction, trajectory_type, trajectory_period, trajectory_begin, trajectory_end):
        self.position = initial_pos
        self.direction = initial_direction

        self.trajectory_type = trajectory_type
        self.trajectory_begin = trajectory_begin
        self.trajectory_end = trajectory_end
        self.trajectory_period = trajectory_period

        if trajectory_type == 'h':
            self.velocity = pygame.Vector2((trajectory_end - trajectory_begin) / trajectory_period, 0)

        self.radius = 9
        self.position = self.position.elementwise() - self.radius

        self.color = (0, 0, 255)
        self.current_level = None

    def move(self, dt: float):
        if self.is_at_end():
            self.direction *= -1

        self.position += self.velocity * dt * self.direction

    def is_at_end(self):
        if self.position.x >= self.trajectory_end - 2 * self.radius or \
            self.position.x <= self.trajectory_begin + 1:
            return True

        return False

    def collision_box(self):
        return pygame.Rect((int(self.position.x), int(self.position.y)), (self.radius * 2, self.radius * 2))

    def draw_enemy(self, surface):
        ret = pygame.draw.circle(surface, self.color, (int(self.position.x + self.radius), int(self.position.y + self.radius)), self.radius)
        #print(ret)
