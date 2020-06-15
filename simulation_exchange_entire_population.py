from src.AppSimulation import AppSimulation as App
import genetic_algorithm.ga_exchange_entire_population as ga
import random
import os

def simulate_game(population_size, display):
    max_iterations = 2000
    state_size = 30
    i = 0
    j = 0
    increase_state = 0
    winners = 0
    min_winners = int(0.5*population_size)


    mutation_rate = 0.3
    crossover_pos = 1

    n = 5

    max_state_size = 900

    state_increment = 20

    d = int((state_size/2))

    population = ga.create_initial_population(population_size, state_size, d)

    app = App(len(population), display=display)

    while(j < max_iterations and winners < min_winners):

        best = None
        worst = None

        d = int(state_size/2) #max number of repetitions

        print("Starting simulation of generation " + str(j), state_size)

        results = app.run([individual.state[:state_size] for individual in population], (state_size))

        for i in range(len(population)):
            population[i].win = results[i][0]
            population[i].best_position = results[i][1]
            population[i].action_best_position = results[i][2]
            population[i].poison = results[i][3]

            best_win = population[i]

            if population[i].win:
                print("Alguém venceu!!!")
                winners += 1

            if population[i].win:
                if not best_win or population[i].fitness() > best_win.fitness():
                    best_win = population[i]

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

        population =  new_population

        increase_state += 1

        if (increase_state%n == 0 or best.action_best_position - 5 >= state_size) and (state_size+state_increment) <= max_state_size:
            crossover_pos += 0.05
            state_size += state_increment
            population = ga.increase_state(population, state_size, d)
            increase_state = 0

    try:
        filesize = os.path.getsize("simulation-exchange-entire-population.csv")
    except:
        filesize = None

    f = open("simulation-exchange-entire-population.csv", "a")
    if not filesize:
        f.write("type,population_size,max_iterations,iterations,winners,final_state_size,n,max_state_size,best_number_actions\n")
    f.write("exchange-entire-pop,"+str(population_size)+","+str(max_iterations)+","+str(j)+","+str(winners)+","+str(state_size)+","+str(n)+","+str(max_state_size)+","+str(best_win.action_best_position)+"\n")
    f.close()

    return best_win

if __name__ == "__main__":
    population_size = [200, 200, 200, 500, 500, 500]

    bests = []
    for p in population_size:
        bests.append(simulate_game(p, display=True))
