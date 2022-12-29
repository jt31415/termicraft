from enum import Enum

class stateType(Enum):
    MAIN, INV, MENU = range(3)

class armType(Enum):
    NONE, LEATHER, IRON, GOLD, DIAMOND = range(5)

class mobType(Enum):
    ZOMBIE, SKELETON, SPIDER = range(3)