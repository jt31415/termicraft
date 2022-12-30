from msvcrt import kbhit, getch
import colorama
import os

import random, time

from colors import *

from enums import *

size=width,height=(100,30)
MAXFPS = 60.0
MINFRAMETIME = 1/MAXFPS
TIMESAMPLE = 5.0
FRAMESAMPLES = 100
ADJUST = 0.1 # to adjust to_sleep
MINSLEEPTIME = 0.0001

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

def draw_rect(rect, lines):
    insert('┏'+'━'*(rect[2]-2)+'┓',rect[0],rect[1]-1,lines)         # top
    vline(rect[1], rect[1]+rect[3]-2, rect[0], lines)               # left
    vline(rect[1], rect[1]+rect[3]-2, rect[0] + rect[2]-1, lines)   # right
    insert('┗'+'━'*(rect[2]-2)+'┛',rect[0],rect[1]+rect[3]-2,lines) # bottom

def inv_slot(x, y, lines):
    draw_rect([x,y,6,3],lines)

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

        # position rect
        draw_rect([4,19,33,5],lines)

        #hotbar
        inv_slot(3, 28, lines)


        for y, line in enumerate(lines):

            for x, char in enumerate(lines[y]):
                pass
    
    lines.extend(debug) # DEBUG
    return "\n".join(lines)

state = stateType.MAIN

debug = ['DEBUG','',''] # DEBUG

recent_frames = []
frame_times = [0 for i in range(FRAMESAMPLES)]

# place
start = time.perf_counter()
end = time.perf_counter()
to_sleep = MINSLEEPTIME

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

    last_start = start # last frame's start
    start = time.perf_counter()

    last_frame_time = end - last_start
    frame_times.append(last_frame_time); frame_times.pop(0)
    avg_time = sum(frame_times)/len(frame_times)

    adjust = (MINFRAMETIME - (start-last_start)) * ADJUST
    to_sleep = max(MINSLEEPTIME, to_sleep + adjust)

    debug[1] = f'avg_time: {avg_time:.6f}, to_sleep: {to_sleep:.6f}, start - end: {start-end:.6f}, (start-end)/to_sleep: {(start-end)/to_sleep:.6f}, start - last_start: {start-last_start}'

    # get fps
    recent_frames.append(start)
    recent_frames = [frame for frame in recent_frames if (start - frame) <= TIMESAMPLE]
    fps = len(recent_frames)/TIMESAMPLE
    
    if kbhit():
        key = getch()
        try:
            key = key.decode()
        except:
            pass

        if key=='q':
            print('\033[?25h', end="") # show cursor
            running=False

    final = draw_screen()
    n = overwrite(final, n)

    end = time.perf_counter()

    time.sleep(to_sleep) # account for going faster than max frame rate