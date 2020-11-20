from PlayerHandler import PlayerHandler
from helper import BOARDSIZE, Dir, Orientation, Player
from FieldHandler import FieldHandler
from WallHandler import WallHandler

class Board():
  def __init__(self):
    """Object that handles all the game logic."""
    self.wh = WallHandler()
    self.fh = FieldHandler()
    self.ph = PlayerHandler()
    self.__updatePlayerPaths()

  def checkWallSetable(self, x, y, orientation):
    count = self.wh.getConnectorCount(x, y)
    #TODO STUFF 


#######################################################################################################################
                                                    #SET WALL
##########################################################################################################################
  def setWall(self, x, y, o):
    """Set a Wall.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        o (Orientation): Orientation of the wall
    """
    self.__setWallPair(x, y, o)
    self.fh.reconnectDisconnectedFields(Player.P1)
    self.fh.reconnectDisconnectedFields(Player.P2)
    self.__updatePlayerPaths()


  def __setWallPair(self, x, y, o):
    """Sets a pair wallspieces. 

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        o (Orientation): Orientation of the wall
    """
    if o == Orientation.H: 
      self.__setHorizontalWall(x, y)
      self.__setHorizontalWall(x+1, y)

    if o == Orientation.V: 
      self.__setVerticalWall(x, y)
      self.__setVerticalWall(x, y+1)

  def __setHorizontalWall(self, x, y):
    """Sets a horizontal wall.

    Args:
        x (int): X-Coordinate
        y (int): Y-Coordinate
    """
    self.wh.setWall(x, y, Orientation.H)

    self.fh.removeNextAndSetWall(x, y, Dir.S)
    self.fh.removeNextAndSetWall(x, y+1, Dir.N)
    
    if x != 0: self.wh.incrConnectorCount(x-1, y)
    if x != BOARDSIZE: self.wh.incrConnectorCount(x, y)

  def __setVerticalWall(self, x, y):
    """Set a vertical wall.

    Args:
        x (int): X-Coordinate
        y (int): Y-Coordinate
    """
    self.wh.setWall(x, y, Orientation.V)

    self.fh.removeNextAndSetWall(x, y, Dir.E)
    self.fh.removeNextAndSetWall(x+1, y, Dir.W)

    if y != 0: self.wh.incrConnectorCount(x, y-1)
    if y != BOARDSIZE: self.wh.incrConnectorCount(x, y)



##########################################################################################################################
                                                    #PLAYER PATH STUFF
##########################################################################################################################

  def __updatePlayerPaths(self):
    """Updates the paths of each player."""
    for p in range(2):
      x, y = self.ph.getPos(p)
      p_path = self.fh.findPaths(x, y, p)
      self.ph.setPath(p, p_path)

  def doesPlayerPathCrossWall(self, i, x, y, path):
    #TODO STILL IN WORK
    for p in range(2):
      for d, (x, y) in path[p]:
        if i == Orientation.H and (d == Dir.W or d == Dir.E): continue
        if i == Orientation.V and (d == Dir.N or d == Dir.S): continue
        if self.fh.getWallDir(x, y, d) == (self.posX, self.posY): return True



##########################################################################################################################
                                                    #DEBUG METHODS
##########################################################################################################################

  def debug_PrintInformation(self, myLambda, *args):
    #TODO MOVE TO FIELDHANDLER
    for y in range(BOARDSIZE+1):
      s = ""
      for x in range(BOARDSIZE+1):
        s += str(myLambda(self.fh.fields[x][y], *args)) + " "
      print(s)
