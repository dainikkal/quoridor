class Player():
  Empty = 0
  P1 = 1
  P2 = 2

class Dir():
  N = 0
  E = 1
  S = 2
  W = 3

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

BOARDSIZE = 4
BOARDSIZEMID = 2
INFINITE = 9999999