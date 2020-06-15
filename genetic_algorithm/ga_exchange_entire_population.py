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
        self.death = -1

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

def mutationImproved(state, state_size, cross_point, idx_dadDeath):
    if (cross_point > idx_dadDeath):#manteve a açao que o pai morreu na sequencia do filho gerado, então muta a partir dessa ação
        d = random.randint(1, state_size - idx_dadDeath)
        state[idx_dadDeath:idx_dadDeath+d] = [random.choice(list(Actions)).value]*d
    else:#a ação que o pai morreu não esta mais no filho. Só muta por "obrigação"
        d = random.randint(1, state_size - cross_point)
        state[cross_point:cross_point+d] = [random.choice(list(Actions)).value]*d

    #print(state_size, " ", cross_point, " ", idx_dadDeath, " ", d)
    #print(state)
    #print("-----------------")
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
