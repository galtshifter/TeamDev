import curses
import time
from random import randint


directions = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]


field_dictionary = {-1: '░',
                    0:  ' ',
                    1:  '#',
                    2:  'o',
                    3:  '0',
                    4:  'ж'}


class Field:
    def __init__(self, height, width, snake):
        self.height = height
        self.width = width
        self.cells = [[0 for i in range(self.width+2)] for j in range(self.height+2)]
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

        self.cells[self.food[0]][self.food[1]] = 4

        # Setting body
        for i in snake.body[1:]:
            if i in snake.eaten_food:
                self.cells[i[0]][i[1]] = 3 
            else:
                self.cells[i[0]][i[1]] = 2 

        # Setting head
        self.cells[snake.body[0][0]][snake.body[0][1]] = 1
        
        # add food and full body
        

    def border_render(self, screen):
        for i in range(self.width+2):
            screen.addstr(0, i, '░')
            screen.addstr(self.height+1, i, '░')
        for j in range(1, self.height+1):
            screen.addstr(j, 0, '░')
            screen.addstr(j, self.width+1, '░')
        screen.addstr(0, 0, '')


    def render(self, screen, snake):
        
        self.set_field(snake)
        
        screen.clear()

        self.border_render(screen)

        for j in range(1, self.height+1):
            for i in range(1, self.width+1):
                screen.addstr(j, i, field_dictionary[self.cells[j][i]])
        
        # screen.refresh()


    def food_gen(self, snake):
        a = [randint(1, self.height), randint(1, self.width)]
        while a in snake.body:
            a = [randint(1, self.height), randint(1, self.width)]
        self.food = a


class Snake:
    def __init__(self, y, x, direction):
        self.body = [[y, x], [y, x-1], [y, x-2], [y-1, x-2]]
        self.direction = direction
        self.eaten_food = []

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
        if (self.direction == curses.KEY_UP) and (self.body[0][0] != 1):
            dy = -1
        elif (self.direction == curses.KEY_DOWN) and (self.body[0][0] != field.height):
            dy = 1
        elif (self.direction == curses.KEY_LEFT) and (self.body[0][1] != 1):
            dx = -1
        elif (self.direction == curses.KEY_RIGHT) and (self.body[0][1] != field.width):
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
            


def main(screen):

    screen.timeout(1)

    snake = Snake(5, 5, curses.KEY_RIGHT)
    field = Field(20, 20, snake)

    while True:
        key = screen.getch()

        if key in directions:
            snake.set_direction(key)
        
        snake.move(field)

        field.render(screen, snake)
        
        time.sleep(.1)

        

if __name__ == "__main__":
    curses.wrapper(main)