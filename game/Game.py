"""Handles instance of a game."""
from game.Playerstate import Playerstate
from game.helper import BOARDSIZE, BOARDSIZEMID, Dir, Orientation, Player, mir
from game.Board import Board
import random


class Game:
    """Instance of a Game."""

    def __init__(self, log="", random=False):
        """Initialize Game class."""
        self.b = Board()
        self.currentPlayer = Player.P1
        self.walls_left = [10, 10]
        self.p1_walls_left = 10
        self.p2_walls_left = 10
        self.classes = {}
        self.links = {}
        self.tasks = {}
        self.winner = Player.Empty
        self.update_classes()
        self.redolog = []
        self.gamelog = []
        self.movelog = ([], [])
        self.load(log)
        if random:
            self.randomize()
            self.update_classes()

    def load(self, log):
        lines = log.split("-")
        for line in lines:
            parts = line.split(" ")
            if len(parts) < 2:
                continue
            self.redolog.append(parts[1])
            if len(parts) == 3:
                self.redolog.append(parts[2])
        self.redolog.reverse()
        while self.redolog:
            self.call_redo()

    def toggleplayer(self):
        """Change the current Player."""
        self.currentPlayer = Player.P2 if self.currentPlayer == Player.P1 else Player.P1
        self.update_classes()

    def get_notation(self, x, y, o=None):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        if o == Orientation.H:
            orientation = "h"
        elif o == Orientation.V:
            orientation = "v"
        else:
            orientation = ""
        return letters[x] + str(y + 1) + orientation

    def get_move_from_notation(self, code):
        letters = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7,
            "i": 8,
        }
        x = letters[code[0]]
        y = int(code[1]) - 1
        if len(code) == 2:
            o = None
        elif "v" == code[2]:
            o = Orientation.V
        elif "h" == code[2]:
            o = Orientation.H
        return x, y, o

    def randomize(self):
        """Randomizes boardstate in 4phases by calling each phase function."""
        p1_rx, p2_rx, p1_ry, p2_ry = [None] * 4
        while p1_rx == p2_rx and p1_ry == p2_ry:
            p1_rx = random.randint(0, BOARDSIZE)
            p1_ry = random.randint(1, BOARDSIZE)
            p2_rx = random.randint(0, BOARDSIZE)
            p2_ry = random.randint(0, BOARDSIZE - 1)
        random_pos = [[p1_rx, p1_ry], [p2_rx, p2_ry]]
        pos = [[BOARDSIZEMID, BOARDSIZE], [BOARDSIZEMID, 0]]

        self.random_prep(random_pos, pos)
        self.random_vertical(random_pos, pos)
        self.random_horizontal(random_pos, pos)
        self.random_walls()
        from game.Board import printcounter

        printcounter()
        pass

    def random_prep(self, random_pos, pos):
        """Phase 1 of randomizing the boardstate: 1 step towards their
        horizontal axis.

        Args:
            random_pos (List): random goal positions the players should reach
            pos (List): current position of the players.
        """
        if random_pos[Player.P1][0] < random_pos[Player.P2][0]:
            d = Dir.W
            pos[Player.P1][0] -= 1
            pos[Player.P2][0] += 1
        else:
            d = Dir.E
            pos[Player.P1][0] += 1
            pos[Player.P2][0] -= 1

        self.move_player(d)
        self.toggleplayer()
        self.move_player(mir(d))
        self.toggleplayer()

    def random_vertical(self, random_pos, pos):
        """Phase 2 of randomizing the boardstate: Moves Players to their
        vertical axis.

        Args:
            random_pos (List): random goal positions the players should reach
            pos (List): current position of the players.
        """
        reached = [
            (pos[Player.P1][1] == random_pos[Player.P1][1]),
            (pos[Player.P2][1] == random_pos[Player.P2][1]),
        ]
        waiting = [False] * 2
        dirs = [Dir.N, Dir.S]
        dodge = [Dir.E, Dir.E]
        while (False in reached) or (True in waiting):
            self.random_move(
                random_pos, pos, reached, waiting, dodge, self.currentPlayer, dirs, 1
            )

    def random_horizontal(self, random_pos, pos):
        """Phase 3 of randomizing the boardstate: Moves Players to their
        horizontal axis.

        Args:
            random_pos (List): random goal positions the players should reach
            pos (List): current position of the players.
        """
        reached = [
            (pos[Player.P1][0] == random_pos[Player.P1][0]),
            (pos[Player.P2][0] == random_pos[Player.P2][0]),
        ]
        waiting = [False] * 2
        dirs = [Dir.E, Dir.E]
        if pos[Player.P1][0] > random_pos[Player.P1][0]:
            dirs[Player.P1] = Dir.W
        if pos[Player.P2][0] > random_pos[Player.P2][0]:
            dirs[Player.P2] = Dir.W
        if random_pos[Player.P1][1] != random_pos[Player.P2][1]:
            dodge = [Dir.E, Dir.E]
            if random_pos[Player.P1][0] == BOARDSIZE:
                dodge[Player.P1] = Dir.W
            if random_pos[Player.P2][0] == BOARDSIZE:
                dodge[Player.P2] = Dir.W
        else:
            dodge = [Dir.S, Dir.N]
            if random_pos[Player.P1][1] == BOARDSIZE:
                dodge[Player.P1] = Dir.N
            if random_pos[Player.P2][1] == 0:
                dodge[Player.P2] = Dir.S
        while (False in reached) or (True in waiting):
            self.random_move(
                random_pos, pos, reached, waiting, dodge, self.currentPlayer, dirs, 0
            )

    def random_walls(self):
        """Phase 4 of randomizing the boardstate: Sets Walls till all walls
        are set.
        """
        while self.p1_walls_left + self.p2_walls_left > 0:
            walls = self.b.getAllSetableWalls()
            r = random.randint(0, len(walls) - 1)
            x, y, o = walls[r]
            if self.currentPlayer == Player.P1:
                self.p1_walls_left -= 1
            else:
                self.p2_walls_left -= 1
            self.set_wall(x, y, o)
            self.toggleplayer()

    def random_move(self, rpos, pos, reached, wait, dodge, p, dirs, axis):
        if reached[p]:
            wait[p] = True
            d = dodge[p]
        elif wait[p]:
            wait[p] = False
            d = mir(dodge[p])
        else:
            d = dirs[p]

        if d == Dir.N:
            pos[p][1] -= 1
        if d == Dir.E:
            pos[p][0] += 1
        if d == Dir.S:
            pos[p][1] += 1
        if d == Dir.W:
            pos[p][0] -= 1
        reached[p] = pos[p][axis] == rpos[p][axis] and (not wait[p])

        self.move_player(d)
        self.toggleplayer()

    def compute_winner_no_wall(self):

        p1_x, p1_y = self.b.ph.getPos(Player.P1)
        p2_x, p2_y = self.b.ph.getPos(Player.P2)
        self.classes[self.calc_relative_field(p1_x, p1_y)] += " P1"
        self.classes[self.calc_relative_field(p2_x, p2_y)] += " P2"

        h_p1 = self.b.fh.getHeuristic(p1_x, p1_y, Player.P1)
        h_p2 = self.b.fh.getHeuristic(p2_x, p2_y, Player.P2)
        state = Playerstate((p1_x, p1_y), (p2_x, p2_y), self.currentPlayer, h_p1, h_p2)

        self.b.compute_winner_no_wall(state)
        pass

    def call_undo(self):
        p, move = self.prepare_undo()
        self.execute_undo(p, move)

    def prepare_undo(self):
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
        return p, move

    def execute_undo(self, p, move):
        """Undos action

        Args:
            p ([type]): [description]
            move ([type]): [description]
        """
        x, y, o = self.get_move_from_notation(move)

        if o != None:
            self.increment_currentplayer_walls(p)
            self.b.setWall(x, y, o, False)
        else:
            d1, d2 = self.movelog[p].pop()
            d1_rev = mir(d1)
            if d2 != Dir.NoDir:
                d2_rev = mir(d2)
                self.b.movePlayer(p, d2_rev, d1_rev)
            else:
                self.b.movePlayer(p, d1_rev)

        self.redolog.append(move)
        self.toggleplayer()

    def call_redo(self):
        """Redos last undone action."""
        redo_notation = self.redolog.pop()
        self.execute_action(redo_notation, True)

    def execute_action(self, action_code, redo=False):
        """
        Calls an function pointer by inputing the action code.

        Args:
            action_code (string): key for the dict with the function pointers.
        """
        if action_code not in self.tasks.keys():
            return

        if not redo:
            self.redolog.clear()

        action, params = self.tasks[action_code]
        action(*params)

        self.toggleplayer()
        self.compute_winner_no_wall()

    def move_player(self, d, d2=Dir.NoDir):
        """Moves player and check for win."""
        self.b.movePlayer(self.currentPlayer, d, d2)

        turnnumber = len(self.gamelog)
        if self.currentPlayer == Player.P1:
            x, y = self.b.ph.getPos(Player.P1)
            action = self.get_notation(x, y, None)
            self.gamelog.append([turnnumber + 1, action, None])
            h = self.b.fh.getHeuristic(x, y, Player.P1)
        else:
            turn = self.gamelog[turnnumber - 1]
            x, y = self.b.ph.getPos(Player.P2)
            turn[2] = self.get_notation(x, y, None)
            h = self.b.fh.getHeuristic(x, y, Player.P2)
        if h == 0:
            self.winner = self.currentPlayer

        self.movelog[self.currentPlayer].append([d, d2])

    def set_wall(self, x, y, o):
        """sets wall in with coordinates and orientation"""
        self.decrement_currentplayer_walls()
        self.b.setWall(x, y, o)

        turnnumber = len(self.gamelog)
        action = self.get_notation(x, y, o)
        if self.currentPlayer == Player.P1:
            self.gamelog.append([turnnumber + 1, action, None])
        else:
            turn = self.gamelog[turnnumber - 1]
            turn[2] = action

    def currentplayer_walls_left(self):
        return self.walls_left[self.currentPlayer]

    def increment_currentplayer_walls(self, p):
        self.walls_left[p] += 1

    def decrement_currentplayer_walls(self):
        self.walls_left[self.currentPlayer] -= 1

    def update_classes(self):
        """Updates the classes for html."""
        self.tasks.clear()
        for i in range(17 * 17):
            self.links[i] = ""
        self.update_fields_to_classes()
        self.update_wallcenters_to_classes()
        self.update_horizontal_walls_to_classes()
        self.update_vertical_walls_to_classes()

    def calc_relative_horizontal_wall(self, x, y):
        return (y * 2 + 1) * 17 + x * 2

    def calc_relative_vertical_wall(self, x, y):
        return y * 2 * 17 + x * 2 + 1

    def calc_relative_field(self, x, y):
        return x * 2 + 17 * 2 * y

    def update_wallcenters_to_classes(self):
        """Update the wall centers for html."""
        for y in range(0, 8):
            for x in range(0, 8):
                val = "Square Wall C"

                val += " V" + str(x) + "-" + str(y)
                val += " H" + str(x) + "-" + str(y)

                val += " set" if self.b.wh.isCenterSet(x, y) else " open"

                self.classes[(y * 2 + 1) * 17 + x * 2 + 1] = val

    def update_horizontal_walls_to_classes(self):
        """Update the horizontal wall for html."""
        for y in range(0, 8):
            for x in range(0, 9):
                val = "Square Wall H Hpiece" + str(x) + "-" + str(y)

                if x != 0:
                    val += " H" + str(x - 1) + "-" + str(y)
                if x != 8:
                    val += " H" + str(x) + "-" + str(y)

                val += " set" if self.b.wh.isWallSet(x, y, Orientation.H) else " open"
                if (
                    x != 8
                    and self.b.isWallSetable(x, y, Orientation.H)
                    and self.currentplayer_walls_left() > 0
                ):
                    val += " setable"
                    code = self.get_notation(x, y, Orientation.H)
                    self.links[self.calc_relative_horizontal_wall(x, y)] = code
                    self.tasks[code] = [self.set_wall, [x, y, Orientation.H]]

                self.classes[self.calc_relative_horizontal_wall(x, y)] = val

    def update_vertical_walls_to_classes(self):
        """Update the wall centers for html."""
        for y in range(0, 9):
            for x in range(0, 8):
                val = "Square Wall V Vpiece" + str(x) + "-" + str(y)

                if y != 0:
                    val += " V" + str(x) + "-" + str(y - 1)
                if y != 8:
                    val += " V" + str(x) + "-" + str(y)

                val += " set" if self.b.wh.isWallSet(x, y, Orientation.V) else " open"

                if (
                    y != 8
                    and self.b.isWallSetable(x, y, Orientation.V)
                    and self.currentplayer_walls_left() > 0
                ):
                    val += " setable"
                    code = self.get_notation(x, y, Orientation.V)
                    self.links[self.calc_relative_vertical_wall(x, y)] = code
                    self.tasks[code] = [self.set_wall, [x, y, Orientation.V]]

                self.classes[self.calc_relative_vertical_wall(x, y)] = val

    def update_fields_to_classes(self):
        """Update the centers for html."""
        for y in range(0, 9):
            for x in range(0, 9):
                self.classes[self.calc_relative_field(x, y)] = (
                    "Square F F" + str(x) + "-" + str(y)
                )

        p1_x, p1_y = self.b.ph.getPos(Player.P1)
        p2_x, p2_y = self.b.ph.getPos(Player.P2)
        self.classes[self.calc_relative_field(p1_x, p1_y)] += " P1"
        self.classes[self.calc_relative_field(p2_x, p2_y)] += " P2"

        h_p1 = self.b.fh.getHeuristic(p1_x, p1_y, Player.P1)
        h_p2 = self.b.fh.getHeuristic(p2_x, p2_y, Player.P2)
        state = Playerstate((p1_x, p1_y), (p2_x, p2_y), self.currentPlayer, h_p1, h_p2)

        for m in self.b.getPlayerMoves(state):
            x, y = m[3].p1_pos if self.currentPlayer == Player.P1 else m[3].p2_pos

            pos_relative = self.calc_relative_field(x, y)

            move_code = self.get_notation(x, y)

            self.classes[pos_relative] += " Move "
            self.classes[pos_relative] += move_code
            self.links[pos_relative] = move_code
            self.tasks[move_code] = [self.move_player, [m[0], m[1]]]

    def get_classes(self):
        return [self.classes[i] for i in range(17 * 17)]

    def get_links(self):
        return [self.links[i] for i in range(17 * 17)]

    def get_winner(self):
        return self.winner

    def get_gamelog(self):
        """Return printable game log.

        Returns:
            string: game log.
        """
        log = ""
        for turn in self.gamelog:
            log += "-" + str(turn[0]) + " " + turn[1]
            if turn[2]:
                log += " " + turn[2] + "\n"
            else:
                log += "\n"
        return log

    def get_undoable(self):
        return True if len(self.gamelog) != 0 else False

    def get_redoable(self):
        return True if len(self.redolog) != 0 else False

    def get_currentplayer(self):
        return self.currentPlayer

    def get_p1_wallsCount(self):
        return self.p1_walls_left

    def get_p2_wallsCount(self):
        return self.p2_walls_left
