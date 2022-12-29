from msvcrt import kbhit, getch
import colorama
import os

import random

from colors import *

def cls(n = 0):
    if n==0:
        os.system('cls')
    else:
        print('\b \b'*n,end='')

def overwrite(new, n):
    final = new
    len_new = len(new)
    
    if len_new < n:
        final += ' '*(n-len_new)
        length = n
    else:
        length = len_new

    final += '\b'*length

    print(final, end='')
    return length

def draw_screen():
    return ""

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