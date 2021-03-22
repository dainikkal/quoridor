"""Handles instance of a game."""
from flask.helpers import safe_join
from game.Playerstate import Playerstate
from game.helper import BOARDSIZE, BOARDSIZEMID, Dir, Orientation, Player, mir
from game.Board import Board


class Game():
    """Instance of a Game."""

    def __init__(self, log=""):
        """Initialize Game class."""
        self.b = Board()
        self.currentPlayer = Player.P1
        pos_p1 = self.b.ph.getPos(Player.P1)
        pos_p2 = self.b.ph.getPos(Player.P2)   
        h_p1 = self.b.fh.getHeuristic(pos_p1[0], pos_p1[1], Player.P1)
        h_p2 = self.b.fh.getHeuristic(pos_p2[0], pos_p2[1], Player.P2)
        self.state = Playerstate(pos_p1, pos_p2, Player.P1, h_p1, h_p2)
        self.classes = {}
        self.links = {}
        self.tasks = {}
        self.winner = Player.Empty
        self.update_classes()
        self.redolog = []
        self.gamelog = []
        self.movelog = ([],[])
        self.load(log)


    def load(self, log):
        lines = log.split("-")
        for line in lines:
            parts = line.split(" ")
            if len(parts) < 2: continue
            self.redolog.append(parts[1])
            if len(parts) == 3:
                self.redolog.append(parts[2])
        while self.redolog:
            self.execute_redo()


    def turn(self):
        """Change the current Player."""
        self.currentPlayer = Player.P2 if self.currentPlayer == Player.P1 \
            else Player.P1


    def get_notation(self, x, y, o=None):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        if o == Orientation.H: 
            orientation = "h"
        elif o == Orientation.V:
            orientation = "v"
        else:
            orientation =""  
        return letters[x] + str(y + 1) + orientation

    def get_move_from_notation(self, code):
        letters = {"a":0, "b":1, "c":2, 
                   "d":3, "e":4, "f":5, 
                   "g":6, "h":7, "i":8}
        x = letters[code[0]]
        y = int(code[1]) - 1
        if len(code) == 2:
            o = None
        elif 'v' == code[2]:
            o = Orientation.V
        elif 'h' == code[2]:
            o = Orientation.H
        return x, y, o

    def execute_undo(self):
        last = self.gamelog[-1]
        if last[2] != None:
            p = Player.P2
            move = last[2]
            self.gamelog[-1] = last[:-1]
            self.gamelog[-1].append(None)
        else:
            p = Player.P1
            move = last[1]
            self.gamelog.pop()      
        self.redolog.append(move)

        x, y, o = self.get_move_from_notation(move)

        if o != None:
            self.b.setWall(x, y, o, False)
        else:
            d1, d2 = self.movelog[p].pop()
            d1_rev = mir(d1)
            if d2 != Dir.NoDir:
                d2_rev = mir(d2)
                self.state = self.b.movePlayer(p, self.state, d2_rev, d1_rev)
            else:
                self.state = self.b.movePlayer(p, self.state, d1_rev)
        
        self.turn()
        self.update_classes()
        self.state.p_now = self.currentPlayer


    def execute_redo(self):
        redo_notation = self.redolog.pop(0)
        self.execute_action(redo_notation, True)


    def execute_action(self, action_code, redo=False):
        """
        Calls an function pointer by inputing the action code.

        Args:
            action_code (string): key for the dict with the function pointers.
        """
        if action_code not in self.tasks.keys(): return

        if not redo: self.redolog.clear()

        action, params = self.tasks[action_code]
        action(*params)

        self.turn()
        self.update_classes()

    def move_player(self, d, d2=Dir.NoDir):
        """Moves player and check for win."""
        self.state = self.b.movePlayer(self.currentPlayer, self.state, d, d2)

        turnnumber = len(self.gamelog)
        if self.currentPlayer == Player.P1:
            x, y = self.state.p1_pos
            action = self.get_notation(x, y, None)
            self.gamelog.append([turnnumber + 1, action, None])
        else:
            turn = self.gamelog[turnnumber - 1]
            x, y = self.state.p2_pos
            turn[2] = self.get_notation(x, y, None)

        self.movelog[self.currentPlayer].append([d, d2])
        self.winner = self.b.isGameOver(self.state)

    def set_wall(self, x, y, o): 
        self.b.setWall(x, y, o)

        turnnumber = len(self.gamelog)         
        action = self.get_notation(x, y, o)
        if self.currentPlayer == Player.P1:
            self.gamelog.append([turnnumber + 1, action, None])
        else:
            turn = self.gamelog[turnnumber - 1] 
            turn[2] = action

    def update_classes(self):
        """Updates the classes for html."""
        self.tasks.clear()
        for i in range(17 * 17): self.links[i] = ""
        self.update_fields_to_classes()
        self.update_wallcenters_to_classes()
        self.update_horizontal_walls_to_classes()
        self.update_vertical_walls_to_classes()

    def calc_relative_horizontal_wall(self, x, y):
        return (y*2+1)*17 + x*2        
    def calc_relative_vertical_wall(self, x, y):
        return y*2*17 + x*2+1 
    def calc_relative_field(self, x, y):
        return x*2 + 17*2*y

    def update_wallcenters_to_classes(self):
        """Update the wall centers for html."""
        for y in range(0, 8):
            for x in range(0, 8):
                val = "Square Wall C"

                val += " V" + str(x) + "-" + str(y)
                val += " H" + str(x) + "-" + str(y)

                val += " set" if self.b.wh.isCenterSet(x, y) else " open"

                self.classes[(y*2+1)*17 + x*2+1] = val

    def update_horizontal_walls_to_classes(self):
        """Update the horizontal wall for html."""
        for y in range(0,8):
            for x in range(0, 9):
                val = "Square Wall H Hpiece" + str(x) + "-" + str(y)

                if x != 0: val += " H" + str(x-1) + "-" + str(y)
                if x != 8: val += " H" + str(x) + "-" + str(y)

                val += " set" if self.b.wh.isWallSet(x, y, Orientation.H) \
                              else " open"
                if x != 8 and self.b.isWallSetable(x, y, Orientation.H): 
                    val += " setable"
                    code = self.get_notation(x,y, Orientation.H)
                    self.links[self.calc_relative_horizontal_wall(x, y)] = code
                    self.tasks[code] = [self.set_wall, [x, y, Orientation.H]]

                self.classes[self.calc_relative_horizontal_wall(x, y)] = val

    def update_vertical_walls_to_classes(self):
        """Update the wall centers for html."""
        for y in range(0,9):
            for x in range(0,8):
                val = "Square Wall V Vpiece" + str(x) + "-" + str(y)

                if y != 0: val += " V" + str(x) + "-" + str(y-1)
                if y != 8: val += " V" + str(x) + "-" + str(y)

                val += " set" if self.b.wh.isWallSet(x, y, Orientation.V) \
                              else " open"
                
                if y != 8 and self.b.isWallSetable(x, y, Orientation.V):
                    val += " setable"
                    code = self.get_notation(x,y, Orientation.V)
                    self.links[self.calc_relative_vertical_wall(x, y)] = code
                    self.tasks[code] = [self.set_wall, [x, y, Orientation.V]]

                self.classes[self.calc_relative_vertical_wall(x, y)] = val

    def update_fields_to_classes(self):
        """Update the centers for html."""
        for y in range(0, 9):
            for x in range(0, 9):
                self.classes[self.calc_relative_field(x,y)] = \
                    "Square F F" + str(x) + "-" + str(y)

        p1_x, p1_y = self.b.ph.getPos(Player.P1)
        p2_x, p2_y = self.b.ph.getPos(Player.P2)    
        self.classes[self.calc_relative_field(p1_x, p1_y)] += " P1"
        self.classes[self.calc_relative_field(p2_x, p2_y)] += " P2"

        h_p1 = self.b.fh.getHeuristic(p1_x, p1_y, Player.P1)
        h_p2 = self.b.fh.getHeuristic(p2_x, p2_y, Player.P2)
        state = Playerstate((p1_x, p1_y), (p2_x, p2_y), self.currentPlayer, \
                            h_p1, h_p2)

        for m in self.b.getPlayerMoves(state):
            x, y = m[3].p1_pos if self.currentPlayer == Player.P1 \
                              else m[3].p2_pos
            
            pos_relative = self.calc_relative_field(x, y)

            move_code = self.get_notation(x, y)

            self.classes[pos_relative] += " Move "  
            self.classes[pos_relative] += move_code
            self.links[pos_relative] = move_code
            self.tasks[move_code] = [self.move_player, [m[0], m[1]]]

    def get_classes(self): return [self.classes[i] for i in range(17*17)]
    def get_links(self): return [self.links[i] for i in range(17*17)]
    def get_winner(self): return self.winner
    def get_gamelog(self):
        log = ""
        for turn in self.gamelog:
            log += "-"+ str(turn[0]) + " " + turn[1]
            if turn[2]:
                log += " " + turn[2]+ "\n"
            else:
                log += "\n"
        return log
    def get_undoable(self):
        return True if len(self.gamelog) != 0 else False
    def get_redoable(self):
        return True if len(self.redolog) != 0 else False
