from neuro import *

# n_x -> no. of input units
# n_h -> no. of units in hidden layer 1
# n_h2 -> no. of units in hidden layer 2
# n_y -> no. of output units
def main(screen):
	sol_per_pop = 50
	num_weights = n_x*n_h + n_h*n_h2 + n_h2*n_y

	pop_size = (sol_per_pop,num_weights)

if __name__ == "__main__":
    curses.wrapper(main)