import random
from src.Actions import Actions
from .ga_lib import weighted_shuffle
import numpy as np


class Individual:

    def __init__(self, state):
        self.state = state
        self.best_position = 1000
        self.action_best_position = -1
        self.poison = 0
        self.win = False
        self.death = -1

    def fitness(self):
        return self.poison + (2 * self.best_position) + self.action_best_position #menor dist para o goal com o menor numero de acoes

    def fitness_roullete(self):
        return 1/self.fitness()

def crossover(s1, s2, point):
    return s1[:point] + s2[point:], s2[:point] + s1[point:]

def selection(population):
    all_fitness = [individual.fitness() for individual in population]
    # print("Mean before selectioN:", np.mean(all_fitness))
    max_f = max(all_fitness) + 1
    p = [max_f - fitness for fitness in all_fitness]
    new = weighted_shuffle(population, p)

    all_fitness_new = [individual.fitness() for individual in new]
    # print("Mean after selectioN:", np.mean(all_fitness_new))

    return new

def roulette_selection(population):
    all_fitness = [ individual.fitness_roullete() for individual in population]
    total = (sum(all_fitness))
    new = []

    for i in range(len(population)):
        r = random.uniform(0, total)
        cum_sum = 0
        for individual in population:
            cum_sum += individual.fitness_roullete()
            if cum_sum >= r:
                new.append(individual)
                break
    return new

def increase_state(population, n_state, d):
    for individual in population:
        state = individual.state
        while len(state) < n_state:
            state.extend([random.choice(list(Actions)).value]*random.randint(1, d))
        individual.state = state[:n_state]

    return population

def mutation(state, state_size, cross_point, idx_dadDeath):
    if (cross_point > idx_dadDeath):#manteve a açao que o pai morreu na sequencia do filho gerado, então muta a partir dessa ação
        # print("state_size - idx_dadDeath", state_size - idx_dadDeath)
        d = random.randint(1, min(state_size - idx_dadDeath, 30))
        # print("Mutating at:", idx_dadDeath, " to", idx_dadDeath+d)
        # print("d", d)
        initial_point = max(1, int(idx_dadDeath*0.85))
        delta_d = idx_dadDeath - initial_point
        state[initial_point:idx_dadDeath+d] = [random.choice(list(Actions)).value]*(d + delta_d)
    else:#a ação que o pai morreu não esta mais no filho. Só muta por "obrigação"
        d = random.randint(1, state_size - cross_point)
        initial_point = cross_point
        state[initial_point:cross_point+d] = [random.choice(list(Actions)).value]*(d)
    return state

def create_initial_population(size, n_state, d):
    population = []
    for i in range(size):
        state = []
        while len(state) < n_state:
            state.extend([random.choice(list(Actions)).value]*random.randint(1, d)) #repeat an action at most d times
            # state.extend([[i] * 5 for i in list(Actions)] * random.randint(1, d))  # repeat an action at most d times
        population.append(Individual(state[:n_state]))
    return population
