from src.AppSimulation import AppSimulation as App
import genetic_algorithm.ga as ga
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import write_tests as wt

def create_mean_graphic(time, pop_min, pop_max, pop_mean, ax_mean, fig_mean, fig_mean_file, index):
	pop_error = [pop_max, pop_min]
	error_interval = (index // 50) + 1
	ax_mean.errorbar(np.arange(index + 1), pop_mean, yerr=pop_error, errorevery=error_interval)
	ax_mean.set_xlabel("geração")
	ax_mean.set_ylabel('fitness')
	fig_mean.suptitle('Mean Fitness')
	fig_mean.savefig(str(time) + fig_mean_file, dpi=100)
	plt.close(fig_mean)

def create_best_graphic(time, pop_best, ax_best, fig_best, fig_best_file, index):
	ax_best.plot(np.arange(index + 1), pop_best)
	ax_best.set_xlabel("geração")
	ax_best.set_ylabel('fitness')
	fig_best.suptitle('Best Fitness')
	fig_best.savefig(str(time) + fig_best_file, dpi=100)
	plt.close(fig_best)

def simulate_game(seed, population_size, sim_type="steady", display=False):
	random.seed(seed) 
	
	max_iterations = 500
	state_size = 15 
	i = 0
	j = 0
	
	increase_state = 0
	winners = 0
	min_winners = int(0.5*population_size)

	now = datetime.now()
	# dd/mm/YY-H:M:S
	dt_string = now.strftime("Tests/Figures/" + sim_type + "-" + str(population_size) +"%d-%m-%Y-%H:%M:%S")
	n = 5

	max_state_size = 500

	state_increment = 10

	d = int((state_size/2))

	population = ga.create_initial_population(population_size, state_size, d)

	best_win = None

	# Graphic lists
	pop_max_error = []
	pop_min_error = []
	pop_mean = []
	pop_best = []

	fig_mean_file = 'pop_mean.png'
	fig_best_file = 'pop_max.png'

	best_win = None

	app = App(len(population), display=display)

	while(j < max_iterations and winners < min_winners):

		fig_mean, ax_mean = plt.subplots(figsize=(6, 6))
		fig_best, ax_best = plt.subplots(figsize=(6, 6))
		
		best = None
		worst = None

		d = int((state_size/2)) #max number of repetitions

		print("Starting simulation of generation " + str(j), state_size)
	
		results = app.run([individual.state[:state_size] for individual in population], (state_size))

		for i in range(len(population)):
			population[i].win = results[i][0]
			population[i].best_position = results[i][1]
			population[i].action_best_position = results[i][2]
			population[i].poison = results[i][3]

			if population[i].win:
				print("Alguém venceu!!!")
				winners += 1

			if population[i].win:
				if not best_win or population[i].fitness() > best_win.fitness():
					best_win = population[i]

			if not best or population[i].fitness() > best.fitness():
				best = population[i]

			if not worst or population[i].fitness() < worst.fitness():
				worst = population[i]

		population_mean = np.mean([p.fitness() for p in population])

		pop_mean.append(population_mean)
		pop_min_error.append(worst.fitness() - population_mean)
		pop_max_error.append(population_mean - best.fitness())

		pop_best.append(best.fitness())

		create_mean_graphic(dt_string, pop_min_error, pop_max_error, pop_mean, ax_mean, fig_mean, fig_mean_file, j)
		app.update_mean_graph(str(dt_string) + fig_mean_file)

		create_best_graphic(dt_string, pop_best, ax_best, fig_best, fig_best_file, j)
		app.update_max_graph(str(dt_string) + fig_best_file)

		new_population = []		

		if type == "steady":
			clone_pop, crossover_pop = ga.selection(population)

			for ind in clone_pop:
				if ind.fitness() == best.fitness():
					new_state = ga.mutation(ind.state, ind.action_best_position, d)
				else:
					new_state = ga.mutation(ind.state, ind.action_best_position-random.randint(0, 5), d)
				new_population.append(ga.Individual(new_state))
			
			for i in range(int(len(crossover_pop)/2), 2):
				point = min(crossover_pop[i].action_best_position, crossover_pop[i+1].action_best_position)
				ind1, ind2 = ga.crossover(crossover_pop[i].state, crossover_pop[i+1].state, point)
				new_population.append(ga.Individual(ind1)) 
				new_population.append(ga.Individual(ind2))
		else:
			selected = ga.roulette_selection(population)

			for ind in selected:
				if ind.fitness() == best.fitness():
					new_state = ga.mutation(ind.state, ind.action_best_position, d)
				else:
					new_state = ga.mutation(ind.state, ind.action_best_position-random.randint(0, 5), d)
				new_population.append(ga.Individual(new_state))

		population = new_population.copy()
		
		j += 1

		increase_state += 1

		if (increase_state%n == 0 or best.action_best_position - 5 >= state_size) and (state_size+state_increment) <= max_state_size:
			state_size += state_increment
			population = ga.increase_state(population, state_size, d)
			increase_state = 0

	if not best_win:
		best_solution = 0
		best_state = 0
	else:
		best_solution = best_win.action_best_position
		best_state = best_win.state

	wt.write_csv("simulation_one_"+str(population_size), sim_type, population_size, max_iterations, j, winners, state_size, n, state_increment, max_state_size, best_solution,best_state)

if __name__ == "__main__":
	number_of_tests = 9
	seeds = [i*10 for i in range(0, number_of_tests*2)] # x2 because has steady and roullete type
	population_size = [200]*number_of_tests
	sim_type = ["steady", "roulette"]
	i = 0
	for p in population_size:
		for t in sim_type:
			simulate_game(seeds[i], p, sim_type=t, display=False)
			i += 1

