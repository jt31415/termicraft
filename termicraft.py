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

def insert(text, x, y, lines):
    lines[y] = lines[y][:x] + text + lines[y][x+len(text):]

def left(text, y, lines):
    lines[y] =  text + lines[y][len(text):]

def right(text, y, lines):
    lines[y] = lines[y][:-len(text)] + text

def center(text, y, lines, start=0, end=width):
    x = start+((end-start)-len(text))//2
    insert(text,x,y,lines)

def vline(start, end, x, lines):
    for i in range(start,end):
        insert('|',x,i,lines)

def draw_screen():
    lines = [' '*width for i in range(height)]

    if state==stateType.MAIN:

        # fps
        left(f'FPS:{fps:.2f}',0,lines)

        # action
        center("Breaking stone",0,lines)
        left('  [',1,lines)
        right(']  ',1,lines)
        insert('#'*int(progress/100*(width-6)),3,1,lines)
        center(str(int(progress))+"%",1,lines)

        # environment and mobs headers
        center('Environment',2,lines,end=width//2)
        center('Mobs',       2,lines,start=width//2)

        # seperator
        vline(2,23,width//2,lines)

        # actions
        left('  b - Dig Down | B - Build up',3,lines)
        i = 5
        for action in actions:
            left(f'  {action[0]} - {action[1]}',i,lines)
            i+=2

        # mobs
        i = 3
        for mob in mobs:
            name = {mobType.ZOMBIE:'Zombie',mobType.SKELETON:'Skeleton',mobType.SPIDER:'Spider'}[mob[1].type]
            arm_names = [{armType.NONE:'NONE',armType.LEATHER:'LTHR',armType.IRON:'IRON',armType.GOLD:'GOLD',armType.DIAMOND:'DMND'}[j] for j in mob[1].arm]

            insert(f'{mob[0]} - {name}',width//2+3,i,lines)
            insert(f'Armor: {", ".join(arm_names)}',width//2+7,i+1,lines)
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