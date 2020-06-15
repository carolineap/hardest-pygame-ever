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

    max_f = max(all_fitness) + 1
    p = [max_f - fitness for fitness in all_fitness]

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
    #swap apenas com dois pontos aleatórios
    #point_one = random.randint(0, len(state)-1)
    #point_two = random.randint(0, len(state)-1)
    #state[point_one], state[point_two] = state[point_two], state[point_one]

    #swap de uma sequencia
    tam = len(state)//2
    d = random.randint(1,tam)
    p = tam-d
    #print(d)
    ##print(p)
    state[p:p+d],state[p+d:p+2*d] = state[p+d:p+2*d],state[p:p+d]
    #print(state)

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
