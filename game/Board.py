from game.Playerstate import Playerstate
from game.Path import Path
from game.PlayerHandler import PlayerHandler
from game.helper import BOARDSIZE, Dir, INFINITE, MINUSINFINITE, Orientation, Player, mir
from game.FieldHandler import FieldHandler
from game.WallHandler import WallHandler

class Board():
  def __init__(self):
    """Object that handles all the game logic."""
    self.wh = WallHandler()
    self.fh = FieldHandler()
    self.ph = PlayerHandler()
    self.updatePlayerPaths()

#######################################################################################################################
                                                    #SET WALL
##########################################################################################################################
  def setWall(self, x, y, o, val=True):
    """Sets a wall pair and updates information.

    Args:
        x (int): X-coordinate of the wallpair
        y (int): Y-coordinate of the wallpair
        o (Orientation): Orientation of the wall
        val (bool): if the wall is to be set or unset
    """
    self.setWallPair(x, y, o, val)
    self.fh.reconnectDisconnectedFields(Player.P1)
    self.fh.reconnectDisconnectedFields(Player.P2)
    self.updatePlayerPaths()


  def setWallPair(self, x, y, o, val=True):
    """Sets a wallpair.

    Args:
        x (int): X-coordinate of the wallpair
        y (int): Y-coordinate of the wallpair
        o (Orientation): Orientation of the wall
        val (bool): if the wall is to be set or unset
    """
    if o == Orientation.H: 
      self.setHorizontalWall(x, y, val)
      self.setHorizontalWall(x+1, y, val)

    if o == Orientation.V: 
      self.setVerticalWall(x, y, val)
      self.setVerticalWall(x, y+1, val)

  def setHorizontalWall(self, x, y, val=True):
    """Sets a horizontal wall.

    Args:
        x (int): X-Coordinate
        y (int): Y-Coordinate
        val (bool): if the wall is to be set or unset
    """
    self.wh.setWall(x, y, Orientation.H, val)

    self.fh.removeNextAndSetWall(x, y, Dir.S)
    self.fh.removeNextAndSetWall(x, y+1, Dir.N)

    increment = 1 if val else -1
    if x != 0: self.wh.incrWallcenterCount(x-1, y, increment)
    if x != BOARDSIZE: self.wh.incrWallcenterCount(x, y, increment)

  def setVerticalWall(self, x, y, val=True):
    """Sets a vertical wall.

    Args:
        x (int): X-Coordinate
        y (int): Y-Coordinate
        val (bool): if the wall is to be set or unset
    """
    self.wh.setWall(x, y, Orientation.V, val)

    self.fh.removeNextAndSetWall(x, y, Dir.E)
    self.fh.removeNextAndSetWall(x+1, y, Dir.W)

    increment = 1 if val else -1
    if y != 0: self.wh.incrWallcenterCount(x, y-1, increment)
    if y != BOARDSIZE: self.wh.incrWallcenterCount(x, y, increment)

##########################################################################################################################
                                                      #MOVE PLAYER
##########################################################################################################################
  def movePlayer(self, p, state, d, d2 = Dir.NoDir):
    """Move player to direction.

    Args:
        p (Player): Player
        state (Playerstate): Playerstate before the turn.
        d (Dir): Direction
        d2 (Dir, optional): Direction after Jump. Defaults to Dir.NoDir.

    Returns:
        state: new state after the player.
    """
    #Assumption viable direction
    x, y = self.ph.getPos(p)
    new_x, new_y = self.fh.movePlayer(x, y, p, d, d2)
    self.ph.setPos(p, new_x, new_y)
    new_h = self.fh.getHeuristic(new_x, new_y, p)
    state = Playerstate.newPlayerstate(state, [new_x, new_y], new_h)   

    self.updatePlayerPaths()

    return state

  def getPlayerMoves(self, state):
    """Get all possible moves of a player.

    Args:
        state (Playerstate): currentPlayerstate

    Returns:
        List: List of tuple(Direction, direction in case of a jump, heuristic of new place, state after the move)
    """
    p = state.p_now
    x , y = state.p1_pos if p == Player.P1 else state.p2_pos
    other_pos = state.p2_pos if p == Player.P1 else state.p1_pos

    moves = []
    for d in [Dir.N, Dir.E, Dir.S, Dir.W]:
      if self.fh.getWall(x, y, d): continue

      pos_moved = self.fh.getDir(x, y, d)
      if not pos_moved: continue

      x_moved, y_moved = pos_moved


      if pos_moved != other_pos:
        moves.append(self.zipMove(pos_moved, p, state, d, Dir.NoDir))
        
      else: #Jump over Player
        if self.fh.getWall(x_moved, y_moved, d) or not self.fh.getDir(x_moved, y_moved, d): #Side Jump
          for d2 in [Dir.N, Dir.E, Dir.S, Dir.W]:
            if d2 in [d, mir(d)]: continue
            if self.fh.getWall(x_moved, y_moved, d2): continue

            new_pos = self.fh.getDir(x_moved, y_moved, d2)
            if not new_pos:continue

            moves.append(self.zipMove(new_pos, p, state, d, d2))
        else: #Straight Jump
          pos_jump = self.fh.getDir(x_moved, y_moved, d)
          moves.append(self.zipMove(pos_jump, p, state, d, d))
    return moves

  def zipMove(self, pos, p, state, d, d2):
    x, y = pos
    h = self.fh.getHeuristic(x, y, p)
    new_state = Playerstate.newPlayerstate(state, pos, h)
    return (d, d2, h, new_state)

##########################################################################################################################
                                                    #PLAYER PATH STUFF #MAYBE UNNECESSARYgetPath
##########################################################################################################################
  def updatePlayerPaths(self):
    """Updates the paths of each player."""
    self.wh.initWallOnPath()
    for p in [Player.P1, Player.P2]:
      x, y = self.ph.getPos(p)
      p_path = self.findPaths(x, y, p)
      self.ph.setPath(p, p_path)

  def findPaths(self, x, y, p):
    """Recursivly finds path from player to goal.

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
                                                #CHECK SETABLE WALLS
##########################################################################################################################
  def getAllSetableWalls(self):
    """Generate List of pairs with wallpairs that are setable.

    Returns:
        List: List of pairs(x-Coordinate, y-coordinate, orientation)
    """
    return [(x, y, o) for x in range(BOARDSIZE) for y in range(BOARDSIZE) for o in [Orientation.H, Orientation.V] if self.isWallSetable(x, y, o)]

  def isWallSetable(self, x, y, o):
    """Checks if a wallpair is setable.

    Args:
        x (int): X-coordinate of the wallpair
        y (int): Y-coordinate of the wallpair
        o (Orientation): Orientation of the wallpair

    Returns:
        bool: True is wallpair is setable, False if not
    """
    midCon_count =  self.wh.getWallcenterCount(x, y)

    #already locked center
    if midCon_count > 1: return False
    
    #If middle center has 1 wall that is not on that orientation
    (w2_x, w2_y) = (x+1, y) if o == Orientation.H else (x, y+1)  
    if midCon_count == 1 and (self.wh.isWallSet(x, y, o) or self.wh.isWallSet(w2_x, w2_y, o)): return False

    #if there are 2 or more loose connectors 
    if self.wh.countFreeCentersInWall(x, y, o) in [2,3]: return True

    #if players have a way to reach the goal even if the walls were set
    return self.findGoalReachability(x, y, o)
  
  def findGoalReachability(self,x, y, o):
    """find if all players are able to reach their goals if a wallpair would be set. 

    Args:
        x (int): X-coordinate of the temporary wallpair
        y (int): Y-coordinate of the temporary wallpair
        o (Orientation): Orientation of the temporary wallpair

    Returns:
        bool: True if all players reach goal, False if atleast one player does not reach the goal
    """
    self.setWallPairInField(x, y, o, True)

    returnValue = True
    for p in [Player.P1, Player.P2]:
      p_x, p_y = self.ph.getPos(p)
      self.fh.help_checkedForPlayer = []
      returnValue &= self.fh.doesPlayerReachGoal(p_x, p_y, p)

    self.setWallPairInField(x, y, o, False)
    return returnValue   

  def setWallPairInField(self, x, y, o, val):
    """Sets the wall value in fields for a wallpair.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        o (Orientation): Orientation of the wall
        val (bool): State of the wall to be set
    """
    if Orientation.H == o:
      dirs = [(Dir.NE, Dir.S), (Dir.NW, Dir.S), (Dir.SE, Dir.N), (Dir.SW, Dir.N)]
    else: #if Orientation.V == o: 
      dirs = [(Dir.NE, Dir.W), (Dir.SE, Dir.W), (Dir.NW, Dir.E), (Dir.SW, Dir.E)]
    for d, d_passthrough in dirs:
      f_x = x + d[0]
      f_y = y + d[1]
      self.fh.setWall(f_x, f_y, d_passthrough, val)

##########################################################################################################################
                                                          #EVAL
##########################################################################################################################

  def evalPos(self, p1_pos, p2_pos):
    pass

  def isGameOver(self, state):
    if state.h_p1 == 0: return Player.P1
    if state.h_p2 == 0: return Player.P2
    return Player.Empty

  def minmax(self, state, depth, alpha, beta, maxMe):
    if depth == 100 or self.isGameOver(state) != Player.Empty:
      return state.h_p2 - state.h_p1, depth
    

    moves = self.getPlayerMoves(state)
    moves.sort(key=lambda x:x[2])
    

    if maxMe:
      maxEval = MINUSINFINITE

      for m in moves:
        eval, new_depth = self.minmax(m[3], depth +1, alpha, beta, False)
        if new_depth + 1 < depth:
          depth = new_depth + 1
        maxEval = max(maxEval, eval)
        alpha = max(alpha, eval)
        if beta <= alpha: break
      return maxEval, depth
    else:
      minEval = INFINITE

      for m in moves:
        eval, new_depth = self.minmax(m[3], depth + 1, alpha, beta, True)
        if new_depth+1 < depth:
          depth = new_depth + 1
        minEval = min(minEval, eval)
        beta = min(beta, eval)
        if beta <= alpha: break
      return minEval, depth