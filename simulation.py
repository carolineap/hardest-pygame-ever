from src.AppSimulation import AppSimulation as App
import genetic_algorithm.ga as ga
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def create_mean_graphic(time, pop_min, pop_max, pop_mean, ax_mean, fig_mean, fig_mean_file, index):
	pop_error = [pop_max, pop_min]
	error_interval = (index // 50) + 1
	ax_mean.errorbar(np.arange(index + 1), pop_mean, yerr=pop_error, errorevery=error_interval)

	fig_mean.suptitle('Mean Fitness')
	fig_mean.savefig(str(time) + fig_mean_file, dpi=100)
	plt.close(fig_mean)


def create_best_graphic(time, pop_best, ax_best, fig_best, fig_best_file, index):
	ax_best.plot(np.arange(index + 1), pop_best)

	fig_best.suptitle('Best Fitness')
	fig_best.savefig(str(time) + fig_best_file, dpi=100)
	plt.close(fig_best)

def simulate_game(population_size, sim_type="steady", display=False):

	max_iterations = 500
	state_size = 15 #aumenta o tamanho do cromossomo gradativamente, cinco estados a cada cinco gerações
	i = 0
	j = 0

	d = int(state_size/2)
	
	now = datetime.now()
	# dd/mm/YY-H:M:S
	dt_string = now.strftime("%d/%m/%Y-%H:%M:%S")

	population = ga.create_initial_population(population_size, state_size, d)

	app = App(len(population), display=True)

	# Graphic lists
	pop_max_error = []
	pop_min_error = []
	pop_mean = []
	pop_best = []

	fig_mean_file = 'pop_mean.png'
	fig_best_file = 'pop_max.png'

	while(j < max_iterations and winners < min_winners):

		fig_mean, ax_mean = plt.subplots(figsize=(3, 3))
		fig_best, ax_best = plt.subplots(figsize=(3, 3))

	
		best = None
		worst = None
		best_win = None

		d = int(state_size/2) #max number of repetitions

		print("Starting simulation of generation " + str(j), state_size)
	
		results = app.run([individual.state[:state_size] for individual in population], (state_size))

		for i in range(len(population)):
			population[i].win = results[i][0]
			population[i].best_position = results[i][1]
			population[i].action_best_position = results[i][2]
			population[i].poison = results[i][3]

			if population[i].win:
				print("Alguém venceu!!!")

				if not best_win or population[i].fitness() > best_win.fitness():
					best_win = population[i]

			if not best or population[i].fitness() > best.fitness():
				best = population[i]

			if not worst or population[i].fitness() > worst.fitness():
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
		
		for i in range(int(len(population)/2)):
			ind1, ind2 = ga.selection(population)
			new_population.append(ga.Individual(ga.mutation(ind1.state, ind1.action_best_position-2, d))) #tenta fazer mutação bem perto da melhor posição
			new_population.append(ga.Individual(ga.mutation(ind2.state, ind2.action_best_position-2, d)))
		
		population =  new_population
		
		j += 1

		if j%5 == 0:
			state_size += 20
			population = ga.increase_state(population, state_size, d)

	try:
		filesize = os.path.getsize("tests.csv")
	except:
		filesize = None

	f = open("tests.csv", "a")
	if not filesize:
		f.write("type,population_size,max_iterations,iterations,winners,final_state_size,n,max_state_size,best_number_actions\n")
	f.write(sim_type+","+str(population_size)+","+str(max_iterations)+","+str(j)+","+str(winners)+","+str(state_size)+","+str(n)+","+str(max_state_size)+","+str(best_win.action_best_position)+"\n")
	f.close()

	return best

if __name__ == "__main__":
	population_size = [200, 200, 500, 500]
	sim_type = ["steady", "roulette"]
	bests = []
	for p in population_size:
		for t in sim_type:
			bests.append(simulate_game(p, sim_type=t, display=False))

# app = App(1, display=True)

	# while len(bests):
	# 	best = bests.pop()
	# 	input("Press Enter to continue...")
	# 	app.run([best.state], (len(best.state)))


	
