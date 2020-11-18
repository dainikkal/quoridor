from helper import BOARDSIZEMID, Player, Dir, BOARDSIZE, INFINITE, mir, UpDown

#TO Include
# Pos X
# Pos Y
# Pathvector P1
# Pathvector P2
# is player on this?
# WallN, WallE, WallS, WallW
# can currentplayer move here?


class Field():
  
  def __init__(self, posX, posY):
    self.posX = posX
    self.posY = posY
    self.Walls = [False] * 4
    self.Walls[Dir.N] = False
    self.Walls[Dir.E] = False
    self.Walls[Dir.S] = False
    self.Walls[Dir.W] = False
    self.player = Player.Empty

    #a* part
    self.heuristic = [posY, BOARDSIZE - posY]
    #self.distToP = [INFINITE, INFINITE]
    self.nexts = [[Dir.N] if posY != 0 else [],
                  [Dir.S] if posY != BOARDSIZE else []]

    self.prevs = [[Dir.S] if posY != BOARDSIZE else [],
                  [Dir.N] if posY != 0 else []]
    self.inDisco = [False, False]

    pass

  def setPlayer(self, player = Player.Empty): 
    self.player = player
    #self.distToP[UpDown.U] = INFINITE if player != Player.P1 else 0
    #self.distToP[UpDown.D] = INFINITE if player != Player.P2 else 0
  
  def getPos(self): return (self.posX, self.posY)

  def getN(self): return (self.posX, self.posY - 1)
  def getE(self): return (self.posX + 1, self.posY) if not self.Walls[Dir.E] else (self.posX, self.posY)
  def getS(self): return (self.posX, self.posY + 1) if not self.Walls[Dir.S] else (self.posX, self.posY)
  def getW(self): return (self.posX - 1, self.posY) 

  def getDir(self, dir):
    if dir == Dir.N: return self.getN() if self.posY != 0 else None
    if dir == Dir.E: return self.getE() if self.posX != BOARDSIZE else None
    if dir == Dir.S: return self.getS() if self.posY != BOARDSIZE else None
    if dir == Dir.W: return self.getW() if self.posX != 0 else None

  def getWall(self, dir): return self.Walls[dir]
  def setWall(self, dir, fields, disco): 
    if dir in self.nexts[UpDown.U]:
      self.removeNextAddToDisco(UpDown.U, dir, fields, disco)
    if dir in self.nexts[UpDown.D]:
      self.removeNextAddToDisco(UpDown.D, dir, fields, disco)
    self.Walls[dir] = True

  def getHeuristic(self, i): return self.heuristic[i]
  def setHeuristic(self, i, h): self.heuristic[i] = h

  #def getDistToP(self, i): return self.distToP[i]
  #def setDistToP(self, i, dist): self.distToP[i] = dist

  def getNexts(self, i): return self.nexts[i]
  def addToNexts(self, i, dir):
    if dir not in self.nexts[i]:
      self.nexts[i].append(dir)
  def removeFromNexts(self, i, dir):
    if dir in self.nexts[i]:
      self.nexts[i].remove(dir)
      
  def getPrevs(self, i): return self.prevs[i]
  def addToPrevs(self, i, dir):
    if dir not in self.prevs[i]:
      self.prevs[i].append(dir)
  def removeFromPrevs(self, i, dir):
    if dir in self.prevs[i]:
      self.prevs[i].remove(dir)

  def getDisco(self, i): return self.inDisco[i]
  def setDisco(self, i, val): self.inDisco[i] = val

  def setUnreachable(self, i):
    self.setDisco(i, False)
    self.setHeuristic(i, INFINITE)
    #self.setDistToP(i, INFINITE)

  def removeNextAddToDisco(self, i, dir, fields, disco):
    if dir in self.nexts[i]:
      self.removeFromNexts(i, dir)
      posX, posY = self.getDir(dir)
      fields[posX][posY].removeFromPrevs(i, mir(dir))
      if not self.nexts[i]:
        self.setDisco(i, True)
        disco[i].append((self.getHeuristic(i), self.getPos()))