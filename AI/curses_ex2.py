from curses import wrapper,newpad

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    pad = newpad(100, 100)
    for y in range(0, 99):
        for x in range(0, 99):
            pad.addch(y,x, ord('a') + (x*x+y*y) % 26)
#    for i in range(0, 11):
#        v = i-10
#        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))
    pad.refresh( 0,0, 5,5, 20,75)

    #stdscr.refresh()
    stdscr.getkey()

wrapper(main)
