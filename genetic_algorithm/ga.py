import random
from actions import Actions

class Individual:
    
    def __init__(self, state):
        self.state = state
        self.final_position = (-1, -1)
        
    def fitness(self): 
        return self.final_position[0] + self.final_position[1]

            
def crossover(s1, s2, point): 
    return s1[:point] + s2[point:], s2[:point] + s1[point:]

def selection(population, k): #select k individuals from population based on fitness
    all_fitness = [individual.fitness() for individual in population]
    
    total = sum(all_fitness)
    p = [fitness/total for fitness in all_fitness]
    
    new = random.choices(population, p, k=k)
    return new
    
def mutation(state, point): 
    state[point] = random.choice(list(Actions))
    return state

def create_initial_population(size, n_state):
    population = []
    for i in range(size):
        state = []
        for j in range(n_state):
            state.append(random.choice(list(Actions)))
        population.append(Individual(state))
    return population