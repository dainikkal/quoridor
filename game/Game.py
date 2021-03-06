"""Handles instance of a game."""
from game.Playerstate import Playerstate
from game.helper import (
    BOARDSIZE,
    BOARDSIZEMID,
    Dir,
    Orientation,
    Player,
    get_wallCount_key,
    mir,
    get_notation,
    get_pos_key,
    sortWallKey,
)
from game.Board import Board
from map import cacheMap
import random


# intend = ""


class Game:
    """Instance of a Game."""

    def __init__(self, log="", random=False):
        """Initialize Game class."""
        self.b = Board()
        # cacheMap = {}
        self.currentPlayer = Player.P1
        self.walls_left = [10, 10]
        self.classes = {}
        self.links = {}
        self.tasks = {}
        self.winner = Player.Empty
        self.helpactive = True
        self.autoplay = [False, False]
        self.bestmove = ""
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
            if len(parts) >= 3:
                self.redolog.append(parts[2])
        self.redolog.reverse()
        while self.redolog:
            self.call_redo()

    def otherPlayer(self, p=None):
        p = self.currentPlayer if p is None else p
        return Player.P1 if p == Player.P2 else Player.P2

    def toggleplayer(self, update=False):
        """Change the current Player."""
        self.currentPlayer = self.otherPlayer()
        if update:
            self.update_classes()

    def get_wallsCountLeft(self, p=None):
        p = self.currentPlayer if None else p
        return self.walls_left[p]

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
        if len(code) == 2:
            o = None
        elif "v" == code[2]:
            o = Orientation.V
        elif "h" == code[2]:
            o = Orientation.H
        y = BOARDSIZE - int(code[1]) + (1 if o == None else 0)
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
        self.toggleplayer(update=False)
        self.move_player(mir(d))
        self.toggleplayer(update=False)

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
        while self.walls_left[0] + self.walls_left[1] > 0:
            walls = self.b.getAllSetableWalls()
            r = random.randint(0, len(walls) - 1)
            x, y, o = walls[r]
            self.set_wall(x, y, o)
            self.toggleplayer(update=False)

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
        self.toggleplayer(update=False)

    def call_undo(self):
        self.winner = Player.Empty

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

    def find_best_move(self, wallkey, wallCountKey, state, init=0):
        if not isinstance(state, Playerstate):
            raise

        global cacheMap
        winner = Player.Empty

        # - Check if already been here.
        cp = state.p_now
        cpStr = str(cp)
        posKey = get_pos_key(
            state.p1_pos[0],
            state.p1_pos[1],
            state.p2_pos[0],
            state.p2_pos[1],
        )

        if posKey in cacheMap[wallkey][wallCountKey][cpStr]:
            if init == 0:
                return cacheMap[wallkey][wallCountKey][cpStr][posKey]["winner"]
        else:
            cacheMap[wallkey][wallCountKey][cpStr][posKey] = {
                "winner": Player.Empty,
                "moves": [],
            }

        # - Check if cp wins
        moves = self.b.getPlayerMoves(state)
        hdifs = [self.get_HeursiticDiff(state, x[3]) for x in moves]
        sortedmoves = sorted(zip(hdifs, moves), reverse=True)

        min_h = sortedmoves[0][1][2]
        good_moves = []

        if min_h == 0:
            for _, m in sortedmoves:
                if m[2] == 0:
                    good_moves.append([0, m])
            cacheMap[wallkey][wallCountKey][cpStr][posKey]["moves"] = good_moves
            cacheMap[wallkey][wallCountKey][cpStr][posKey]["winner"] = cp
            return cp

        # - Check options
        #        global intend
        #
        #        def p_print(p):
        #            if p == Player.P1:
        #                return "\033[94m" + "P1" + "\033[0m"
        #            return "\033[91m" + "P2" + "\033[0m"
        #
        #        def dir_print(p):
        #            if p == Dir.N:
        #                return "\033[91m" + "N" + "\033[0m"
        #            if p == Dir.S:
        #                return "\033[92m" + "S" + "\033[0m"
        #            if p == Dir.E:
        #                return "\033[93m" + "E" + "\033[0m"
        #            if p == Dir.W:
        #                return "\033[94m" + "W" + "\033[0m"
        #            return ""
        #
        #        def codeinit(code, init):
        #            if init == 2:
        #                return "\033[92m" + code + "\033[0m"
        #            if init == 1:
        #                return "\033[93m" + code + "\033[0m"
        #            return code

        for h_dif, m in sortedmoves:
            w = Player.Empty
            if m[2] > state.getHeuristicCurrentPlayer():
                continue
            # intend += "  "
            # print(
            #    intend
            #    + p_print(cp)
            #    + " "
            #    + dir_print(m[0])
            #    + " "
            #    + dir_print(m[1])
            #    + " "
            #    + codeinit(posKey, init)
            #    + " "
            #    + "\033[96m"
            #    + str(m[2])
            #    + "\033[0m"
            #    + " "
            #    + "\033[97m"
            #    + str(h_dif)
            #    + "\033[0m"
            # )
            if init == 2:
                w = self.find_best_move(wallkey, wallCountKey, m[3], 1)
            elif h_dif < sortedmoves[0][0]:
                # intend = intend[:-2]
                continue
            elif -1 < h_dif and h_dif < 2:
                w = self.find_best_move(wallkey, wallCountKey, m[3])
            elif h_dif >= 1:
                w = cp
            else:
                w = self.otherPlayer(cp)

            if w == cp:
                good_moves.append((h_dif, m))
                winner = cp
            # intend = intend[:-2]

        good_moves.sort()

        winner = cp if winner == cp else self.otherPlayer(cp)

        cacheMap[wallkey][wallCountKey][cpStr][posKey]["winner"] = winner
        cacheMap[wallkey][wallCountKey][cpStr][posKey]["moves"] += good_moves
        return winner

    def get_HeursiticDiff(self, state, state2):
        if not isinstance(state, Playerstate):
            return Player.Empty
        if not isinstance(state2, Playerstate):
            return Player.Empty

        p_now = state.p_now
        p_other = self.otherPlayer(p_now)
        h_now = state2.getHeuristic(p_now)
        h_other = state.getHeuristic(p_other)
        return h_other - h_now

    def wrapper_find_best_move(self):
        global cacheMap
        wallkey = sortWallKey(self.b.wh.getWallsAsStringKey())
        if wallkey not in cacheMap:
            cacheMap[wallkey] = {}

        wallCountKey = get_wallCount_key(self.walls_left[0], self.walls_left[1])
        if wallCountKey not in cacheMap[wallkey]:
            cacheMap[wallkey][wallCountKey] = {}
            cacheMap[wallkey][wallCountKey][str(Player.P1)] = {}
            cacheMap[wallkey][wallCountKey][str(Player.P2)] = {}

        p1_pos = self.find_pos(Player.P1)
        p2_pos = self.find_pos(Player.P2)
        p1_h = self.find_heuristic(p1_pos[0], p1_pos[1], Player.P1)
        p2_h = self.find_heuristic(p2_pos[0], p2_pos[1], Player.P2)
        state = Playerstate(p1_pos, p2_pos, self.currentPlayer, p1_h, p2_h)

        w = self.find_best_move(wallkey, wallCountKey, state, 2)
        return w

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
        self.toggleplayer(update=True)

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

        self.toggleplayer(update=True)

        if self.autoplay[self.currentPlayer] and redo == False:
            self.playautomatically()
        # self.compute_winner_no_wall()

    def playautomatically(self):
        self.execute_action(self.bestmove)

    def move_player(self, d, d2=Dir.NoDir):
        """Moves player and check for win."""
        self.b.movePlayer(self.currentPlayer, d, d2)

        turnnumber = len(self.gamelog)
        if self.currentPlayer == Player.P1:
            x, y = self.find_pos(Player.P1)
            action = get_notation(x, y, None)
            self.gamelog.append([turnnumber + 1, action, None])
            h = self.find_heuristic(x, y, Player.P1)
        else:
            turn = self.gamelog[turnnumber - 1]
            x, y = self.find_pos(Player.P2)
            turn[2] = get_notation(x, y, None)
            h = self.find_heuristic(x, y, Player.P2)
        if h == 0:
            self.winner = self.currentPlayer

        self.movelog[self.currentPlayer].append([d, d2])

    def set_wall(self, x, y, o):
        """sets wall in with coordinates and orientation"""
        self.decrement_currentplayer_walls()
        self.b.setWall(x, y, o)

        turnnumber = len(self.gamelog)
        action = get_notation(x, y, o)
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
        self.bestmove = ""
        self.wrapper_find_best_move()
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
                    and self.winner == Player.Empty
                ):
                    val += " setable"
                    code = get_notation(x, y, Orientation.H)
                    self.links[self.calc_relative_horizontal_wall(x, y)] = code
                    self.tasks[code] = [self.set_wall, [x, y, Orientation.H]]

                if x == 8:
                    if (
                        self.b.isWallSetable(x - 1, y, Orientation.H)
                        and self.currentplayer_walls_left() > 0
                        and self.winner == Player.Empty
                    ):
                        val += " setable"
                        code = get_notation(x - 1, y, Orientation.H)
                        self.links[self.calc_relative_horizontal_wall(x - 1, y)] = code

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
                    and self.winner == Player.Empty
                ):
                    val += " setable"
                    code = get_notation(x, y, Orientation.V)
                    self.links[self.calc_relative_vertical_wall(x, y)] = code
                    self.tasks[code] = [self.set_wall, [x, y, Orientation.V]]

                if y == 8:

                    if (
                        self.b.isWallSetable(x, y - 1, Orientation.V)
                        and self.currentplayer_walls_left() > 0
                        and self.winner == Player.Empty
                    ):
                        val += " setable"
                        code = get_notation(x, y - 1, Orientation.V)
                        self.links[self.calc_relative_vertical_wall(x, y - 1)] = code

                self.classes[self.calc_relative_vertical_wall(x, y)] = val

    def update_fields_to_classes(self):
        """Update the centers for html."""
        for y in range(0, 9):
            for x in range(0, 9):
                self.classes[self.calc_relative_field(x, y)] = (
                    "Square F F" + str(x) + "-" + str(y)
                )

        p1_x, p1_y = self.find_pos(Player.P1)
        p2_x, p2_y = self.find_pos(Player.P2)
        self.classes[self.calc_relative_field(p1_x, p1_y)] += " P1"
        self.classes[self.calc_relative_field(p2_x, p2_y)] += " P2"

        if self.winner != Player.Empty:
            return

        h_p1 = self.find_heuristic(p1_x, p1_y, Player.P1)
        h_p2 = self.find_heuristic(p2_x, p2_y, Player.P2)
        state = Playerstate((p1_x, p1_y), (p2_x, p2_y), self.currentPlayer, h_p1, h_p2)

        wallkey = sortWallKey(self.b.wh.getWallsAsStringKey())
        cpStr = str(self.currentPlayer)
        posKey = get_pos_key(p1_x, p1_y, p2_x, p2_y)
        wallCountKey = get_wallCount_key(self.walls_left[0], self.walls_left[1])
        goodmoves = cacheMap[wallkey][wallCountKey][cpStr][posKey]["moves"]
        if len(goodmoves) > 0:
            goodmoves = [x for _, x in goodmoves]

        moves = self.b.getPlayerMoves(state)
        moves.sort(key=lambda x: x[2])
        min_h = moves[0][2]
        bestmovetier = 0
        for m in moves:
            x, y = m[3].p1_pos if self.currentPlayer == Player.P1 else m[3].p2_pos

            pos_relative = self.calc_relative_field(x, y)

            move_code = get_notation(x, y)
            gmove = self.inMoves(m, goodmoves)
            bettermove = m[2] == min_h

            if ((gmove and bettermove) or m[2] == 0) and bestmovetier < 4:
                self.bestmove = move_code
                bestmovetier = 4

            if ((gmove and not bettermove) or m[2] == 0) and bestmovetier < 3:
                self.bestmove = move_code
                bestmovetier = 3

            if ((not gmove and bettermove) or m[2] == 0) and bestmovetier < 2:
                self.bestmove = move_code
                bestmovetier = 2

            if ((not gmove and not bettermove) or m[2] == 0) and bestmovetier < 1:
                self.bestmove = move_code
                bestmovetier = 1

            if self.helpactive:
                if (gmove and bettermove) or m[2] == 0:
                    self.classes[pos_relative] += " GoodWinningMove "
                if gmove and not bettermove:
                    self.classes[pos_relative] += " WinningMove "
                if not gmove and bettermove:
                    self.classes[pos_relative] += " GoodMove "
                if not gmove and not bettermove:
                    self.classes[pos_relative] += " Move "
            else:
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
        return self.walls_left[0]

    def get_p2_wallsCount(self):
        return self.walls_left[1]

    def find_heuristic(self, x, y, p):
        if p == Player.Empty:
            p = self.currentPlayer
        return self.b.fh.getHeuristic(x, y, p)

    def find_pos(self, p):
        if p == Player.Empty:
            p = self.currentPlayer
        return self.b.ph.getPos(p)

    def inMoves(self, m, moves):
        for move in moves:
            if m[0:2] == move[0:2]:
                return True

        return False

    def toggleHelp(self):
        self.helpactive = not self.helpactive
        self.update_classes()

    def get_helpactive(self):
        return self.helpactive

    def toggleAutoP1(self):
        self.autoplay[Player.P1] = not self.autoplay[Player.P1]
        self.update_classes()
        if self.autoplay[self.currentPlayer]:
            self.playautomatically()

    def get_autop1(self):
        return self.autoplay[Player.P1]

    def toggleAutoP2(self):
        self.autoplay[Player.P2] = not self.autoplay[Player.P2]
        self.update_classes()
        if self.autoplay[self.currentPlayer]:
            self.playautomatically()

    def get_autop2(self):
        return self.autoplay[Player.P2]
