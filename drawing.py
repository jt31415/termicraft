import os
from config import *

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

def insert(text, x, y, lines):
    y -= 1
    lines[y] = lines[y][:x] + text + lines[y][x+len(text):]

def left(text, y, lines):
    y -= 1
    lines[y] =  text + lines[y][len(text):]

def right(text, y, lines):
    y -= 1
    lines[y] = lines[y][:-len(text)] + text

def center(text, y, lines, start=0, end=width):
    x = start+((end-start)-len(text))//2
    insert(text,x,y,lines)

def vline(start, end, x, lines):
    for i in range(start,end):
        insert('|',x,i,lines)

def draw_rect(rect, lines):
    insert('┏'+'━'*(rect[2]-2)+'┓',rect[0],rect[1],lines)           # top
    vline(rect[1]+1, rect[1]+rect[3]-1, rect[0], lines)             # left
    vline(rect[1]+1, rect[1]+rect[3]-1, rect[0] + rect[2]-1, lines) # right
    insert('┗'+'━'*(rect[2]-2)+'┛',rect[0],rect[1]+rect[3]-1,lines) # bottom

def inv_slot(x, y, stack, lines):
    draw_rect([x,y,6,3],lines)

    if stack:
        insert(str(stack.amount).rjust(2), x+4, y+3, lines)
    else:
        insert('  ', x+4, y+2, lines)