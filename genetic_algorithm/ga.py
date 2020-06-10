import random
from src.Actions import Actions

class Individual:
    
    def __init__(self, state):
        self.state = state
        self.max_position = (-1, -1)
        self.win = False
        self.action_max_position = 0
        
    def fitness(self): 
        return self.max_position[0]

            
def crossover(s1, s2, point): 
    return s1[:point] + s2[point:], s2[:point] + s1[point:]

def selection(population): #just remove the worst individual and clone the best
    all_fitness = [individual.fitness() for individual in population]
    
    total = sum(all_fitness)
    p = sorted([fitness/total for fitness in all_fitness], reverse=True)

    min_i = p.index(min(p))
    max_i = p.index(max(p))

    new = population.copy()
    
    new.pop(min_i)
    new.append(population[max_i])

    random.shuffle(new)

    return new
    
def mutation(state, point, d): 
    d = random.randint(3, d)
    state[point:point+d] = [random.choice(list(Actions))]*d
    return state

def create_initial_population(size, n_state, d):
    population = []
    for i in range(size):
        state = []
        while len(state) < n_state:
            state.extend([random.choice(list(Actions))]*random.randint(3, d)) #repeat an action at most d times
        population.append(Individual(state[:n_state]))
    return population