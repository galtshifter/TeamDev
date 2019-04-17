import curses
import time

directions = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]

class Field:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def border_render(self, screen):
        for i in range(self.width+2):
            screen.addstr(0, i, '░')
            screen.addstr(self.height+1, i, '░')
        for j in range(1, self.height+1):
            screen.addstr(j, 0, '░')
            screen.addstr(j, self.width+1, '░')
        screen.addstr(0, 0, '')

    def render(self, screen, snake):
        for i in range(1, self.width):
            for j in range(1, self.height):
                screen.addstr(j, i, ' ')
        
        screen.addstr(snake.y, snake.x, '#')
        screen.addstr(0, 0, '')
        screen.refresh()


class Snake:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

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
        if (self.direction == curses.KEY_LEFT) and (self.x != 1):
            self.x -= 1
        elif (self.direction == curses.KEY_RIGHT) and (self.x != field.width):
            self.x += 1
        elif (self.direction == curses.KEY_UP) and (self.y != 1):
            self.y -= 1
        elif (self.direction == curses.KEY_DOWN) and (self.y != field.height):
            self.y += 1
            


def main(screen):

    screen.timeout(1)

    field = Field(20, 20)
    snake = Snake(2, 2, curses.KEY_RIGHT)

    field.border_render(screen)

    while True:
        key = screen.getch()

        if key in directions:
            snake.set_direction(key)
        
        snake.move(field)

        field.render(screen, snake)
        
        time.sleep(.5)

        

if __name__ == "__main__":
    curses.wrapper(main)