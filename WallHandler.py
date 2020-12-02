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

  def doesWallTouchBorder(self, x, y, o):
    """Returns if wall touches game Border

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        o (Orientation): Orientation of the wall

    Returns:
        Bool: True if yes, False if no
    """
    if o == Orientation.H: return self.horizontal[x][y].doesWalltouchBorder()
    if o == Orientation.V: return self.vertical[x][y].doesWalltouchBorder()

  def getWallPair(self, x, y, o):
    """Get wall positions based on connector position  

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