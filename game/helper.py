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
    if dir == Dir.NoDir:
        return Dir.NoDir


BOARDSIZE = 8
BOARDSIZEMID = int(BOARDSIZE / 2)
HEURISTICJUMP = 100
INFINITE = 9999999
MINUSINFINITE = -INFINITE


def get_notation(x, y, o=None):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    if o == Orientation.H:
        orientation = "h"
    elif o == Orientation.V:
        orientation = "v"
    else:
        orientation = ""
    return letters[x] + str(y + 1) + orientation


def get_pos_key(x1, y1, x2, y2):
    return "%d%d%d%d" % (x1, y1, x2, y2)


def get_wallCount_key(c1, c2):
    s = ""
    s += str(c1) if c1 < 10 else "a"
    s += str(c2) if c2 < 10 else "a"
    return s


def splitWallKey(wallkey):
    l = []
    w = ""
    for char in wallkey:
        w += char
        if len(w) == 3:
            l.append(w)
            w = ""
    return l


def mergeWallKey(l):
    wk = ""
    for w in l:
        wk += w
    return wk


def sortWallKey(wallkey):
    splitWK = splitWallKey(wallkey)
    hWKs = [w for w in splitWK if w[2] == "h"]
    vWKs = [w for w in splitWK if w[2] == "v"]
    newsplitWK = []
    for w in hWKs + vWKs:
        newsplitWK.append(w[0] + w[1] + w[2])

    newsplitWK.sort(key=lambda x: (x[2], x[0], x[1]))

    newWallkey = mergeWallKey(newsplitWK)
    return newWallkey
