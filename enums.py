from enum import Enum

class stateType(Enum):
    MAIN, INV, MENU = range(3)

class armType(Enum):
    NONE, LEATHER, IRON, GOLD, DIAMOND = range(5)

class mobType(Enum):
    ZOMBIE, SKELETON, SPIDER = range(3)

class itemName(Enum):
    GRASS, CHEST, DIRT = range(3)

class itemType(Enum):
    BLOCK, SWORD, CHEST = range(3)

class world(Enum):
    OVERWORLD, NETHER, END = range(3)