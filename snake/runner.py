from snake import *
from neuro import *

snake_direction = { 0:  curses.KEY_RIGHT,
                    1:  curses.KEY_LEFT,
                    2:  curses.KEY_UP,
                    3:  curses.KEY_DOWN}
					
def run_game(weights, screen):
	score = 0

	field_size = 20
	field_border = 3
	snake_pos_x = randint(field_border,field_size-field_border)
	snake_pos_y = randint(field_border,field_size-field_border)
	key_type = randint(0,3)

	snake = Snake(snake_pos_x, snake_pos_y, snake_direction[key_type])
   	field = Field(field_size, field_size, snake)
	snake_is_alive = True
	
	steps_per_game = 20

	for _ in range(steps_per_game):
		snake.move(field)
        if if_inc_score(snake):
            score +=1
            
        field.render(screen, snake, score)

	    screen.refresh()
	    time.sleep(.1)

	return score