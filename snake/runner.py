import curses
import copy
import math
import random
import time
from snake import *
from neuro import *

snake_direction = { 0:  curses.KEY_RIGHT,
					1:  curses.KEY_LEFT,
					2:  curses.KEY_UP,
					3:  curses.KEY_DOWN}


def angle_with_apple(snake_position, apple_position):
	apple_direction_vector = np.array(apple_position) - np.array(snake_position[0])
	snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

	norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
	norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)
	if norm_of_apple_direction_vector == 0:
		norm_of_apple_direction_vector = 1
	if norm_of_snake_direction_vector == 0:
		norm_of_snake_direction_vector = 1

	apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
	snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector
	angle = math.atan2(
		apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] - apple_direction_vector_normalized[
			0] * snake_direction_vector_normalized[1],
		apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] + apple_direction_vector_normalized[
			0] * snake_direction_vector_normalized[0]) / math.pi
	return angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized


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
	#file.write(str(current_direction_vector)+str(left_direction_vector)+str(right_direction_vector)+'\n')
	
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
	#file.write(str(snake_direction[key_front])+' '+str(snake_direction[key_left])+' '+str(snake_direction[key_right])+'\n')
	is_front_blocked = is_direction_blocked(copy.deepcopy(snake_next), key_front, copy.deepcopy(field))
	is_left_blocked = is_direction_blocked(copy.deepcopy(snake_next), key_left, copy.deepcopy(field))
	is_right_blocked = is_direction_blocked(copy.deepcopy(snake_next), key_right, copy.deepcopy(field))
	#file.close()
	return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked

def generate_button_direction(new_direction):
	button_direction = 0
	if new_direction.tolist() == [1, 0]:
		button_direction = 2
	elif new_direction.tolist() == [-1, 0]:
		button_direction = 3
	elif new_direction.tolist() == [0, 1]:
		button_direction = 0
	else:
		button_direction = 1

	return button_direction

def run_game(weights, screen):
	score = 0
	score1 = 0
	score2 = 0
	avg_score = 0	
	max_score =0
	steps_per_game = 100

	field_size = 20
	field_border = 3
	snake_pos_x = random.randint(field_border,field_size-field_border)
	snake_pos_y = random.randint(field_border,2*field_size-field_border)
	key_type = random.randint(0,3)

	snake = Snake(snake_pos_x, snake_pos_y, snake_direction[key_type])
	field = Field(field_size, 2*field_size, snake)
	snake_is_alive = True

	count_same_direction = 0
	prev_direction = 0

	for _ in range(steps_per_game):
		current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = blocked_directions(snake, snake.body, field)
		angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized = angle_with_apple(snake.body, field.food)
		predictions = []
		predicted_direction = np.argmax(np.array(forward_propagation(np.array(
		[is_left_blocked, is_front_blocked, is_right_blocked, apple_direction_vector_normalized[0],
				 snake_direction_vector_normalized[0], apple_direction_vector_normalized[1],
				 snake_direction_vector_normalized[1]]).reshape(-1, 7), weights))) - 1

		if predicted_direction == prev_direction:
			count_same_direction += 1
		else:
			count_same_direction = 0
			prev_direction = predicted_direction

		new_direction = np.array(snake.body[0]) - np.array(snake.body[1])
		if predicted_direction == -1:
			new_direction = np.array([new_direction[1], -new_direction[0]])
		if predicted_direction == 1:
			new_direction = np.array([-new_direction[1], new_direction[0]])

		button_direction = generate_button_direction(new_direction)

		if snake.is_alive(field):
			score1 += 0
			 
		else:
			score1 += -150
			break

		snake.direction = snake_direction[button_direction]
		snake.move(field)
		if if_inc_score(snake):
			score +=1
			
		field.render(screen, snake, score)

		screen.refresh()
		time.sleep(.001)

		if score > max_score:
			max_score = score

		if count_same_direction > 8 and predicted_direction != 0:
			score2 -= 1
		else:
			score2 += 2

	return score, score1 + score2 + max_score * 500


