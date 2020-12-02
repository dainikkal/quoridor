from Field import Field
from helper import Dir, Orientation, Player, UpDown
from Board import Board

class Game():
  def __init__(self):
    #TODO WRITE PEP257
    b = Board()
    b.movePlayer(Player.P2, Dir.S)
    b.movePlayer(Player.P1, Dir.E)

    b.setWall(0, 1, Orientation.H)
    b.setWall(1, 1, Orientation.V)
    b.setWall(2, 1, Orientation.V)
    b.setWall(2, 2, Orientation.H)

    r = b.getAllSetableWalls()
    print(len(r), r)

    b.debug_PrintInformation(Field.getHeuristic, Player.P1)
    b.debug_PrintInformation(Field.getNexts, Player.P1)
    print("hello world")