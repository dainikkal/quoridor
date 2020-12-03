from Wall import WallH, WallV
from WallConnector import WallConnector
from helper import BOARDSIZE, Dir, Orientation, Player

class WallHandler():  
  def __init__(self):
    """Handles all wall related game logic."""
    self.horizontal = [[WallH(x, y) for y in range(BOARDSIZE)] for x in range(BOARDSIZE+1)]
    self.vertical = [[WallV(x, y) for y in range(BOARDSIZE+1)] for x in range(BOARDSIZE)]
    self.connectors = [[WallConnector(x, y) for y in range(BOARDSIZE)] for x in range(BOARDSIZE)]
    self.wallsOnPath = {}
    self.initWallOnPath()

  def getConnectorWalls(self, x, y): return self.connectors[x][y].getWalls()
  
  def getConnectorCount(self, x, y):
    """Gets the count of an connector."""
    return self.connectors[x][y].getCount()

  def incrConnectorCount(self, x, y):
    """Increments the count of an connector by 1."""
    self.connectors[x][y].incrCount()

  def getConnectorField(self, x, y, d1, d2): return self.connectors[x][y].getFields(d1, d2)

  def getConnectorNeighbour(self, x, y, d): return self.connectors[x][y].Neighbours[d]

  def countLooseConnectorsInWallPair(self, x, y, o):
    """Count how many loose connector a wallpair has.

    Args:
        x (int): X-coordinate of wallpair
        y (int): Y-coordiante of wallpair
        o (Orientation): Orientation of wallpair

    Returns:
        int: count of loose connectors
    """
    midCon_count =  self.connectors[x][y].getCount()
    if o == Orientation.H:
      con1_pos = self.connectors[x][y].Neighbours[Dir.W]
      con2_pos = self.connectors[x][y].Neighbours[Dir.E]
    else:
      con1_pos = self.connectors[x][y].Neighbours[Dir.N]
      con2_pos = self.connectors[x][y].Neighbours[Dir.S]
    
    con1_x, con1_y = con1_pos if con1_pos else [0, 0]
    con2_x, con2_y = con2_pos if con2_pos else [0, 0]
    con1_count = self.connectors[con1_x][con1_y].getCount() if con1_pos else 3
    con2_count = self.connectors[con2_x][con2_y].getCount() if con2_pos else 3

    return [con1_count, midCon_count, con2_count].count(0)

  def setWall(self, x, y, o):
    """Updates the wall.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        o (Orientation): Orientation of the wall
    """
    if o == Orientation.H: self.horizontal[x][y].setWall()
    if o == Orientation.V: self.vertical[x][y].setWall()
  
  def isWallSet(self, x, y, o):
    """Returns if wall is set.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        o (Orientation): Orientation of the wall

    Returns:
        Bool: True if set, False if not
    """
    if o == Orientation.H: return self.horizontal[x][y].isWallSet()
    if o == Orientation.V: return self.vertical[x][y].isWallSet()

  def getWallPair(self, x, y, o):
    """Get wall positions based on connector position.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        o (Orientation): Orientation of the wall

    Returns:
        List: List [(x1, y1), (x2, y2)] position of the wall 
    """
    if o == Orientation.H: return [(x, y), (x+1, y)] 
    if o == Orientation.V: return [(x, y), (x, y+1)]

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