from game.Path import Path
from game.Field import Field
from game.helper import BOARDSIZE, BOARDSIZEMID, Dir, HEURISTICJUMP, Player, mir, UpDown

class FieldHandler():
  def __init__(self):
    self.fields = {(x, y) : Field(x, y) for x in range(BOARDSIZE+1) for y in range(BOARDSIZE+1)}
    self.fields[(BOARDSIZEMID, BOARDSIZE)].setPlayer(Player.P1)
    self.fields[(BOARDSIZEMID, 0)].setPlayer(Player.P2)    
    self.disconnected = [[], []]

    self.help_checkedForPlayer = []

  def getWall(self, x, y, d): return self.fields[(x, y)].getWall(d)
  def setWall(self, x, y, d, val=True): self.fields[(x, y)].setWall(d, val)
  def getNexts(self, x, y, p): return self.fields[(x, y)].getNexts(p)
  def getDir(self, x, y, d): return self.fields[(x, y)].getDir(d)
  def getHeuristic(self, x, y, p): return self.fields[(x, y)].getHeuristic(p)

##########################################################################################################################
                                                    #SET WALL
##########################################################################################################################
  def removeNextAndSetWall(self, x, y, d, val=True):
    """Removes Next that wall pierces, disconnects the field and sets the Wall. 

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        d (Dir): Direction
        val (bool): if the wall is to be set or unset
    """
    self.removeNextAndAddToDisco(x, y, Player.P1, d)
    self.removeNextAndAddToDisco(x, y, Player.P2, d)
    self.fields[(x, y)].setWall(d,val)

  def removeNextAndAddToDisco(self, x, y, p, d):
    """Removes Nexts and according Prevs and disconnects field.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        p (Player): Player
        d (Dir): Direction
    """
    if d in self.fields[(x, y)].getNexts(p):
      self.fields[(x, y)].removeFromNexts(p, d)
      d_x, d_y = self.fields[(x, y)].getDir(d)
      self.fields[(d_x, d_y)].removeFromPrevs(p, mir(d))
      if not self.fields[(x, y)].getNexts(p):
        self.fields[(x, y)].setDisconnected(p, True)
        h = self.fields[(x, y)].getHeuristic(p)
        self.disconnected[p].append((h, (x, y)))

##########################################################################################################################
                                                    #RECONNECT Disconnected Fields
##########################################################################################################################
  def reconnectDisconnectedFields(self, p):
    """Reconnects disconnected fields and updates next.

    Args:
        p (Player): Player
    """
    prevDisconnects = None
    repeatCount = len(self.disconnected[p])

    while self.disconnected[p]:
      tmpDisconnects = self.disconnected[p]
      tmpDisconnects.sort()
      smallest_h = tmpDisconnects[0][0]
      if smallest_h > HEURISTICJUMP * 2:
        if self.compareDisconnectsByPos(prevDisconnects, tmpDisconnects):
          if repeatCount == 0:
            self.setDisconnectedUnreachable(p)
            break
          repeatCount -= 1
        else: repeatCount = len(self.disconnected[p])
        prevDisconnects = tmpDisconnects

      s_h, (s_x, s_y) = tmpDisconnects[0]
      self.disconnected[p] = tmpDisconnects[1:]
      self.setNextToShortest(s_x, s_y, p, s_h)

  def compareDisconnectsByPos(self, prev, curr):
    """Compares if 2 disconnection (heuristic, (posX, posY)) arrays are the same.

    Args:
        prev (List): List of disconnections (heuristic, (posX, posY))
        curr (List): List of disconnections (heuristic, (posX, posY))

    Returns:
        Bool: True if the same, False otherwise
    """
    if not prev: return False 
    if len(prev) != len(curr): return False
    prev.sort(key=lambda x:x[1])
    curr.sort(key=lambda x:x[1])
    for (_, p), (_, c) in zip(prev, curr):
      if p != c: return False
    return True

  def setDisconnectedUnreachable(self, p):
    """Sets all disconnected Fields to unreachable.

    Args:
        p (Player): Player
    """
    for _, pos in self.disconnected[p]:
      self.fields[pos].setUnreachable(p)
    self.disconnected[p].clear()

  def setNextToShortest(self, x, y, p, h):
    """Adds Next to all the neighbours with shortest distance.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        p (Player): Player
        h (int): Heuristic of the neighbour closest to the goal
    """
    self.fields[(x, y)].setDisconnected(p, False)

    neighbours = self.findVisitiableNeighbours(x, y, p)
    neighbours.sort()
    if not neighbours or neighbours[0][0] >= HEURISTICJUMP:       
      self.reAddToDisconnected(x, y, p, h)
      return
    
    smallest_h = neighbours[0][0]
    self.fields[(x, y)].setHeuristic(p, smallest_h+1)

    for n in neighbours:
      n_h, n_pos, n_dir = n
      if n_h != smallest_h: break
      self.fields[(x, y)].addToNexts(p, n_dir)
      self.fields[n_pos].addToPrevs(p, mir(n_dir))


  def findVisitiableNeighbours(self, x, y, p):
    """Finds all Neighbours from the current field that are not disconnected or in Prevs.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        p (Player): Player

    Returns:
        List: List of viable neighbours (heuristic, (posX, posY), direction)
    """
    neighbours = []
    for d in range(4):
      #Walll
      if self.fields[(x, y)].getWall(d): continue
      posD = self.fields[(x, y)].getDir(d)
      #Border
      if posD == None: continue
      #Discnonnected
      if self.fields[posD].getDisconnected(p): continue
      prevs = self.fields[(x, y)].getPrevs(p)
      #Prevs
      if d in prevs:#POT ERROR: if prevs and d in prevs
        d_x, d_y = posD   
        self.removeNextAndAddToDisco(d_x, d_y, p, mir(d))
        continue
      h = self.fields[posD].getHeuristic(p)
      neighbours.append((h, posD, d))
    return neighbours

  def reAddToDisconnected(self, x, y, p, h):
    """Reads a field to be disconnected.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        p (Player): Player
        h (heuristic): old heuristic the player  had
    """
    self.fields[(x, y)].setHeuristic(p, h + HEURISTICJUMP)
    self.fields[(x, y)].setDisconnected(p, True)
    self.disconnected[p].append((h + HEURISTICJUMP, (x, y)))

    
##########################################################################################################################
                                                      #MOVE PLAYER
##########################################################################################################################
  def movePlayer(self, x, y, p, d, d2 = Dir.NoDir):
    """Move player.

    Args:
        x (int): X-Coordinate of the player
        y (int): Y-Coordinate of the player
        p (Player): Player
        d (Direction): Direction to Move
        d2 (Direction, optional): Direction to Move in Case of a Jump. Defaults to Dir.NoDir.

    Returns:
        int, int: new coordinates of the player
    """
    new_pos =  self.fields[(x, y)].getDir(d)
    #check if position is a jump over player
    if self.fields[new_pos].getPlayer() != Player.Empty:
      new_pos =  self.fields[new_pos].getDir(d2)
      
    self.fields[(x, y)].setPlayer(Player.Empty)
    self.fields[new_pos].setPlayer(p)
    return new_pos

    
##########################################################################################################################
                                                      #FIND PLAYER
##########################################################################################################################  
  def doesPlayerReachGoal(self, x, y, p):
    """Recursivly checks if a player is able to reach their goal.

    Args:
        x (int): x-coordinate of current field
        y (int): y-coordiante of current field
        p (Player): Player to be checked

    Returns:
        bool: True if player is able to reach the goal, False if not
    """
    self.help_checkedForPlayer.append((x, y))
    if self.fields[(x, y)].getHeuristic(p) == 0: return True

    for d in [Dir.N, Dir.E, Dir.S, Dir.W]:
      if self.fields[(x, y)].getWall(d): continue
      n_pos = self.fields[(x, y)].getDir(d) 
      if n_pos and n_pos not in self.help_checkedForPlayer:
        n_x, n_y = n_pos
        if self.doesPlayerReachGoal(n_x, n_y, p): return True

    return False