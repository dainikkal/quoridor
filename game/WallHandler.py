from game.helper import BOARDSIZE, Dir, Orientation, Player

class WallHandler():  
  def __init__(self):
    """Handles all wall related game logic."""
    self.walls = {(x, y, o) : False for o in [Orientation.H, Orientation.V] for x in range(BOARDSIZE+1) for y in range(BOARDSIZE+1) \
                                    if (x != BOARDSIZE or o == Orientation.H) and (y != BOARDSIZE or o == Orientation.V)} 
    
    self.wallcenter = {(x, y) : 0 for x in range(BOARDSIZE) for y in range(BOARDSIZE)}

    self.wallsOnPath = {}
    self.initWallOnPath()

  def setWall(self, x, y, o, val=True): self.walls[(x, y, o)] = val  
  def isWallSet(self, x, y, o): return self.walls[(x, y, o)]

  def isCenterSet(self, x, y): return False if self.wallcenter[(x, y)] < 2 else True
  def getWallcenterCount(self, x, y): return self.wallcenter[(x, y)]
  def incrWallcenterCount(self, x, y, increment=1): self.wallcenter[(x, y)] += increment

  def countFreeCentersInWall(self, x, y, o):
    """Count how many free center a wall has.

    Args:
        x (int): X-coordinate of wallpair
        y (int): Y-coordiante of wallpair
        o (Orientation): Orientation of wallpair

    Returns:
        int: count of free Centers
    """
    midCon_count =  self.wallcenter[(x, y)]

    if o == Orientation.V:
      con1_pos = (x, y-1) if y != 0 else None
      con2_pos = (x, y+1) if y != BOARDSIZE-1 else None
    else:
      con1_pos = (x+1, y) if o == Orientation.H and x != BOARDSIZE-1 else None
      con2_pos = (x-1, y) if o == Orientation.H and x != 0 else None

    con1_count = self.wallcenter[con1_pos] if con1_pos else 3
    con2_count = self.wallcenter[con2_pos] if con2_pos else 3

    return [con1_count, midCon_count, con2_count].count(0)


  def initWallOnPath(self):
    """initializes wallsOnPath to map to False."""
    for p in [Player.P1, Player.P2]:
      for x in range(BOARDSIZE+1):
        for y in range(BOARDSIZE):
          self.wallsOnPath[(x, y, Orientation.H, p)] = False
      for x in range(BOARDSIZE):
        for y in range(BOARDSIZE+1):
          self.wallsOnPath[(x, y, Orientation.V, p)] = False

  def isWallOnPath(self, x, y, o, p): return self.wallsOnPath[(x, y, o, p)]
  def setWallOnPath(self, x, y, o, p, val=True): self.wallsOnPath[(x, y, o, p)] = val