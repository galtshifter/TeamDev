import snake as snk
import unittest
import random
import curses

N = 1000

class TestSnake(unittest.TestCase):

    def test_snake_set_direction(self):
        directions = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]
        snake = snk.Snake(5, 5, curses.KEY_RIGHT)

        for i in range(1000):
            key = directions[random.randint(0, 3)]
            right_direction = snake.direction
            snake.set_direction(key)

            if not((key == curses.KEY_LEFT and snake.direction == curses.KEY_RIGHT) or 
                (key == curses.KEY_RIGHT and snake.direction == curses.KEY_LEFT) or 
                (key == curses.KEY_UP and snake.direction == curses.KEY_DOWN) or
                (key == curses.KEY_DOWN and snake.direction == curses.KEY_UP)):
                right_direction = key

            self.assertEqual(snake.direction, right_direction, "set_direction is not working worng")


    def test_field_clear_field(self):
        snake = snk.Snake(5, 5, curses.KEY_RIGHT)
        field = snk.Field(20, 20, snake)

        right_cells = [[0 for i in range(field.width+2)] for j in range(field.height+2)]
        for j in range(field.height+2):
            right_cells[j][0] = -1
            right_cells[j][field.width+1] = -1
        for i in range(1, field.width+1):
            right_cells[0][i] = -1
            right_cells[field.height+1][i] = -1

        field.clear_field()

        self.assertEqual(field.cells, right_cells, "clear_field is working wrong")



if __name__ == '__main__':
    unittest.main()
