#TO INCLUDE
#Fields
#Walls
# Function to load/save board positions
from helper import BOARDSIZE, HEURISTICJUMP, INFINITE, Orientation, UpDown
from FieldHandler import FieldHandler
from WallHandler import WallHandler

class Board():
  def __init__(self, gamestate=""):    
    self.wallhandler = WallHandler()
    self.fieldhandler = FieldHandler()
    if gamestate !="": #__loadBameState()
      pass

  def __loadBoardState(self):
    pass

  #assumption legal move!!!
  def setWall(self, x, y, orientation):
    self.wallhandler.setWallPair(self.fieldhandler.fields, x, y, orientation, self.fieldhandler.disco)
    self.__reconnectDisco(UpDown.U)
    self.__reconnectDisco(UpDown.D)

  def __reconnectDisco(self, i):
    prevDisco = None

    while self.fieldhandler.disco[i]:
      tmpDisco = self.fieldhandler.disco[i]
      tmpDisco.sort()
      smallest_h = tmpDisco[0][0]
      if smallest_h > HEURISTICJUMP * 2:
        if self.__discoCompareByPos(prevDisco, tmpDisco):
          self.fieldhandler.setDiscoUnreachable(i)
          break
        prevDisco = tmpDisco

      c_h, (c_x, c_y) = tmpDisco[0]
      self.fieldhandler.disco[i] = tmpDisco[1:]
      self.fieldhandler.setNextToShortest(i, c_x, c_y, c_h)

  def __discoCompareByPos(self, prev, curr):
    if not prev: return False 
    if len(prev) != len(curr): return False
    prev.sort(key=lambda x:x[1])
    curr.sort(key=lambda x:x[1])
    for (_, p), (_, c) in zip(prev, curr):
      if p != c: return False
    return True

  def debug__printInformation(self, myLambda,*args):
    for y in range(BOARDSIZE+1):
      s = ""
      for x in range(BOARDSIZE+1):
        s += str(myLambda(self.fieldhandler.fields[x][y], *args)) + " "
      print(s)
