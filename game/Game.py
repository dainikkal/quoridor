from game.Playerstate import Playerstate
from game.Field import Field
from game.helper import Dir, INFINITE, MINUSINFINITE, Orientation, Player, UpDown
from game.Board import Board
from game.Path import Path

class Game():
  def __init__(self):
    #TODO WRITE PEP257
    self.b = Board()
    self.currentPlayer = Player.P1
    self.classes = {} #refactor into "b" to increase performence
    self.links = {} #refactor into "b" to increase performence
    self.tasks = {} #refactor into "b" to increase performence
    self.update_classes()

  def turn(self):
    #check win
    self.currentPlayer = Player.P2 if self.currentPlayer == Player.P1 else Player.P1

  def execute_action(self, action_code):
    if action_code not in self.tasks.keys(): return
    action, params = self.tasks[action_code]
    action(*params)

    self.turn()
    self.update_classes()

  def move_player(self, d, d2=Dir.NoDir): self.b.movePlayer(self.currentPlayer, d, d2)
  def set_wall(self, x, y, o): self.b.setWall(x, y, o)

  def update_classes(self):
    self.tasks.clear()
    for i in range(17*17): self.links[i] = ""
    self.add_fields_to_classes()
    self.add_wallcenters_to_classes()
    self.add_horizontal_walls_to_classes()
    self.add_vertical_walls_to_classes()

  def add_wallcenters_to_classes(self):
    for y in range(0, 8):
      for x in range(0, 8):
        val = "Square Wall C"

        val += " V" + str(x) + "-" + str(y)
        val += " H" + str(x) + "-" + str(y)

        val += " set" if self.b.wh.isCenterSet(x, y) else " open"

        self.classes[(y*2+1)*17 + x*2+1] = val
  
  def add_horizontal_walls_to_classes(self):
    for y in range(0,8):
      for x in range(0, 9):
        val = "Square Wall H Hpiece" + str(x) + "-" + str(y)

        if x != 0: val += " H" + str(x-1) + "-" + str(y)
        if x != 8: val += " H" + str(x) + "-" + str(y)

        val += " set" if self.b.wh.isWallSet(x, y, Orientation.H) else " open"
        if x != 8 and self.b.isWallSetable(x, y, Orientation.H): 
          val += " setable"
          code = "Hpiece" + str(x) + "-" + str(y)
          self.links[(y*2+1)*17 + x*2] = code
          self.tasks[code] = [self.set_wall, [x, y, Orientation.H]]

        self.classes[(y*2+1)*17 + x*2] = val

  def add_vertical_walls_to_classes(self):
    for y in range(0,9):
      for x in range(0,8):
        val = "Square Wall V Vpiece" + str(x) + "-" + str(y)

        if y != 0: val += " V" + str(x) + "-" + str(y-1)
        if y != 8: val += " V" + str(x) + "-" + str(y)

        val += " set" if self.b.wh.isWallSet(x, y, Orientation.V) else " open"
        
        if y != 8 and self.b.isWallSetable(x, y, Orientation.V):
          val += " setable"
          code = "Vpiece" + str(x) + "-" + str(y)
          self.links[(y*2*17 + x*2+1)] = code
          self.tasks[code] = [self.set_wall, [x, y, Orientation.V]]

        self.classes[(y*2*17 + x*2+1)] = val

  def add_fields_to_classes(self):
    for y in range(0, 9):
      for x in range(0, 9):
        self.classes[x*2 + 17*2*y] = "Square F F" + str(x) + "-" + str(y)

    pos_p1 = self.b.ph.getPos(Player.P1)
    pos_p2 = self.b.ph.getPos(Player.P2)    
    self.classes[pos_p1[0]*2 + 17*2*pos_p1[1]] += " P1"
    self.classes[pos_p2[0]*2 + 17*2*pos_p2[1]] += " P2"

    h_p1 = self.b.fh.getHeuristic(pos_p1[0], pos_p1[1], Player.P1)
    h_p2 = self.b.fh.getHeuristic(pos_p2[0], pos_p2[1], Player.P2)
    state = Playerstate(pos_p1, pos_p2, self.currentPlayer, h_p1, h_p2)
    moves = self.b.getPlayerMoves(state)
    x, y = self.b.ph.getPos(self.currentPlayer)
    for m in moves:
      pos_relative = x*2 + 17*2*y
      move_code = "Move" + str(m[0])
      if m[0] == Dir.N: pos_relative = pos_relative - 17*2
      if m[0] == Dir.E: pos_relative = pos_relative + 2
      if m[0] == Dir.S: pos_relative = pos_relative + 17*2
      if m[0] == Dir.W: pos_relative = pos_relative - 2
      if m[1] != -1:
        move_code += "-" + str(m[1])
        if m[1] == Dir.N: pos_relative = pos_relative - 17*2
        if m[1] == Dir.E: pos_relative = pos_relative + 2
        if m[1] == Dir.S: pos_relative = pos_relative + 17*2
        if m[1] == Dir.W: pos_relative = pos_relative - 2    
      self.classes[pos_relative] += " Move "  
      self.classes[pos_relative] += move_code
      self.links[pos_relative] = move_code
      self.tasks[move_code] = [self.move_player, [m[0], m[1]]]

  def get_classes(self): return [self.classes[i] for i in range(17*17)]
  def get_links(self): return [self.links[i] for i in range(17*17)]

