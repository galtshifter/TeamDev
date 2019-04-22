from runner import *
from random import choice, randint

def cal_pop_fitness(pop, screen, file):
    # calculating the fitness value by playing a game with the given weights in chromosome
    fitness = []
    for i in range(pop.shape[0]):
        fit = run_game(pop[i], screen)
        file.write('fitness value of chromosome '+ str(i) +' :  ' +str(fit) + '\n')
        fitness.append(fit)
    return np.array(fitness)