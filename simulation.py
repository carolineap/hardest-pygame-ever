from src.AppSimulation import AppSimulation as App
import genetic_algorithm.ga as ga
import random


def simulate_game(population, best, display=True):

	app = App(display=display)

	for individual in population:	
		individual.win, individual.max_position, individual.action_max_position = app.run(individual.state)

		if not best or individual.fitness() > best.fitness():
			best = individual

		print(individual.fitness())

	return best

if __name__ == "__main__":

	POPULATION_SIZE = 10
	STATE_SIZE = 300
	K = 2 
	N_ITERATIONS = 10
	D = 10

	best = None

	population = ga.create_initial_population(POPULATION_SIZE, STATE_SIZE, D)

	while(N_ITERATIONS):

		print("Starting simulation of a population...")
	
		b = simulate_game(population, best, display=False) 

		if not best or best.fitness() < b.fitness():
			best = b 
		
		new_population = []

		selected = ga.selection(population)

		for i in range(0, len(population)-1, 2):

			print("fitness selected:")
			print(selected[i].fitness())

			min_point = min(selected[i].action_max_position, selected[i+1].action_max_position)
			max_point = max(selected[i].action_max_position, selected[i+1].action_max_position)

			s1, s2 = selected[i].state, selected[i+1].state
			s1, s2 = ga.crossover(s1, s2, random.randint(min_point, max_point))

			new_population.append(ga.Individual(ga.mutation(s1, random.randint(min_point, max_point), D)))
			new_population.append(ga.Individual(ga.mutation(s2, random.randint(min_point, max_point), D)))            
		
		population =  new_population

		print(len(population))
		
		N_ITERATIONS -= 1

	input("Press Enter to continue...")
	simulate_game([best], best, display=True)
