# -*- coding: utf-8 -*-

import curses
import time
from random import randint



directions = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]


field_dictionary = {-1: '/',
					0:  ' ',
					1:  '#',
					2:  'o',
					3:  '0',
					4:  'w'}


class Field:
	def __init__(self, height, width, snake):
		self.height = height
		self.width = width
		self.cells = [[0 for i in range(self.width+2)] for j in range(self.height+2)]

		#setting border
		for j in range(self.height+2):
			self.cells[j][0] = -1
			self.cells[j][self.width+1] = -1
		for i in range(1, self.width+1):
			self.cells[0][i] = -1
			self.cells[self.height+1][i] = -1
		
		self.food_gen(snake)
		
			 
	def clear_field(self):
		for j in range(1, self.height+1):
			for i in range(1, self.width+1):
				self.cells[j][i] = 0		
		return


	def set_field(self, snake):
		# Setting field
		self.clear_field()

		#setting food
		self.cells[self.food[0]][self.food[1]] = 4

		# Setting body
		for i in snake.body[1:]:
			if i in snake.eaten_food:
				self.cells[i[0]][i[1]] = 3 
			else:
				self.cells[i[0]][i[1]] = 2 

		# Setting head
		self.cells[snake.body[0][0]][snake.body[0][1]] = 1


	def render(self, screen, snake, score):
		
		self.set_field(snake)
		screen.clear()
		for j in range(0, self.height+2):
			for i in range(0, self.width+2):
				screen.addstr(j, i, field_dictionary[self.cells[j][i]])
		screen.addstr(24, 2, 'Your score: ' + str(score))


	def food_gen(self, snake):
		a = [randint(1, self.height), randint(1, self.width)]
		#checking if generated food hit the body
		while a in snake.body:
			a = [randint(1, self.height), randint(1, self.width)]
		self.food = a


class Snake:
	def __init__(self, y, x, direction):
		self.body = [[y, x], [y, x-1], [y, x-2]]
		self.direction = direction
		self.eaten_food = []

	def is_alive(self, field):
		#checking if snake hit the wall
		if (self.body[0][0] == 0) or (self.body[0][0] == field.height+1) or (self.body[0][1] == 0) or (self.body[0][1] == field.width+1):
			return False
		#checking if snake hit itself
		if (self.body[0] in self.body[1:]):
			return False
		return True


	def set_direction(self, key):
		if key == curses.KEY_LEFT and self.direction == curses.KEY_RIGHT:
			return
		if key == curses.KEY_RIGHT and self.direction == curses.KEY_LEFT:
			return
		if key == curses.KEY_UP and self.direction == curses.KEY_DOWN:
			return
		if key == curses.KEY_DOWN and self.direction == curses.KEY_UP:
			return 
		self.direction = key
	
	def move(self, field):
		dy = 0
		dx = 0
		if (self.direction == curses.KEY_UP):
			dy = -1
		elif (self.direction == curses.KEY_DOWN):
			dy = 1
		elif (self.direction == curses.KEY_LEFT):
			dx = -1
		elif (self.direction == curses.KEY_RIGHT):
			dx = 1
		else:
			return

		y = self.body[0][0] + dy
		x = self.body[0][1] + dx

		#checking if snake have just eaten food
		if [y, x] == field.food:
			self.eaten_food.append([y, x])
			field.food_gen(self)

		self.body.insert(0, [y, x])
		self.body.pop()

		#checking if the length of the body should increase
		for i in self.eaten_food:
			if i not in self.body:
				self.eaten_food.remove(i)
				self.body.append(i)
				# break # can be uncomment if snake will start lagging
			

def if_inc_score(snake):
	return True if (len(snake.eaten_food) != 0) and (snake.eaten_food[0] == snake.body[0]) else False
		
'''
def main(screen):

	screen.timeout(1)

	snake = Snake(5, 5, curses.KEY_RIGHT)
	field = Field(20, 20, snake)
	snake_is_alive = True
	score = 0

	while snake_is_alive:
		key = screen.getch()

		if key in directions:
			snake.set_direction(key)
		
		snake.move(field)

		if if_inc_score(snake):
			score +=1
			
		field.render(screen, snake, score)

		if not(snake.is_alive(field)):
			snake_is_alive = False
		
		time.sleep(.4)
	else:
		screen.timeout(-1)
		screen.addstr(23, 2, 'Oops, you died. Press End to exit the game')
		while (screen.getch() != curses.KEY_END):
			pass
		

if __name__ == "__main__":
	curses.wrapper(main)
'''
