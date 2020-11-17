from helper import BOARDSIZE, Orientation, WallLegality, Dir

class WallHandler():
  
  def __init__(self):
    self.horizontal = [[False] * BOARDSIZE for _ in range(BOARDSIZE+1)]
    self.vertical = [[False] * (BOARDSIZE+1) for _ in range(BOARDSIZE)]
    self.connectors = [[0] * BOARDSIZE for _ in range(BOARDSIZE)]


  def getWallLegality(self, setX, setY):
    legality = 0x0
    
    if self.horizontal[setX][setY]: legality + WallLegality.WLocked
    if self.horizontal[setX+1][setY]: legality + WallLegality.ELocked
    if self.vertical[setX][setY]: legality + WallLegality.NLocked
    if self.vertical[setX][setY+1]: legality + WallLegality.SLocked

    return legality

  def setWallPair(self, fields, setX, setY, orientation, upDisco, downDisco):
    if orientation == Orientation.H: 
      self.__setHorizontalWall(fields, setX, setY, upDisco, downDisco)
      self.__setHorizontalWall(fields, setX+1, setY, upDisco, downDisco)

    if orientation == Orientation.V: 
      self.__setVerticalWall(fields, setX, setY, upDisco, downDisco)
      self.__setVerticalWall(fields, setX, setY+1, upDisco, downDisco)

  def __setHorizontalWall(self, fields, setX, setY, upDisco, downDisco):
    self.horizontal[setX][setY] = True

    fields[setX][setY].setWall(Dir.S, fields, upDisco, downDisco)
    fields[setX][setY+1].setWall(Dir.N, fields, upDisco, downDisco)

    if setX != 0: self.connectors[setX-1][setY] +=1
    if setX != (BOARDSIZE): self.connectors[setX][setY] +=1

  def __setVerticalWall(self, fields, setX, setY, upDisco, downDisco):
    self.vertical[setX][setY] = True

    fields[setX][setY].setWall(Dir.E, fields, upDisco, downDisco)
    fields[setX+1][setY].setWall(Dir.W, fields, upDisco, downDisco)

    if setY != 0: self.connectors[setX][setY-1] +=1
    if setY != (BOARDSIZE): self.connectors[setX][setY] +=1