from src.AppSimulation import AppSimulation as App
import genetic_algorithm.ga_exchange_entire_population as ga
import random

def simulate_game():
	population_size = 100
	max_iterations = 2000
	best = None
	worst = None
	state_size = 15 #aumenta o tamanho do cromossomo gradativamente, cinco estados a cada cinco gerações
	i = 0
	j = 0

	d = int(state_size/2)

	population = ga.create_initial_population(population_size, state_size, d)

	app = App(len(population), display=True)

	while(j < max_iterations):

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

			if not best or population[i].fitness() < best.fitness():
				best = population[i]

			if not worst or population[i].fitness() > worst.fitness():
				worst = population[i]

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

	print(state_size)

if __name__ == "__main__":
	simulate_game()



	