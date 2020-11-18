from Field import Field
from helper import BOARDSIZE,BOARDSIZEMID, HEURISTICJUMP, Player, mir
class FieldHandler():

  def __init__(self):
    self.fields = []
    for x in range(BOARDSIZE+1):
      inner = []
      for y in range(BOARDSIZE+1):
        inner.append(Field(x,y))
      self.fields.append(inner)
    
    self.playerinfo = [None, None, None]
    self.playerinfo[Player.Empty] = None
    self.playerinfo[Player.P1] = (BOARDSIZEMID, BOARDSIZE)
    self.fields[BOARDSIZEMID][BOARDSIZE].setPlayer(Player.P1)
    self.playerinfo[Player.P2] = (BOARDSIZEMID, 0)
    self.fields[BOARDSIZEMID][0].setPlayer(Player.P2)

    self.disco = [[],[]]

  def setNextToShortest(self, i, x, y, h):
    current = self.fields[x][y]
    current.setDisco(i, False)

    neighbours = self.__getNeighboursForNext(i, x, y)
    neighbours.sort()
    if not neighbours or neighbours[0][0] >= HEURISTICJUMP:       
      return self.__reAddToDisco(i, x, y, h)
    
    smallest_h = neighbours[0][0]
    current.setHeuristic(i, smallest_h + 1)

    for n in neighbours:
      n_h, (n_x, n_y), n_dir = n
      if n_h != smallest_h: break
      current.addToNexts(i, n_dir)
      self.fields[n_x][n_y].addToPrevs(i, mir(n_dir))
  
  def setDiscoUnreachable(self, i):    
    for d in self.disco[i]: 
      d_x, d_y = d[1]
      self.fields[d_x][d_y].setUnreachable(i)
    self.disco[i].clear()

  def __reAddToDisco(self, i, x, y, h):
      self.fields[x][y].setHeuristic(i, h + HEURISTICJUMP)
      self.fields[x][y].setDisco(i, True)
      self.disco[i].append((h + HEURISTICJUMP, (x,y)))


  def __getNeighboursForNext(self, i, x, y):
    current = self.fields[x][y]
    neighbours = []
    for d in range(4):
      #Walll
      if current.getWall(d): continue
      posD = current.getDir(d)
      #Border
      if posD == None: continue
      posD_x, posD_y = posD   
      #Discnonnected
      if self.fields[posD_x][posD_y].getDisco(i): continue
      prevs = current.getPrevs(i)
      #Prevs
      if d in prevs:#POT ERROR: if prevs and d in prevs
        self.fields[posD_x][posD_y].removeNextAddToDisco(i, mir(d), self.fields, self.disco)
        continue

      neighbours.append((self.fields[posD_x][posD_y].getHeuristic(i), (posD_x, posD_y), d))
    return neighbours