import os

def write_csv(file_name, sim_type, population_size, max_iterations, j, winners, state_size, n, increment_size, max_state_size, best_number_actions, best_state):
	file_name = "Tests/" + file_name + ".csv"
	try:
		filesize = os.path.getsize(file_name)
	except:
		filesize = None

	f = open(file_name, "a")
	if not filesize:
		f.write("type,population_size,max_iterations,iterations,winners,final_state_size,n,increment_size, max_state_size,best_number_actions,best_state\n")
	f.write(sim_type+","+str(population_size)+","+str(max_iterations)+","+str(j)+","+str(winners)+","+str(state_size)+","+str(n)+","+str(increment_size)+","+str(max_state_size)+","+str(best_number_actions)+","+str(best_state)+"\n")
	f.close()