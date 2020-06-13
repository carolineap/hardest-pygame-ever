import random
from src.Actions import Actions
from .ga_lib import weighted_shuffle

class Individual:

    def __init__(self, state):
        self.state = state
        self.best_position = 1000
        self.action_best_position = -1
        self.poison = 0
        self.win = False

    def fitness(self):
        return self.poison + (1*self.best_position) + self.action_best_position #menor dist para o goal com o menor numero de acoes
#
def crossover(s1, s2, point):
    return s1[:point] + s2[point:], s2[:point] + s1[point:]

def selection(population):
    all_fitness = [individual.fitness() for individual in population]

    total = sum(all_fitness)
    p = [(1-(fitness/total)) for fitness in all_fitness]

    new = weighted_shuffle(population, p)

    return new

def increase_state(population, n_state, d):
    for individual in population:
        state = individual.state
        while len(state) < n_state:
            state.extend([random.choice(list(Actions)).value]*random.randint(1, d))
        individual.state = state[:n_state]

    return population

def mutation(state):
    point_one = random.randint(0, len(state)-1)
    point_two = random.randint(0, len(state)-1)
    #print(point_one)
    #print(point_two)
    state[point_one], state[point_two] = state[point_two], state[point_one]
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