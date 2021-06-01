from game.helper import Player, BOARDSIZE, BOARDSIZEMID


class PlayerHandler:
    def __init__(self, p1_x=BOARDSIZEMID, p1_y=BOARDSIZE, p2_x=BOARDSIZEMID, p2_y=0):
        # TODO WRITE PEP257
        self.pos = [(p1_x, p1_y), (p2_x, p2_y)]
        self.path = [None] * 2

    def getPos(self, p):
        return self.pos[p]

    def setPos(self, p, x, y):
        self.pos[p] = (x, y)

    def setPath(self, p, path):
        self.path[p] = path

    def getPath(self, p):
        return self.path[p]
