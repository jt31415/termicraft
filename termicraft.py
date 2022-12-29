from msvcrt import kbhit, getch
import colorama
import os

import random

from colors import *

size=width,height=(100,30)

def cls(n = 0):
    if n==0:
        os.system('cls')
    else:
        print('\b \b'*n,end='')

def cursor_to(x, y):
    print("\033[%d;%dH" % (y, x), end='')

def overwrite(new, n):
    final = new
    len_new = len(new)
    
    if len_new < n:
        final += ' '*(n-len_new)
        length = n
    else:
        length = len_new
    
    # move cursor back to the top left corner
    final += "\033[H"

    print(final, end='')
    return length

def left(text, line):
    return text + line[len(text):]

def right(text, line):
    return line[:-len(text)] + text

def center(text, line):
    where = (len(line)-len(text))//2
    return line[:where] + text + line[where+len(text):]


def draw_screen():
    lines = [' '*width for i in range(height)]

    if state==MAIN:        

        # fps
        lines[0] = left(f'FPS:{fps:.2f}',lines[0])

        # action
        lines[0] = center("Breaking stone",lines[0])

        for y, line in enumerate(lines):

            for x, char in enumerate(lines[y]):
                pass

    return "\n".join(lines)

MAIN, INV, MENU = range(3)
state = MAIN
fps = 60.0

cls()

n=0
running=True
while running:
    
    if kbhit():
        key = getch()
        try:
            key = key.decode()
        except:
            pass

    final = draw_screen()
    n = overwrite(final, n)