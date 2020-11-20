from Field import Field
from helper import BOARDSIZE, BOARDSIZEMID, HEURISTICJUMP, Player, mir, UpDown

class FieldHandler():
  def __init__(self):
    self.fields = [[Field(x,y) for y in range(BOARDSIZE+1)] for x in range(BOARDSIZE+1)]    
    self.fields[BOARDSIZEMID][BOARDSIZE].setPlayer(Player.P1)
    self.fields[BOARDSIZEMID][0].setPlayer(Player.P2)    
    self.disconnected = [[], []]

  def setWall(self, x, y, d): self.fields[x][y].setWall(d)
  def getWall(self, x, y, d): return self.fields[x][y].getWall(d)

  def getDir(self, x, y, d): return self.fields[x][y].getDir(d)
  def getWallDir(self, x, y, d): return self.fields[x][y].getWallDir(d)
  
  def setHeurisitic(self, x, y, p, val): self.fields[x][y].setHeuristic(p, val)
  def getHeuristic(self, x, y, p): return self.fields[x][y].getHeuristic(p)

  def getNexts(self, x, y, p): return self.fields[x][y].getNexts(p)
  def addToNexts(self, x, y, p, d): self.fields[x][y].addToNexts(p, d)
  def removeFromNexts(self, x, y, p, d): self.fields[x][y].removeFromNexts(p, d)
  
  def getPrevs(self, x, y, p): return self.fields[x][y].getPrevs(p)
  def addToPrevs(self, x, y, p, d): self.fields[x][y].addToPrevs(p, d)
  def removeFromPrevs(self, x, y, p, d): self.fields[x][y].removeFromPrevs(p, d)

  def setDisconnected(self, x, y, p, val): self.fields[x][y].setDisconnected(p, val)

  def getDisconnected(self, x, y, p): return self.fields[x][y].getDisconnected(p)
  def setDisconnected(self, x, y, p, val): self.fields[x][y].setDisconnected(p, val)
  def appendDisconnected(self, p, h, x, y): self.disconnected[p].append((h, (x, y)))


##########################################################################################################################
                                                    #SET WALL
##########################################################################################################################
  def removeNextAndSetWall(self, x, y, d):
    """Removes Next that wall pierces, disconnects the field and sets the Wall. 

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        d (Dir): Direction
    """
    if d in self.getNexts(x, y, Player.P1):
      self.__removeNextAndAddToDisco(x, y, Player.P1, d)
    if d in self.getNexts(x, y, Player.P2):
      self.__removeNextAndAddToDisco(x, y, Player.P2, d)
    self.setWall(x, y, d)

  def __removeNextAndAddToDisco(self, x, y, p, d):
    """Removes Nexts and according Prevs and disconnects field 

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        p (Player): Player
        d (Dir): Direction
    """
    if d in self.getNexts(x, y, p):
      self.removeFromNexts(x, y, p, d)
      d_x, d_y = self.getDir(x, y, d)
      self.removeFromPrevs(d_x, d_y, p, mir(d))
      if not self.getNexts(x, y, p):
        self.setDisconnected(x, y, p, True)
        self.appendDisconnected(p, self.getHeuristic(x, y , p), x, y)

##########################################################################################################################
                                                    #RECONNECT Disconnected Fields
##########################################################################################################################
  def reconnectDisconnectedFields(self, p):
    """Reconnects disconnected fields and updates next

    Args:
        p (Player): Player
    """
    prevDisconnects = None

    while self.disconnected[p]:
      tmpDisconnects = self.disconnected[p]
      tmpDisconnects.sort()
      smallest_h = tmpDisconnects[0][0]
      if smallest_h > HEURISTICJUMP * 2:
        if self.__compareDisconnectsByPos(prevDisconnects, tmpDisconnects):
          self.__setDisconnectedUnreachable(p)
          break
        prevDisconnects = tmpDisconnects

      s_h, (s_x, s_y) = tmpDisconnects[0]
      self.disconnected[p] = tmpDisconnects[1:]
      self.__setNextToShortest(s_x, s_y, p, s_h)

  def __compareDisconnectsByPos(self, prev, curr):
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

  def __setDisconnectedUnreachable(self, p):
    """Sets all disconnected Fields to unreachable

    Args:
        p (Player): Player
    """
    for _,(x,y) in self.disconnected[p]:
      self.fields[x][y].setUnreachable(p)
    self.disconnected[p].clear()

  def __setNextToShortest(self, x, y, p, h):
    """Adds Next to all the neighbours with shortest distance.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        p (Player): Player
        h (int): Heuristic of the neighbour closest to the goal
    """
    self.setDisconnected(x, y, p, False)

    neighbours = self.__findVisitiableNeighbours(x, y, p)
    neighbours.sort()
    if not neighbours or neighbours[0][0] >= HEURISTICJUMP:       
      self.__reAddToDisconnected(x, y, p, h)
      return
    
    smallest_h = neighbours[0][0]
    self.setHeurisitic(x, y, p, smallest_h)

    for n in neighbours:
      n_h, (n_x, n_y), n_dir = n
      if n_h != smallest_h: break
      self.addToNexts(x, y, p, n_dir)
      self.addToPrevs(n_x, n_y, p, mir(n_dir))


  def __findVisitiableNeighbours(self, x, y, p):
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
      if self.getWall(x, y, d): continue
      posD = self.getDir(x, y, d)
      #Border
      if posD == None: continue
      d_x, d_y = posD   
      #Discnonnected
      if self.getDisconnected(d_x, d_y, p): continue
      prevs = self.getPrevs(x, y, p)
      #Prevs
      if d in prevs:#POT ERROR: if prevs and d in prevs
        self.__removeNextAndAddToDisco(d_x, d_y, p, mir(d))
        continue
      neighbours.append((self.getHeuristic(d_x, d_y, p), (d_x, d_y), d))
    return neighbours

  def __reAddToDisconnected(self, x, y, p, h):
    """Readds a field to be disconnected.

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        p (Player): Player
        h (heuristic): old heuristic the player  had
    """
    self.fields[x][y].setHeuristic(p, h + HEURISTICJUMP)
    self.fields[x][y].setDisconnected(p, True)
    self.disconnected[p].append((h + HEURISTICJUMP, (x, y)))

##########################################################################################################################
                                                    #FIND SHORTEST PATH FROM X/Y
##########################################################################################################################
  def findPaths(self, x, y, p):
    """Finds shortest path from position to the Goal

    Args:
        x (int): X-coordinate
        y (int): Y-coordinate
        p (Player): Player

    Returns:
        List: Path Tree (direction, (posX, posY), subPaths) subPaths is a recursive created Path Tree
    """
    nexts = self.getNexts(x, y, p)
    path = []
    if not nexts: return path

    for d in nexts:
      n_x, n_y = self.getDir(x, y, d)
      path.append((d, (n_x, n_y), self.findPaths(n_x, n_y, p)))
    return path