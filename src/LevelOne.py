import math
import pygame


class LevelOne():
    def __init__(self, cell_size=30, background_color=(10, 20, 10)):
        self.cell_size = cell_size
        self.background_color = background_color
        self.padding = 0

        self.points = [
            pygame.Vector2(0, 0),
            pygame.Vector2(3*cell_size, 0),
            pygame.Vector2(3 * cell_size, 5 * cell_size),
            pygame.Vector2(4 * cell_size, 5 * cell_size),
            pygame.Vector2(4 * cell_size, 1 * cell_size),
            pygame.Vector2(13 * cell_size, 1 * cell_size),
            pygame.Vector2(13 * cell_size, 0),
            pygame.Vector2(18 * cell_size, 0),
            pygame.Vector2(18 * cell_size, 6 * cell_size),
            pygame.Vector2(15 * cell_size, 6 * cell_size),
            pygame.Vector2(15 * cell_size, 1 * cell_size),
            pygame.Vector2(14 * cell_size, 1 * cell_size),
            pygame.Vector2(14 * cell_size, 5 * cell_size),
            pygame.Vector2(5 * cell_size, 5 * cell_size),
            pygame.Vector2(5 * cell_size, 6 * cell_size),
            pygame.Vector2(0, 6 * cell_size)
        ]
        self.points = [p.elementwise() + self.padding for p in self.points]

        self.init_points = [
            pygame.Vector2(0, 0),
            pygame.Vector2(3 * cell_size, 0),
            pygame.Vector2(3 * cell_size, 6 * cell_size),
            pygame.Vector2(0, 6 * cell_size)
        ]
        self.init_points = [p.elementwise() + self.padding for p in self.init_points]

        self.end_points = [
            pygame.Vector2(15 * cell_size, 0),
            pygame.Vector2(18 * cell_size, 0),
            pygame.Vector2(18 * cell_size, 6 * cell_size),
            pygame.Vector2(15 * cell_size, 6 * cell_size)
        ]
        self.end_points = [p.elementwise() + self.padding for p in self.end_points]

        self.non_walkable_areas = [
            pygame.Rect(
                (3 * cell_size, 0),
                (1 * cell_size, 5 * cell_size)
            ),
            pygame.Rect(
                (3 * cell_size, 0),
                (10 * cell_size, 1 * cell_size)
            ),
            pygame.Rect(
                (5 * cell_size, 5 * cell_size),
                (10 * cell_size, 1 * cell_size)
            ),
            pygame.Rect(
                (14 * cell_size, 1 * cell_size),
                (1 * cell_size, 5 * cell_size)
            )
        ]

        self.walkable_areas = [
            pygame.Rect(
                (3 * cell_size, 5 * cell_size),
                (2 * cell_size, 1 * cell_size)
            ),
            pygame.Rect(
                (3 * cell_size, 5 * cell_size),
                (2 * cell_size, 1 * cell_size)
            ),
            pygame.Rect(
                (4 * cell_size, 1 * cell_size),
                (10 * cell_size, 4 * cell_size)
            ),
            pygame.Rect(
                (13 * cell_size, 0),
                (2 * cell_size, 1 * cell_size)
            ),
            pygame.Rect(
                (0, 0),
                (3 * cell_size, 6 * cell_size)
            ),
            pygame.Rect(
                (15 * cell_size, 0),
                (3 * cell_size, 6 * cell_size)
            ),
            # Connection areas
            pygame.Rect(
                (2 * cell_size, 5 * cell_size),
                (2 * cell_size, 1 * cell_size)
            ),
            pygame.Rect(
                (4 * cell_size, 4 * cell_size),
                (1 * cell_size, 2 * cell_size)
            ),
            pygame.Rect(
                (13 * cell_size, 0),
                (1 * cell_size, 2 * cell_size)
            ),
            pygame.Rect(
                (14 * cell_size, 0),
                (2 * cell_size, 1 * cell_size)
            ),
        ]

        self.player_init = pygame.Vector2(math.ceil(1.5 * cell_size), 3 * cell_size)

        self.enemies_init = [
            pygame.Vector2(9 * cell_size, 1.5 * cell_size),
            pygame.Vector2(9 * cell_size, 2.5 * cell_size),
            pygame.Vector2(9 * cell_size, 3.5 * cell_size),
            pygame.Vector2(9 * cell_size, 4.5 * cell_size),
        ]
        self.enemies_init_direct = [
            1,
            -1,
            1,
            -1,
        ]
        self.enemies_trajectory = [
            (4 * cell_size, 14 * cell_size),
            (4 * cell_size, 14 * cell_size),
            (4 * cell_size, 14 * cell_size),
            (4 * cell_size, 14 * cell_size)
        ]

        self.width = 18 * cell_size + 2 * self.padding
        self.height = 6 * cell_size + 2 * self.padding
        self.surface = pygame.Surface((self.width, self.height))

        self.draw_level_in_surface()

    def check_if_inside(self, rect):
        return len(rect.collidelistall(self.non_walkable_areas)) == 0
        # for area in self.walkable_areas:
        #     if area.contains(rect):
        #         return True
        #
        # return False

    def draw_level_in_surface(self):
        self.surface.fill(self.background_color)
        # self.surface.fill((10, 10, 10))
        self.main_area = pygame.draw.polygon(self.surface, (100, 100, 100), self.points)
        # _ = pygame.draw.polygon(self.surface, (10, 10, 10), self.points, 4)
        self.init_area = pygame.draw.polygon(self.surface, (140, 220, 140), self.init_points)
        self.end_area = pygame.draw.polygon(self.surface, (140, 220, 140), self.end_points)


if __name__ == "__main__":
    pygame.init()
    level = LevelOne(30)
    print(level.points)

    width = 1366
    height = 768

    screen = pygame.display.set_mode((width, height))
    level_screen_x = math.ceil((width - level.width) / 2)
    level_screen_y = math.ceil((height - level.height) / 2)

    clock = pygame.time.Clock()

    while True:
        clock.tick(30)

        screen.fill((10, 20, 10))
        screen.blit(level.surface, (level_screen_x, level_screen_y))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
