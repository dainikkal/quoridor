from helper import BOARDSIZEMID, Player, Dir, BOARDSIZE, INFINITE, mir

#TO Include
# Pos X
# Pos Y
# Pathvector P1
# Pathvector P2
# is player on this?
# WallN, WallE, WallS, WallW
# can currentplayer move here?


class Field():
  
  def __init__(self, posX, posY, player = Player.Empty):
    self.posX = posX
    self.posY = posY
    self.Walls = [False] * 4
    self.Walls[Dir.N] = False
    self.Walls[Dir.E] = False
    self.Walls[Dir.S] = False
    self.Walls[Dir.W] = False
    self.setPlayer(player)
    #a* part
    #player1towardstop
    self.up_heuristic =  posY;
    self.up_distToP = INFINITE if player != Player.P1 else 0
    self.up_nexts = [Dir.N] if posY != 0 else []
    self.up_prevs = [Dir.S] if posY != BOARDSIZE else []
    self.up_inDisco = False
    pass

  def setPlayer(self, player = Player.Empty): 
    self.player = player
    self.up_distToP = INFINITE if player != Player.P1 else 0
  
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
  def setWall(self, dir, fields, upDisco, downDisco): 
    if dir in self.up_nexts:
      self.removeUpNextAddToUpDisco(dir, fields, upDisco)
    self.Walls[dir] = True

  #A* player 1 stuff
  def getUpHeuristic(self): return self.up_heuristic
  def setUpHeuristic(self, h): self.up_heuristic = h

  def getUpDistToP(self): return self.up_distToP
  def setUpDistToP(self, dist): self.up_distToP = dist

  def getUpNexts(self): return self.up_nexts
  def addToUpNexts(self, dir): 
    if dir not in self.up_nexts:
      self.up_nexts.append(dir)
  def removeFromUpNexts(self, dir): 
    if dir in self.up_nexts:
      self.up_nexts.remove(dir) 
      
  def getUpPrevs(self): return self.up_prevs
  def addToUpPrevs(self, dir): 
    if dir not in self.up_prevs:
      self.up_prevs.append(dir)
  def removeFromUpPrevs(self, dir): 
    if dir in self.up_prevs:
      self.up_prevs.remove(dir)

  def getUpDisco(self): return self.up_inDisco
  def setUpDisco(self, val): self.up_inDisco = val

  def setUpUnreachable(self): 
    self.setUpDisco(False)
    self.setUpHeuristic(INFINITE)
  
  def removeUpNextAddToUpDisco(self, dir, fields, upDisco):    
    if dir in self.up_nexts:
      self.removeFromUpNexts(dir)
      posX, posY = self.getDir(dir)
      fields[posX][posY].removeFromUpPrevs(mir(dir))
      if not self.up_nexts: #if empty
        self.setUpDisco(True)
        upDisco.append((self.getUpHeuristic(), self.getPos()))
