from Field import Field
from helper import BOARDSIZE,BOARDSIZEMID, Player, mir
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
    
    self.upDisco = []# array[] of pairs (heuristic, (posX, posY))
    self.downDisco = []

  def setUpNextToShortest(self, x, y, h, upDisco):
    current = self.fields[x][y]
    current.setUpDisco(False)
    neighbours = []
    for d in range(4):
      if current.getWall(d): continue
      posD = current.getDir(d)
      if posD == None: continue
      posD_x, posD_y = posD   
      if self.fields[posD_x][posD_y].getUpDisco(): continue
      prevs = current.getUpPrevs()
      if prevs:
        if d in prevs:
          self.fields[posD_x][posD_y].removeUpNextAddToUpDisco(mir(d), self.fields, upDisco)
          continue

      neighbours.append( (self.fields[posD_x][posD_y].getUpHeuristic(), (posD_x, posD_y), d))
    
    if not neighbours: 
      current.setUpHeuristic(h + 100)
      current.setUpDisco(True)
      self.upDisco.append((h+100, (x,y)))
      return

    neighbours.sort()
    closest = neighbours[0]
    neighbours = neighbours[1:]
    if closest[0] > 100: 
      current.setUpHeuristic(h + 100)
      current.setUpDisco(True)
      self.upDisco.append((h+100, (x,y)))
      return
    c_h, c_pos, c_dir = closest
    c_posX , c_posY = c_pos
    current.setUpHeuristic(c_h + 1)
    current.addToUpNexts(c_dir)
    self.fields[c_posX][c_posY].addToUpPrevs(mir(c_dir))

    for n in neighbours:
      n_h, n_pos, n_dir = n
      if n_h != c_h: continue
      n_posX , n_posY = n_pos
      current.addToUpNexts(n_dir)
      self.fields[n_posX][n_posY].addToUpPrevs(mir(n_dir))
