from game.helper import Player

class Playerstate():
  def __init__(self, p1_pos, p2_pos, p_current, h_p1, h_p2, oldstate = None):
    self.p1_pos = p1_pos if p1_pos != None else oldstate.p1_pos
    self.p2_pos = p2_pos if p2_pos != None else oldstate.p2_pos
    self.p_current = p_current if p_current != None else oldstate.p_current
    self.h_p1 = h_p1 if h_p1 != None else oldstate.h_p1
    self.h_p2 = h_p2 if h_p2 != None else oldstate.h_p2

  def newPlayerstate(state, new_pos, new_h, p):
    if p == Player.P1:
      return Playerstate(new_pos, None, Player.P2, new_h, None, state)
    return Playerstate(None, new_pos, Player.P1, None, new_h, state)

Playerstate.newPlayerstate = staticmethod(Playerstate.newPlayerstate)