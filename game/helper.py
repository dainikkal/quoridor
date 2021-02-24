class Player():
  Empty = -1
  P1 = 0
  P2 = 1

class Dir():
  NoDir = -1
  N = 0
  E = 1
  S = 2
  W = 3
  NE = [1, 0]
  NW = [0, 0]
  SE = [1, 1]
  SW = [0, 1]

class UpDown():
  U = 0#Up
  D = 1#Down
class LeftRight():
  L = 0#Up
  R = 1#Down

class Orientation():
  H = 0
  V = 1

def mir(dir):
  if dir == Dir.N: return Dir.S
  if dir == Dir.E: return Dir.W
  if dir == Dir.S: return Dir.N
  if dir == Dir.W: return Dir.E

class WallLegality():
  Free = 0x0
  Locked = 0xF
  
  NLocked = 0x1
  ELocked = 0x2
  SLocked = 0x4
  WLocked = 0x8

  NELocked = 0x3
  NSLocked = 0x5
  ESLocked = 0x6
  NWLocked = 0x9
  EWLocked = 0xA
  SWLocked = 0xC
  
  NFree = 0xE
  SFree = 0xB
  WFree = 0x7
  EFree = 0xD

class CycledetectionRetVal():
  noContact = 0
  Border = 1
  Cycle = 2

BOARDSIZE = 8
BOARDSIZEMID = int(BOARDSIZE / 2)
HEURISTICJUMP = 100
INFINITE = 9999999
MINUSINFINITE = -INFINITE