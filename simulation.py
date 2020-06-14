from src.AppSimulation import AppSimulation as App
import genetic_algorithm.ga as ga
import random
import os

def simulate_game(sim_type="steady"):
	population_size = 500
	max_iterations = 500
	best = None
	worst = None
	state_size = 15 #aumenta o tamanho do cromossomo gradativamente, cinco estados a cada cinco gerações
	i = 0
	j = 0
	increase_state = 0
	winners = 0
	min_winners = int(0.5*population_size)

	n = 5

	max_state_size = 500

	state_increment = 10

	d = 10

	population = ga.create_initial_population(population_size, state_size, d)

	app = App(len(population), display=False)

	while(j < max_iterations and winners < min_winners):

		d = random.randint(5, int(state_size/2)) #max number of repetitions

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

			if not best or population[i].fitness() > best.fitness():
				best = population[i]

			if not worst or population[i].fitness() < worst.fitness():
				worst = population[i]

		new_population = []		

		if type == "steady":
			clone_pop, crossover_pop = ga.selection(population)

			for ind in clone_pop:
				if ind.fitness() == best.fitness():
					new_state = ga.mutation(ind.state, ind.action_best_position, d)
				else:
					new_state = ga.mutation(ind.state, ind.action_best_position-random.randint(0, 5), d)
				new_population.append(ga.Individual(new_state))
			
			for i in range(int(len(crossover_pop)/2)):
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

	filesize = os.path.getsize("tests.txt")

	f = open("tests.txt", "a")
	if not filesize:
		f.write("type;population_size;max_iterations;winners;final_state_size;n;max_state_size\n")
	f.write(sim_type+";"+str(population_size)+";"+str(max_iterations)+";"+str(winners)+";"+str(state_size)+";"+str(n)+";"+str(max_state_size)+"\n")
	f.close()

if __name__ == "__main__":
	simulate_game(sim_type="roulette")



	