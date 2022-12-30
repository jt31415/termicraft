from msvcrt import kbhit, getch
import colorama

import random, time

from colors import *

from enums import *
from pos import Pos
from drawing import *
from config import *


class Player:
    def __init__(self):
        self.hotbar: list[Stack] = [None for i in range(10)]
        self.pos: Pos = Pos(0,0,0)
        self.biome = what_biome(self.pos)
    def move(self, dir):
        # moving

        # change biome
        self.biome = what_biome(self.pos)

class Stack:
    def __init__(self, name: int, item_type: int, amount:int = 1, data: dict = {}):
        self.name = name
        self.item_type = item_type
        self.amount = amount
        self.data = data

class Mob:
    def __init__(self, type: int, arm: list[int]):
        self.type = type
        self.arm = arm

def what_biome(pos: Pos):
    pass

def draw_screen():
    lines = [' '*width for i in range(height)]

    if state==stateType.MAIN:

        # fps
        left(f'FPS:{fps:.2f}',1,lines)

        # action
        center("Breaking stone",1,lines)
        left('  [',2,lines)
        right(']  ',2,lines)
        insert('#'*int(progress/100*(width-6)),3,2,lines)
        center(str(int(progress))+"%",2,lines)

        # environment and mobs headers
        center('Environment',3,lines,end=width//2)
        center('Mobs',       3,lines,start=width//2)

        # seperator
        vline(3,24,width//2,lines)

        # actions
        left('  b - Dig Down | B - Build up',4,lines)
        i = 6
        for action in actions:
            left(f'  {action[0]} - {action[1]}',i,lines)
            i+=2

        # mobs
        i = 4
        for mob in mobs:
            name = {mobType.ZOMBIE:'Zombie',mobType.SKELETON:'Skeleton',mobType.SPIDER:'Spider'}[mob[1].type]
            arm_names = [{armType.NONE:'NONE',armType.LEATHER:'LTHR',armType.IRON:'IRON',armType.GOLD:'GOLD',armType.DIAMOND:'DMND'}[j] for j in mob[1].arm]

            insert(f'{mob[0]} - {name}',width//2+3,i,lines)
            insert(f'Armor: {", ".join(arm_names)}',width//2+7,i+1,lines)
            i+=3

        # position rect
        draw_rect([4,19,33,5],lines)
        coords = main_player.pos
        biome = main_player.biome
        world_name = {world.OVERWORLD: 'Overworld', world.NETHER: 'Nether', world.END: 'End'}[main_player.pos.world]
        insert(f'Coords: {coords.x} / {coords.y} / {coords.z}', 6, 20, lines)
        insert(f'Biome: {biome}', 6, 21, lines)
        insert(f'World: {world_name}', 6, 22, lines)

        #hotbar
        for i, slot in enumerate(main_player.hotbar):
            inv_slot(7*i+2, 28, slot, lines)


        for y, line in enumerate(lines):

            for x, char in enumerate(lines[y]):
                pass
    
    lines.extend(debug) # DEBUG
    return "\n".join(lines)

state = stateType.MAIN
main_player = Player()

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

    debug[1] = f'avg_time: {avg_time:.6f}, potential: {1/avg_time:.6f}, to_sleep: {to_sleep:.6f}, start - end: {start-end:.6f}, (start-end)/to_sleep: {(start-end)/to_sleep:.6f}, start - last_start: {start-last_start}'

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