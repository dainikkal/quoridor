from game.helper import Player, BOARDSIZE, BOARDSIZEMID

class PlayerHandler():
  def __init__(self):
    #TODO WRITE PEP257
    self.pos = [(BOARDSIZEMID, BOARDSIZE), (BOARDSIZEMID, 0)]
    self.path = [None] * 2

  def getPos(self, p): return self.pos[p] 
  def setPos(self, p, x, y): self.pos[p] = (x, y)

  def setPath(self, p, path): self.path[p] = path
  def getPath(self, p): return self.path[p]