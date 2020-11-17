#TO INCLUDE
#Fields
#Walls
# Function to load/save board positions
from helper import INFINITE, Orientation
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
    self.wallhandler.setWallPair(self.fieldhandler.fields, x, y, orientation, self.fieldhandler.upDisco, self.fieldhandler.downDisco)
    solorepeatpos = None
    while self.fieldhandler.upDisco:
      self.fieldhandler.upDisco.sort()
      if self.fieldhandler.upDisco[0][0] > 200:
        if len(self.fieldhandler.upDisco) > 1: 
          for disco in self.fieldhandler.upDisco: 
            self.fieldhandler.fields[disco[1][0]][disco[1][1]].setUpUnreachable()
          self.fieldhandler.upDisco.clear()
          break 
        if len(self.fieldhandler.upDisco) == 1:
          if solorepeatpos == self.fieldhandler.upDisco[0][1]:
            self.fieldhandler.fields[solorepeatpos[0]][solorepeatpos[1]]
            self.fieldhandler.upDisco.clear()
            break
          solorepeatpos = self.fieldhandler.upDisco[0][1]

      c_h, c_pos = self.fieldhandler.upDisco[0]
      self.fieldhandler.upDisco = self.fieldhandler.upDisco[1:]
      self.fieldhandler.setUpNextToShortest(c_pos[0], c_pos[1], c_h, self.fieldhandler.upDisco)



