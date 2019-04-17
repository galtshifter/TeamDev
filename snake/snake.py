import curses
import time

direct = {'up': 'A',
          'down': 'B',
          'right': 'C',
          'left': 'D'}

dir = ['A', 'B', 'C', 'D']

class Field:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def render(self, screen, snake):
        screen.clear()
        screen.border(0) 
        screen.addstr(snake.y, snake.x, '#')
        screen.addstr(0, 0, '')


class Snake:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def set_direction(self, key):
        if key in dir:
            if (self.direction == direct['left']) and (key == direct['right']):
                return
            elif (self.direction == direct['right']) and (key == direct['left']):
                return
            elif (self.direction == direct['down']) and (key == direct['up']):
                return
            elif (self.direction == direct['up']) and (key == direct['down']):
                return
            self.direction = key
    
    def move(self, field):
        if (self.direction == direct['left']) and (self.x != 1):
            self.x -= 1
        elif (self.direction == direct['right']) and (self.x != field.width):
            self.x += 1
        elif (self.direction == direct['up']) and (self.y != 1):
            self.x -= 1
        elif (self.direction == direct['down']) and (self.x != field.width):
            self.y += 1
            


def main(screen):

    screen.timeout(-1)

    field = Field(20, 20)
    snake = Snake(2, 2, direct['right'])
    screen = curses.newwin(field.height+2, field.width+2, 0, 0)

    while True:
        key = screen.getkey()
        if key != -1:
            snake.set_direction(key)
        
        snake.move(field)

        field.render(screen, snake)
        #screen.addstr(7, 4, key)
        #screen.addstr(7, 4, str(snake.x))
        #screen.addstr(8, 4, str(snake.y))
    
        #time.sleep(1)

        

if __name__ == "__main__":
    curses.wrapper(main)