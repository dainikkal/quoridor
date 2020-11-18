#TO inlcude:
#boardpos
#move history(boardpos) + prior history

from Field import Field
from helper import BOARDSIZEMID, Orientation, UpDown
from Board import Board


class Game():
  def __init__(self):
    b = Board()
    b.setWall(0, 1, Orientation.H)
    b.setWall(3, 1, Orientation.H)
    b.setWall(1, 1, Orientation.V)
    b.setWall(2, 2, Orientation.V)
    b.setWall(1, 2, Orientation.H)
    b.debug__printInformation(Field.getHeuristic, UpDown.U)
    b.debug__printInformation(Field.getNexts, UpDown.U)
    print("hello world")
