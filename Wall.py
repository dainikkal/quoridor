from helper import BOARDSIZE, LeftRight, Orientation, Dir, UpDown

class Wall():
  def __init__(self, orientation, x, y):
    #TODO WRITE PEP257
    self.type =  orientation
    self.posX = x
    self.posY = y
    self.set = False
    self.touchesBorder = False
    self.connectors = [None] * 2
    self.extensions = [None] * 2
    self.arms = [None] * 2
    pass

  def setWall(self, val=True): self.set = True
  def isWallSet(self): return self.set
  def doesWalltouchBorder(self): return self.touchesBorder

class WallH(Wall):
  def __init__(self, x, y):
    #TODO WRITE PEP257
    super().__init__(Orientation.H, x, y)
    if x != 0:
      self.connectors[LeftRight.L] = (x-1, y)
      self.extensions[LeftRight.L] = (x-1, y)
      self.arms[LeftRight.L] = ((x-1, y), (x-1, y+1))
    else: self.touchesBorder = True
            
    if x != BOARDSIZE:
      self.connectors[LeftRight.R] = (x, y)
      self.extensions[LeftRight.R] = (x+1, y)
      self.arms[LeftRight.R] = ((x, y), (x, y+1))
    else: self.touchesBorder = True
    pass


class WallV(Wall):
  def __init__(self, x, y):
    #TODO WRITE PEP257
    super().__init__(Orientation.V, x, y)
    if y != 0:
      self.connectors[UpDown.U] = (x, y-1)
      self.extensions[UpDown.U] = (x, y-1)
      self.arms[UpDown.U] = ((x, y-1), (x+1, y-1))
    else: self.touchesBorder = True

    if y != BOARDSIZE:
      self.connectors[UpDown.D] = (x, y) 
      self.extensions[UpDown.D] = (x, y+1)
      self.arms[UpDown.D] = ((x, y), (x+1, y))
    else: self.touchesBorder = True
    pass