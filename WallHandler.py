from Wall import WallH, WallV
from WallConnector import WallConnector
from helper import BOARDSIZE, Orientation

class WallHandler():  
  def __init__(self):
    """Handles all wall related game logic."""
    self.horizontal = [[WallH(x,y) for y in range(BOARDSIZE)] for x in range(BOARDSIZE+1)]
    self.vertical = [[WallV(x,y) for y in range(BOARDSIZE+1)] for x in range(BOARDSIZE)]
    self.connectors = [[WallConnector(x,y) for y in range(BOARDSIZE)] for x in range(BOARDSIZE)]

  def getConnectorCount(self, x, y):
    """Gets the count of an connector."""
    return self.connectors[x][y].getCount()

  def incrConnectorCount(self, x, y):
    """Increments the count of an connector by 1."""
    self.connectors[x][y].incrCount()

  def setWall(self, x, y, o):
    """Updates the wall.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        o (Orientation): Orientation of the wall
    """
    if o == Orientation.H:
      self.horizontal[x][y].setWall()
    if o == Orientation.V:
      self.vertical[x][y].setWall()