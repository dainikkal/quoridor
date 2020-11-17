#TO inlcude:
#boardpos
#move history(boardpos) + prior history

from helper import BOARDSIZEMID, Orientation
from Board import Board


class Game():
  def __init__(self):
    b = Board()
    b.setWall(0, 0, Orientation.H)
    b.setWall(2, 0, Orientation.H)
    b.setWall(3, 1, Orientation.V)
    b.setWall(3, 3, Orientation.V)
    print("hello world")
