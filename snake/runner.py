from snake import *
from neuro import *

snake_direction = { 0:  curses.KEY_RIGHT,
                    1:  curses.KEY_LEFT,
                    2:  curses.KEY_UP,
                    3:  curses.KEY_DOWN}
					
def is_direction_blocked(snake, key_type, field):
    snake.direction = snake_direction[key_type]
    snake.move(field)
    if snake.is_alive(field) == True:
    	return 1
    else:
	return 0

def blocked_directions(snake, snake_position, field):
    snake_next = Snake(0, 0, snake_direction[1])
    snake_next.body = snake_position[:]
    snake_next.direction = snake.direction

    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])
    file = open('log2', 'a+')
    file.write(str(current_direction_vector)+str(left_direction_vector)+str(right_direction_vector)+'\n')
    
    if current_direction_vector[0] > 0:
	key_front = 2
	key_left = 1
	key_right = 0 
    elif current_direction_vector[0] < 0:
	key_front = 3
	key_left = 0
	key_right = 1 
    elif current_direction_vector[1] > 0:	
	key_front = 0
	key_left = 2
	key_right = 3 
    elif current_direction_vector[1] < 0:	
	key_front = 1
	key_left = 3
	key_right = 2 
    else:
		return
    file.write(str(snake_direction[key_front])+' '+str(snake_direction[key_left])+' '+str(snake_direction[key_right])+'\n')
    is_front_blocked = is_direction_blocked(copy.deepcopy(snake_next), key_front, copy.deepcopy(field))
    is_left_blocked = is_direction_blocked(copy.deepcopy(snake_next), key_left, copy.deepcopy(field))
    is_right_blocked = is_direction_blocked(copy.deepcopy(snake_next), key_right, copy.deepcopy(field))
    file.close()
    return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked

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
	
	count_same_direction = 0
    prev_direction = 0

	for _ in range(steps_per_game):
		current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = blocked_directions(snake, snake.body, field)
        
		
		snake.move(field)
        if if_inc_score(snake):
            score +=1
            
        field.render(screen, snake, score)

	    screen.refresh()
	    time.sleep(.1)

	return score