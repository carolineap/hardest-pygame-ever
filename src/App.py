import pygame

from src.LevelOne import LevelOne
from src.Controller import Controller
from src.Screen import Screen
from src.Player import Player
from src.Enemy import Enemy
from src.Score import Score


class App:
    def __init__(self):
        pygame.init()

        self.background_color = (200, 200, 200)
        self.main_screen = Screen(background_color=self.background_color)
        self.controller = Controller()
        self.player = Player(pygame.Vector2(0, 0))

        self.clock = pygame.time.Clock()
        self.running = False

        self.action = ""
        self.value = 0

        self.level_one = LevelOne(30, self.background_color)

        self.player.set_init_pos(self.level_one.player_init)
        self.player.set_current_level(self.level_one)

        enemy_mov_period = 1.5
        self.enemies = [
            Enemy(self.level_one.enemies_init[i], self.level_one.enemies_init_direct[i], 'h', enemy_mov_period,
                  self.level_one.enemies_trajectory[i][0], self.level_one.enemies_trajectory[i][1])
            for i in range(len(self.level_one.enemies_init))
        ]

        self.score = Score()

        pygame.mixer.music.load("SoundTrack/hardestGameThemeSong.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def run(self):
        self.running = True
        
        while self.running:
            ms_dt = self.clock.tick(60)
            s_dt = ms_dt / 1000

            self.input_loop()
            self.exec_loop(s_dt)
            self.render_loop()

    def input_loop(self):
        print('input_loop')
        self.action, self.value = self.controller.read_input()

    def exec_loop(self, dt):
        print('exec_loop')
        if self.action == 'exit':
            pygame.quit()
            exit(0)
        elif self.action == 'move':
            # Move enemies first
            for enemy in self.enemies:
                enemy.move(dt)

            self.player.move(self.value, dt)

            if self.player.is_dead(self.enemies):
                punchSound = pygame.mixer.Sound("SoundTrack/punch.wav")
                punchSound.play()

                self.score.deaths += 1
                self.player.set_init_pos(self.level_one.player_init)

            # Check if won
            if self.level_one.end_area.colliderect(self.player.collision_box()):
                # WIN!
                pygame.quit()
                exit(0)

    def render_loop(self):
        print('render_loop')
        self.level_one.draw_level_in_surface()
        self.player.draw_player(self.level_one.surface)

        for enemy in self.enemies:
            enemy.draw_enemy(self.level_one.surface)

        self.main_screen.update_screen(self.level_one)
        self.score.update_score(self.main_screen.screen)

        pygame.display.update()
