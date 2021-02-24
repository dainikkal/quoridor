from game.helper import Dir, BOARDSIZE, Orientation

class WallConnector():
  def __init__(self, x, y):
    #TODO WRITE PEP257
    self.posX = x
    self.posY = y
    self.count = 0

    self.walls = [None] * 4
    self.walls[Dir.N] = (x, y)
    self.walls[Dir.E] = (x+1, y)
    self.walls[Dir.S] = (x, y+1)
    self.walls[Dir.W] = (x, y)

    self.fields = {}
    self.fields[(Dir.N, Dir.E)] = (x+1, y)
    self.fields[(Dir.N, Dir.W)] = (x, y)
    self.fields[(Dir.E, Dir.S)] = (x+1, y+1)
    self.fields[(Dir.S, Dir.W)] = (x, y+1)
    
    self.Neighbours = [None] * 4
    if y != 0: self.Neighbours[Dir.N] = (x, y-1)
    if x != BOARDSIZE-1: self.Neighbours[Dir.E] = (x+1, y)
    if y != BOARDSIZE-1: self.Neighbours[Dir.S] = (x, y+1)
    if x != 0: self.Neighbours[Dir.W] = (x-1, y)

  def getCount(self): return self.count
  def incrCount(self): self.count +=1

  def getWalls(self): return self.walls

  def getFields(self, d1, d2):
    tmp = [d1, d2]
    tmp.sort()
    d_sort1, d_sort2 = tmp
    return self.fields[(d_sort1, d_sort2)]