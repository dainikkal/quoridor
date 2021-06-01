"""Module with Enums."""


class Player:
    """Enum for player."""

    Empty = -1
    P1 = 0
    P2 = 1


class Dir:
    """Enum for Directions."""

    NoDir = -1
    N = 0
    E = 1
    S = 2
    W = 3
    NE = [1, 0]
    NW = [0, 0]
    SE = [1, 1]
    SW = [0, 1]


class UpDown:
    """Enum for Up and Down."""

    U = 0  # Up
    D = 1  # Down


class LeftRight:
    """Enum for Left and Right."""

    L = 0
    R = 1


class Orientation:
    """Enum for Orientation."""

    H = 0
    V = 1


def mir(dir):
    """Mirrors the Directions.

    Args:
        dir (int): Direction to be mirrored

    Returns:
        int: return mirror Direction.
    """

    if dir == Dir.N:
        return Dir.S
    if dir == Dir.E:
        return Dir.W
    if dir == Dir.S:
        return Dir.N
    if dir == Dir.W:
        return Dir.E


BOARDSIZE = 8
BOARDSIZEMID = int(BOARDSIZE / 2)
HEURISTICJUMP = 100
INFINITE = 9999999
MINUSINFINITE = -INFINITE
