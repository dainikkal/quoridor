"""Handles Playerstate including position and their heurisitc."""
from game.helper import Player


class Playerstate:
    """State of Players, and their heuristic."""

    def __init__(self, p1_pos, p2_pos, p_now, h_p1, h_p2, oldstate=None):
        """Initialize Playerstate with positions, heuristics, and old state.

        Args:
            p1_pos (tuple(x,y)): Positions of Player 1.
            p2_pos (tuple(x,y)): Positions of Player 2.
            p_now (int): ID of current Player.
            h_p1 (int): heuristic of Player 1.
            h_p2 (int): heuristic of Player 2.
            oldstate (Playerstate, optional): Previous state. Defaults to None.
        """
        self.p1_pos = p1_pos if p1_pos is not None else oldstate.p1_pos
        self.p2_pos = p2_pos if p2_pos is not None else oldstate.p2_pos
        self.p_now = p_now if p_now is not None else oldstate.p_now
        self.h_p1 = h_p1 if h_p1 is not None else oldstate.h_p1
        self.h_p2 = h_p2 if h_p2 is not None else oldstate.h_p2

    def newPlayerstate(state, new_pos, new_h):
        """Create a new Playerstate from a previous one.

        Args:
            state (Playerstate): previous Playerstate that should be updated.
            new_pos (tuple(x, y)): Position of changed player.
            new_h (int): new heuristic of changed player.

        Returns:
            Playerstate: updated Playerstate.
        """
        if state.p_now == Player.P1:
            return Playerstate(new_pos, None, Player.P2, new_h, None, state)
        return Playerstate(None, new_pos, Player.P1, None, new_h, state)

    def getPositionPnow(self):
        if self.p_now == Player.P1:
            return self.p1_pos
        return self.p2_pos

    def getPositionPOther(self):
        if self.p_now == Player.P1:
            return self.p2_pos
        return self.p1_pos

    def getHeuristicCurrentPlayer(self):
        if self.p_now == Player.P1:
            return self.h_p1
        return self.h_p2

    def getHeuristic(self, p):
        if Player.P1 == p:
            return self.h_p1
        return self.h_p2


Playerstate.newPlayerstate = staticmethod(Playerstate.newPlayerstate)
