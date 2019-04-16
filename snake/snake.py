import curses

def main(screen):

    screen.timeout(-1)

    begin_x = 1
    begin_y = 1
    height = 20
    width = 20

    try:
        key = 'x'
        screen = curses.newwin(height+2, width+2, begin_x, begin_y)
        screen.border(0) 
        cur_x = 1
        cur_y = 1
        screen.addstr(cur_x, cur_y, '')   

        while key != ord('\n'):    
            key = screen.getch()  
            if key != -1:    

                if (key == 68) and (cur_x != 1):
                    cur_x -= 1
                elif (key == 67) and (cur_x != width):
                    cur_x += 1
                elif (key == 65) and (cur_y != 1):
                    cur_y -= 1
                elif (key == 66) and (cur_y != height):
                    cur_y += 1
                screen.addstr(cur_y, cur_x, '#')   
                screen.refresh

    except Exception:
        print(Exception)
    
    finally:
        return

if __name__ == "__main__":
     curses.wrapper(main)