from Playerstate import Playerstate
from Field import Field
from helper import Dir, INFINITE, MINUSINFINITE, Orientation, Player, UpDown
from Board import Board
from Path import Path

class Game():
  def __init__(self):
    #TODO WRITE PEP257
    self.b = Board()
    
    self.b.movePlayer(Player.P1, Dir.E)
    
    pos_p1 = self.b.ph.getPos(Player.P1)
    pos_p2 = self.b.ph.getPos(Player.P2)
    h_p1 = self.b.fh.getHeuristic(pos_p1[0], pos_p1[1], Player.P1)
    h_p2 = self.b.fh.getHeuristic(pos_p2[0], pos_p2[1], Player.P2)
    state = Playerstate(pos_p1, pos_p2, Player.P2, h_p1, h_p2)

    print(self.b.minmax(state,100, MINUSINFINITE, INFINITE, True))

    #self.currentWinner = self.projectWinner()


    #self.b.movePlayer(Player.P1, Dir.N)
    #self.b.movePlayer(Player.P2, Dir.S)
    #print(self.b.getPlayerMoves(Player.P1))
    #self.b.movePlayer(Player.P1, Dir.N)
    #self.b.debug_PrintInformation(Field.getPlayer)
    #print(self.b.getPlayerMoves(Player.P2))

    #self.b.setWall(0, 1, Orientation.H)
    #self.b.setWall(1, 1, Orientation.V)
    #self.b.setWall(2, 1, Orientation.V)
    #self.b.setWall(2, 2, Orientation.H)

    #print(self.b.getAllSetableWalls())
 
    #self.b.debug_PrintInformation(Field.getHeuristic, Player.P1)
    #self.b.debug_PrintInformation(Field.getNexts, Player.P1)self.b.getAllSetableWalls()

  def turn(self):

    self.currentPlayer = Player.P2 if self.currentPlayer == Player.P1 else Player.P1