import pygame
import math

from src.LevelOne import LevelOne
from src.ControllerSimulation import ControllerSimulation as Controller
from src.Screen import Screen
from src.Player import Player
from src.Enemy import Enemy
from src.Score import Score

class AppSimulation:
    def __init__(self, population_size, display=True):
        pygame.init()
        self.controller = Controller()

        self.players = []
        for i in range(population_size):
            self.players.append((Player(pygame.Vector2(0, 0))))

        self.clock = pygame.time.Clock()
        self.running = False

        self.action = ""
        self.value = 0

        self.background_color = (200, 200, 200)
        self.level_one = LevelOne(30, self.background_color)

        enemy_mov_period = 2
        self.enemies = [
            Enemy(self.level_one.enemies_init[i], self.level_one.enemies_init_direct[i], 'h', enemy_mov_period,
                  self.level_one.enemies_trajectory[i][0], self.level_one.enemies_trajectory[i][1])
            for i in range(len(self.level_one.enemies_init))
        ]

        self.restart()

        self.display = display

        if display:
            self.main_screen = Screen(background_color=self.background_color)
            pygame.mixer.music.load("SoundTrack/hardestGameThemeSong.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)

    def run(self, actions, n):        
        self.restart()
        
        results = []
        for i in range(len(self.players)):
            results.append([False, 1000, -1])

        for i in range(n):
            
            ms_dt = self.clock.tick(60)    
            s_dt = ms_dt / 800

            self.move_enemies(s_dt)
            
            for j in range(len(self.players)):

                if not self.players[j].dead:

                    self.input_loop(actions[j][i])

                    results[j][0] = self.exec_loop(s_dt, j) #win

                    if results[j][1] > self.level_one.distance(self.players[j]):
                        results[j][1] = self.level_one.distance(self.players[j]) #get value and action for best position (closest to the goal)
                        results[j][2] = i
           
            if self.display:
                self.render_loop()  

        return results


    def input_loop(self, action):
        self.action, self.value = self.controller.read_input(action)

    def move_enemies(self, dt):
        for enemy in self.enemies:
            enemy.move(dt)

    def exec_loop(self, dt, j):
        if self.action == 'exit':
            pygame.quit()
            exit(0)

        self.players[j].move(self.value, dt)

        if self.players[j].is_dead(self.enemies):
            return False
            
        # Check if won
        if self.level_one.end_area.colliderect(self.players[j].collision_box()):
            return True

        return False
                
    def restart(self):
        for player in self.players:
            player.set_init_pos(self.level_one.player_init)
            player.set_current_level(self.level_one)
            player.set_dead(False) 

    def render_loop(self):
        self.level_one.draw_level_in_surface()

        for player in self.players:
            if not player.dead:
                player.draw_player(self.level_one.surface)
            
        for enemy in self.enemies:
            enemy.draw_enemy(self.level_one.surface)

        self.main_screen.update_screen(self.level_one)
        
        pygame.display.update()



