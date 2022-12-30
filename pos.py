from enums import *

class Pos:
    def __init__(self, x, y, z, world = world.OVERWORLD) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.world = world