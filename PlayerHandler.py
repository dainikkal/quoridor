from helper import Player, BOARDSIZE, BOARDSIZEMID

class PlayerHandler():
  def __init__(self):
    #TODO WRITE PEP257
    self.pos = [None] * 2
    self.pos[Player.P1] = (BOARDSIZEMID, BOARDSIZE)
    self.pos[Player.P2] = (BOARDSIZEMID, 0)
    self.path = [None] * 2

  def getPos(self, p): return self.pos[p] 

  def setPath(self, p, path): self.path[p] = path
  def getPath(self, p): return self.path[p]