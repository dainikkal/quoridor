from typing import List
from Path import Path
from PlayerHandler import PlayerHandler
from helper import BOARDSIZE, CycledetectionRetVal, Dir, Orientation, Player, mir
from FieldHandler import FieldHandler
from WallHandler import WallHandler

class Board():
  def __init__(self):
    """Object that handles all the game logic."""
    self.wh = WallHandler()
    self.fh = FieldHandler()
    self.ph = PlayerHandler()
    self.updatePlayerPaths()
    #helper variables 
    self.checkedCon = []
    self.currentBorderConnector = []
    self.cycleGoal = []

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
    self.setWallPair(x, y, o)
    self.fh.reconnectDisconnectedFields(Player.P1)
    self.fh.reconnectDisconnectedFields(Player.P2)
    self.updatePlayerPaths()


  def setWallPair(self, x, y, o):
    """Sets a pair wallspieces. 

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        o (Orientation): Orientation of the wall
    """
    if o == Orientation.H: 
      self.setHorizontalWall(x, y)
      self.setHorizontalWall(x+1, y)

    if o == Orientation.V: 
      self.setVerticalWall(x, y)
      self.setVerticalWall(x, y+1)

  def setHorizontalWall(self, x, y):
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

  def setVerticalWall(self, x, y):
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
                                                      #MOVE PLAYER
##########################################################################################################################
  def movePlayer(self, p, d):
    """Move player to direction.

    Args:
        p (Player): Player
        d (Dir): Direction
    """
    #Assumption viable direction
    x, y = self.ph.getPos(p)
    new_x, new_y = self.fh.movePlayer(x, y, p, d)
    self.ph.setPos(p, new_x, new_y)

    self.updatePlayerPaths()

##########################################################################################################################
                                                    #PLAYER PATH STUFF #MAYBE UNNECESSARYgetPath
##########################################################################################################################
  def updatePlayerPaths(self):
    """Updates the paths of each player."""
    self.wh.initWallOnPath()
    for p in range(2):
      x, y = self.ph.getPos(p)
      p_path = self.findPaths(x, y, p)
      self.ph.setPath(p, p_path)

  def findPaths(self, x, y, p):
    """Finds Path from starting field position to Goal.

    Args:
        x (int): X-coordinate Start
        y (int): Y-coordinate Start
        p (Player): Player

    Returns:
        Path: Path tree
    """
    nexts = self.fh.getNexts(x, y, p)

    if not nexts: return Path(x, y, True)

    path = Path(x, y)
    for d in nexts:
      n_x, n_y = self.fh.getDir(x, y, d)
      subpath = self.findPaths(n_x, n_y,  p)
      path.subPath[d] = subpath
      nw_x, nw_y = self.fh.getDir(x, y, d)
      if d in [Dir.N, Dir.S]: self.wh.setWallOnPath(nw_x, nw_y, Orientation.H, p)
      if d in [Dir.E, Dir.W]: self.wh.setWallOnPath(nw_x, nw_y, Orientation.V, p)
    return path

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

##########################################################################################################################
                                                      #TO SORT
##########################################################################################################################
  def getAllSetableWalls(self):
    return [(x, y, o) for x in range(BOARDSIZE) for y in range(BOARDSIZE) for o in [Orientation.H, Orientation.V] if self.isWallSetable(x, y, o)]

  def isWallSetable(self, x, y, o):
    midCon_count =  self.wh.getConnectorCount(x, y)
    #already locked connector
    if midCon_count > 1: return False
    
    (w1_x, w1_y), (w2_x, w2_y) = self.wh.getWallPair(x, y, o)    
    #If midconnector has 1 wall that is not on that orientation
    if midCon_count == 1 and (self.wh.isWallSet(w1_x, w1_y, o) or self.wh.isWallSet(w2_x, w2_y, o)): return False

    if o == Orientation.H:
      con1_pos = self.wh.getConnectorNeighbour(x, y, Dir.W)
      con2_pos = self.wh.getConnectorNeighbour(x, y, Dir.E)
    else:
      con1_pos = self.wh.getConnectorNeighbour(x, y, Dir.N)
      con2_pos = self.wh.getConnectorNeighbour(x, y, Dir.S)
    
    con1_x, con1_y = con1_pos if con1_pos else [0, 0]
    con2_x, con2_y = con2_pos if con2_pos else [0, 0]
    con1_count = self.wh.getConnectorCount(con1_x, con1_y) if con1_pos else 3
    con2_count = self.wh.getConnectorCount(con2_x, con2_y) if con2_pos else 3
    
    #only 0 or 1 Connector is connected to something
    if [con1_count, midCon_count, con2_count].count(0) in [2,3]: return True

    self.temporarySetWallInField(x, y, o, True)
    p1_pos = self.ph.getPos(Player.P1)
    p2_pos = self.ph.getPos(Player.P2)
    playersReachGoal = self.fh.doPlayersReachGoal(p1_pos, p2_pos)
    self.temporarySetWallInField(x, y, o, False)

    return playersReachGoal

  def temporarySetWallInField(self, x, y, o, val):
    dirs = []
    if Orientation.H == o:
      dirs = [(Dir.N, Dir.E, Dir.S), (Dir.N, Dir.W, Dir.S), (Dir.S, Dir.E, Dir.N), (Dir.S, Dir.W, Dir.N)]
    if Orientation.V == o: 
      dirs = [(Dir.E, Dir.N, Dir.W), (Dir.E, Dir.S, Dir.W), (Dir.W, Dir.N, Dir.E), (Dir.W, Dir.S, Dir.E)]
    for d1, d2, d3 in dirs:
      f_x, f_y = self.wh.getConnectorField(x, y, d1, d2)
      self.fh.setWall(f_x, f_y, d3, val)