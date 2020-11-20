from helper import Dir, BOARDSIZE, Orientation

class WallConnector():
  def __init__(self, x, y):
    #TODO WRITE PEP257
    self.posX = x
    self.posY = y
    self.count = 0

    self.Walls = [None] * 4
    self.Walls[Dir.N] = (x, y)
    self.Walls[Dir.E] = (x+1, y)
    self.Walls[Dir.S] = (x, y+1)
    self.Walls[Dir.W] = (x, y)
    
    self.Neighbours = [None] * 4
    if y != 0: self.Neighbours[Dir.N] = (x, y)
    if x != BOARDSIZE-1: self.Neighbours[Dir.E] = (x+1, y)
    if y != BOARDSIZE-1: self.Neighbours[Dir.S] = (x, y+1)
    if x != 0: self.Neighbours[Dir.W] = (x, y)

  def getCount(self): return self.count
  def incrCount(self): self.count +=1

  def getSetAble(self, i, wallconnectors, walls, path, fields): #TOMOVE
    if self.count > 1: return False
    
    if i == Orientation.H:
      w_wall_x, w_wall_y = self.Walls[Dir.W]
      walls[i][w_wall_x][w_wall_y].doesPlayerPassPath(path, fields)

    if i == Orientation.H:
      if self.Neighbours[Dir.W] == None:
        w_count = 4
        w_border = True
      else:
        w_x, w_y = self.Neighbours[Dir.W]
        w_count = wallconnectors[w_x][w_y].getCount()
        w_border = False

      if w_count != 0 and self.count != 0: #Blockade Check w-m
        pass

      if w_count == 0 and self.count == 0: return True
      if self.Neighbours[Dir.E] == None:
        e_count = 4
        e_border = True
      else:
        e_x, e_y = self.Neighbours[Dir.E]
        e_count = wallconnectors[e_x][e_y].getCount()
        e_border = False
      if e_count == 0: return True #either 2 are count 0 so its fine, or

    return True