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


class WallTranslation:
    """Enum for Directions of Walltranslation."""

    Nope = 0
    Turned = 1
    Horizontally = 2
    Vertically = 3


def get_notation(x, y, o=None):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    if o == Orientation.H:
        orientation = "h"
    elif o == Orientation.V:
        orientation = "v"
    else:
        orientation = ""
    return letters[x] + str(y + 1) + orientation


def get_pos_key(x1, y1, x2, y2, translation=WallTranslation.Nope):
    n_x1, n_y1, n_x2, n_y2 = x1, y1, x2, y2

    if translation == WallTranslation.Nope:
        return "%d%d%d%d" % (n_x1, n_y1, n_x2, n_y2)

    if translation == WallTranslation.Vertically:
        n_x1, n_x2 = x1, x2
        n_y1 = BOARDSIZE - y1
        n_y2 = BOARDSIZE - y2
        return "%d%d%d%d" % (n_x1, n_y1, n_x2, n_y2)

    if translation == WallTranslation.Horizontally:
        n_y1, n_y2 = y1, y2
        n_x1 = BOARDSIZE - x1
        n_x2 = BOARDSIZE - x2
        return "%d%d%d%d" % (n_x1, n_y1, n_x2, n_y2)

    if translation == WallTranslation.Turned:
        n_x1 = BOARDSIZE - x1
        n_y1 = BOARDSIZE - y1
        n_x2 = BOARDSIZE - x2
        n_y2 = BOARDSIZE - y2
        return "%d%d%d%d" % (n_x1, n_y1, n_x2, n_y2)


def get_wallCount_key(c1, c2):
    s = ""
    s += str(c1) if c1 < 10 else "a"
    s += str(c2) if c2 < 10 else "a"
    return s


def findWallkeyTranslation(wallkey):
    wallKey180 = check180Rotation(wallkey)
    wallKeyHori = checkMirroredHorizontally(wallkey)
    wallKeyVerti = checkMirroredVertically(wallkey)

    return compareWallkeys(wallkey, wallKey180, wallKeyHori, wallKeyVerti)


def compareWallkeys(wallkey, wallkey180, wallkeyHori, wallkeyVerti):
    if wallkey == min([wallkey, wallkey180, wallkeyHori, wallkeyVerti]):
        return (wallkey, WallTranslation.Nope)

    if wallkey180 == min([wallkey, wallkey180, wallkeyHori, wallkeyVerti]):
        return wallkey180, WallTranslation.Turned

    if wallkeyHori == min([wallkey, wallkey180, wallkeyHori, wallkeyVerti]):
        return wallkeyHori, WallTranslation.Horizontally

    if wallkeyVerti == min([wallkey, wallkey180, wallkeyHori, wallkeyVerti]):
        return wallkeyVerti, WallTranslation.Vertically


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


def mirrornumber(number):
    return 9 - number


def mirrorletter(letter):
    if letter == "a":
        return "h"
    if letter == "b":
        return "g"
    if letter == "c":
        return "f"
    if letter == "d":
        return "e"
    if letter == "e":
        return "d"
    if letter == "f":
        return "c"
    if letter == "g":
        return "b"
    if letter == "h":
        return "a"


def check180Rotation(wallkey):
    splitWK = splitWallKey(wallkey)
    hWKs = [w for w in splitWK if w[2] == "h"]
    vWKs = [w for w in splitWK if w[2] == "v"]

    newsplitWK = []
    for w in hWKs + vWKs:
        w0 = mirrorletter(w[0])
        w1 = str(mirrornumber(int(w[1])))
        w2 = w[2]
        newsplitWK.append(w0 + w1 + w2)
    newsplitWK.sort()

    newWallkey = mergeWallKey(newsplitWK)
    return newWallkey


def checkMirroredHorizontally(wallkey):
    splitWK = splitWallKey(wallkey)
    hWKs = [w for w in splitWK if w[2] == "h"]
    vWKs = [w for w in splitWK if w[2] == "v"]

    newsplitWK = []
    for w in hWKs + vWKs:
        w0 = mirrorletter(w[0])
        w1 = w[1]
        w2 = w[2]
        newsplitWK.append(w0 + w1 + w2)
    newsplitWK.sort()

    newWallkey = mergeWallKey(newsplitWK)
    return newWallkey


def checkMirroredVertically(wallkey):
    splitWK = splitWallKey(wallkey)
    hWKs = [w for w in splitWK if w[2] == "h"]
    vWKs = [w for w in splitWK if w[2] == "v"]
    newsplitWK = []
    for w in hWKs + vWKs:
        w0 = w[0]
        w1 = str(mirrornumber(int(w[1])))
        w2 = w[2]
        newsplitWK.append(w0 + w1 + w2)

    newsplitWK.sort()

    newWallkey = mergeWallKey(newsplitWK)
    return newWallkey
    pass
