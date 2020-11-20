from Field import Field
from helper import Orientation, Player, UpDown
from Board import Board

class Game():
  def __init__(self):
    #TODO WRITE PEP257
    b = Board()
    b.setWall(0, 1, Orientation.H)
    b.setWall(3, 1, Orientation.H)
    b.setWall(1, 1, Orientation.V)
    b.setWall(2, 2, Orientation.V)
    b.setWall(1, 2, Orientation.H)
    b.debug_PrintInformation(Field.getHeuristic, Player.P1)
    b.debug_PrintInformation(Field.getNexts, Player.P1)
    print("hello world")