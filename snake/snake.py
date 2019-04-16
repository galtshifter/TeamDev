import curses

direction = {'up': 65,
             'down': 66,
             'left': 67,
             'right': 68}

class Field:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def render(self, screen, snake):
        screen.clear
        screen.addstr(snake.y, snake.x, '#')


class Snake:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def set_direction(self, key):
        if (self.direction == direction['left']) and (key == direction['right']):
            return
        elif (self.direction == direction['right']) and (key == direction['left']):
            return
        elif (self.direction == direction['down']) and (key == direction['up']):
            return
        elif (self.direction == direction['up']) and (key == direction['down']):
            return
        self.direction = direction
    
    def move(self):
        return


def main():
    try:
        field = Field(20, 20)
        snake = Snake(2, 2, direction['right'])
        screen = curses.newwin(field.height+2, field.width+2, 0, 0)
        screen.timeout(0)
        screen.border(0) 

    
        while True:
            key = screen.getch()
            if key != -1:
                snake.set_direction(key)
            
            snake.move

            field.render(screen, snake)
        
            screen.sleep(1)
    finally:
        curses.endwin()
        

if __name__ == "__main__":
    main()