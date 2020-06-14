from src.AppSimulation import AppSimulation as App
import genetic_algorithm.ga_exchange_entire_population as ga
import random

def simulate_game():
	population_size = 150
	max_iterations = 2000

	state_size = 30 #aumenta o tamanho do cromossomo gradativamente, cinco estados a cada cinco gerações
	crossover_pos = 1
	i = 0
	j = 0

    d = int(state_size/2)

    population = ga.create_initial_population(population_size, state_size, d)

    app = App(len(population), display=True)

    while(j < max_iterations):

        d = int(state_size/2) #max number of repetitions

		print("Starting simulation of generation " + str(j), state_size)
		best = None
		worst = None
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

        parents_selection = ga.selection(population)
        for i in range(int(len(parents_selection)/2)):
            new_ind_1_crom, new_ind_2_crom = ga.crossover(parents_selection[i].state, parents_selection[i+1].state, state_size - 10)

            if random.random() <= mutation_rate:
                new_ind_1_crom = ga.mutation(new_ind_1_crom)
                new_ind_2_crom = ga.mutation(new_ind_2_crom)

            new_population.append(ga.Individual(new_ind_1_crom))
            new_population.append(ga.Individual(new_ind_2_crom))

        population =  new_population

        j += 1

        if j%5 == 0 and state_size <=500:
            state_size += 5
            population = ga.increase_state(population, state_size, d)

    print(state_size)

if __name__ == "__main__":
    simulate_game()
