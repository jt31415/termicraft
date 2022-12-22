from msvcrt import kbhit, getch
import os

from colors import *

def cls(n = 0):
    if n==0:
        os.system('cls')
    else:
        print('\b \b'*n,end='')

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
    cls(n)
    print(final, end = "")
    n=len(final)