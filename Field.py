from helper import Player, Dir, BOARDSIZE, INFINITE

class Field():  
  def __init__(self, x, y):
    """Single field of the board.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
    """
    self.x = x
    self.y = y
    self.Walls = [False] * 4
    self.Walls[Dir.N] = False
    self.Walls[Dir.E] = False
    self.Walls[Dir.S] = False
    self.Walls[Dir.W] = False
    self.player = Player.Empty

    #a* part
    self.heuristic = [y, BOARDSIZE - y]
    self.nexts = [[Dir.N] if y != 0 else [],
                  [Dir.S] if y != BOARDSIZE else []]

    self.prevs = [[Dir.S] if y != BOARDSIZE else [],
                  [Dir.N] if y != 0 else []]
    self.disconnected = [False, False]

  def setPlayer(self, p = Player.Empty): self.player = p
  def getPlayer(self): return self.player
  
  def getPos(self): return (self.x, self.y)

  def getN(self): return (self.x, self.y - 1)
  def getE(self): return (self.x + 1, self.y) if not self.Walls[Dir.E] else self.getPos()
  def getS(self): return (self.x, self.y + 1) if not self.Walls[Dir.S] else self.getPos()
  def getW(self): return (self.x - 1, self.y) 

  def getWallDir(self, d):
    """Returns position of wall in direction d.

    Args:
        d (Dir): Direction of wanted wall

    Returns:
        (int, int): Position of wall
    """
    if d == Dir.N: return self.getN() if self.y != 0 else None
    if d == Dir.E: return self.getPos() if self.x != BOARDSIZE else None
    if d == Dir.S: return self.getPos() if self.y != BOARDSIZE else None
    if d == Dir.W: return self.getW() if self.x != 0 else None

  def getDir(self, d):
    """Returns position of object (Field/ Wall) in direction d.

    Args:
        d (Dir): Direction of wanted object

    Returns:
        (int, int): Position of object
    """
    if d == Dir.N: return self.getN() if self.y != 0 else None
    if d == Dir.E: return self.getE() if self.x != BOARDSIZE else None
    if d == Dir.S: return self.getS() if self.y != BOARDSIZE else None
    if d == Dir.W: return self.getW() if self.x != 0 else None

  def getWall(self, d): return self.Walls[d]
  def setWall(self, d, val=True): self.Walls[d] = val

  def getHeuristic(self, p): return self.heuristic[p]
  def setHeuristic(self, p, val): self.heuristic[p] = val

  def getNexts(self, p): return self.nexts[p]
  def addToNexts(self, p, d):
    if d not in self.nexts[p]:
      self.nexts[p].append(d)
  def removeFromNexts(self, p, d):
    if d in self.nexts[p]:
      self.nexts[p].remove(d)
      
  def getPrevs(self, p): return self.prevs[p]
  def addToPrevs(self, p, d):
    if d not in self.prevs[p]:
      self.prevs[p].append(d)
  def removeFromPrevs(self, p, d):
    if d in self.prevs[p]:
      self.prevs[p].remove(d)

  def getDisconnected(self, p): return self.disconnected[p]
  def setDisconnected(self, p, val): self.disconnected[p] = val

  def setUnreachable(self, p):
    """Sets Field to unreachable for player p.

    Args:
        p (Player): Player
    """
    self.setDisconnected(p, False)
    self.setHeuristic(p, INFINITE)