from msvcrt import kbhit, getch
import colorama
import os

import random

from colors import *

from enums import *

size=width,height=(100,30)

class Mob:
    def __init__(self, type: int, arm: list[int]) -> None:
        self.type = type
        self.arm = arm

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

def insert(text, where, line):
    return line[:where] + text + line[where+len(text):]

def left(text, line):
    return text + line[len(text):]

def right(text, line):
    return line[:-len(text)] + text

def center(text, line, start=0, end=width):
    where = start+((end-start)-len(text))//2
    return insert(text,where,line)

def vline(start, end, x, lines):
    for i in range(start,end):
        lines[i] = insert('|',x,lines[i])

def draw_screen():
    lines = [' '*width for i in range(height)]

    if state==stateType.MAIN:

        # fps
        lines[0] = left(f'FPS:{fps:.2f}',lines[0])

        # action
        lines[0] = center("Breaking stone",lines[0])
        lines[1] = left('  [',lines[1])
        lines[1] = right(']  ',lines[1])
        lines[1] = insert('#'*int(progress/100*(width-6)),3,lines[1])
        lines[1] = center(str(int(progress))+"%",lines[1])

        # environment and mobs headers
        lines[2] = center('Environment',lines[2],end=width//2)
        lines[2] = center('Mobs',       lines[2],start=width//2)

        # seperator
        vline(2,23,width//2,lines)

        # actions
        lines[3] = left('  b - Dig Down | B - Build up',lines[3])
        i = 5
        for action in actions:
            lines[i] = left(f'  {action[0]} - {action[1]}',lines[i])
            i+=2

        # mobs
        i = 3
        for mob in mobs:
            name = {mobType.ZOMBIE:'Zombie',mobType.SKELETON:'Skeleton',mobType.SPIDER:'Spider'}[mob[1].type]
            arm_names = [{armType.NONE:'NONE',armType.LEATHER:'LTHR',armType.IRON:'IRON',armType.GOLD:'GOLD',armType.DIAMOND:'DMND'}[j] for j in mob[1].arm]

            lines[i] = insert(f'{mob[0]} - {name}',width//2+3,lines[i])
            lines[i+1] = insert(f'Armor: {", ".join(arm_names)}',width//2+7,lines[i+1])
            i+=3


        for y, line in enumerate(lines):

            for x, char in enumerate(lines[y]):
                pass

    return "\n".join(lines)

state = stateType.MAIN

# example vars
fps = 60.0
progress = 50.0
actions = [['q','Break log'],['1','Break leaves'],['2','Break grass block (b)'],['u','Use chest'],['x','Build Nether Portal'],['3','Build Shelter']]
mobs = [['f',Mob(mobType.ZOMBIE, [armType.NONE, armType.LEATHER, armType.NONE, armType.IRON])],
['4',Mob(mobType.ZOMBIE, [armType.DIAMOND, armType.DIAMOND, armType.NONE, armType.NONE])]]

cls()
print('\033[?25l',end='') # hide cursor

n=0
running=True
while running:
    
    if kbhit():
        key = getch()
        try:
            key = key.decode()
        except:
            pass

        if key=='q':
            print('\033[?25h', end="")
            running=False

    final = draw_screen()
    n = overwrite(final, n)