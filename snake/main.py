from genetic import *
from snake import *
from neuro import *
import curses

# n_x -> no. of input units
# n_h -> no. of units in hidden layer 1
# n_h2 -> no. of units in hidden layer 2
# n_y -> no. of output units
def main(screen):
	sol_per_pop = 50
	num_weights = n_x*n_h + n_h*n_h2 + n_h2*n_y

	pop_size = (sol_per_pop,num_weights)

	new_population = np.random.choice(np.arange(-1,1,step=0.01),size=pop_size,replace=True)

	num_generations = 100
	file = open('log', 'w')

	num_parents_mating = 12
	for generation in range(num_generations):
		file.write('##############		GENERATION ' + str(generation)+ '  ###############\n' )
		fitness = cal_pop_fitness(new_population, screen, file)
		file.write('#######  fittest chromosome in gneneration ' + str(generation) +' is having fitness value:  ' + str(np.max(fitness)) + '\n')
		parents = select_mating_pool(new_population, fitness, num_parents_mating)
		offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))
		offspring_mutation = mutation(offspring_crossover)
		new_population[0:parents.shape[0], :] = parents
		new_population[parents.shape[0]:, :] = offspring_mutation
	file.close()
	
if __name__ == "__main__":
	curses.wrapper(main)
