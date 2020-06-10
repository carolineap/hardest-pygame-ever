import pygame
import math

from src.LevelOne import LevelOne
from src.ControllerSimulation import ControllerSimulation as Controller
from src.Screen import Screen
from src.Player import Player
from src.Enemy import Enemy
from src.Score import Score

class AppSimulation:
    def __init__(self, display=True):
        pygame.init()
       
        self.controller = Controller()
        self.player = Player(pygame.Vector2(0, 0))

        self.clock = pygame.time.Clock()
        self.running = False

        self.action = ""
        self.value = 0

        self.background_color = (200, 200, 200)
        self.level_one = LevelOne(30, self.background_color)

        #self.player.set_init_pos(self.level_one.player_init)
        self.restart()

        self.player.set_current_level(self.level_one)

        enemy_mov_period = 2
        self.enemies = [
            Enemy(self.level_one.enemies_init[i], self.level_one.enemies_init_direct[i], 'h', enemy_mov_period,
                  self.level_one.enemies_trajectory[i][0], self.level_one.enemies_trajectory[i][1])
            for i in range(len(self.level_one.enemies_init))
        ]

        self.score = Score()

        self.display = display

        if display:
            self.main_screen = Screen(background_color=self.background_color)
            pygame.mixer.music.load("SoundTrack/hardestGameThemeSong.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)

    def run(self, actions):        
        self.restart()

        self.running = True

        aux = 0
        current_action = 0

        max_position = self.player.position
        action_max_position = 0

        while self.running and current_action < len(actions):
            ms_dt = self.clock.tick(60)
            s_dt = ms_dt / 800

            self.input_loop(actions[current_action])
            
            win = self.exec_loop(s_dt)

            if max_position[0] < self.player.position[0]:
                max_position = self.player.position
                action_max_position = current_action
           
            if self.display:
                self.render_loop()

            current_action += 1
        
        return win, max_position, action_max_position

    def input_loop(self, action):
        self.action, self.value = self.controller.read_input(action)

    def exec_loop(self, dt):

        if self.action == 'exit':
            pygame.quit()
            exit(0)

        for enemy in self.enemies:
            enemy.move(dt)

        self.player.move(self.value, dt)

        if self.player.is_dead(self.enemies):

            if self.display:
                punchSound = pygame.mixer.Sound("SoundTrack/punch.wav")
                punchSound.play()

            self.score.deaths += 1
        
            self.running = False

            return False, self.player.position

            
        # Check if won
        if self.level_one.end_area.colliderect(self.player.collision_box()):

            self.running = False

            return True, self.player.position

        
        return False, self.player.position
                

    def restart(self):
        self.player.set_init_pos(pygame.Vector2(math.ceil(3 * self.level_one.cell_size), 5 * self.level_one.cell_size))
 

    def render_loop(self):
        self.level_one.draw_level_in_surface()
        self.player.draw_player(self.level_one.surface)

        for enemy in self.enemies:
            enemy.draw_enemy(self.level_one.surface)

        self.main_screen.update_screen(self.level_one)
        
        pygame.display.update()


