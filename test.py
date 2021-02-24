from game.helper import BOARDSIZE
from random import seed, random
import time
seed(1)

keys = [(int(random()*BOARDSIZE),int(random()*BOARDSIZE))  for _ in range(10000000)]

dic = {(x,y) : y*BOARDSIZE + x for x in range(BOARDSIZE) for y in range(BOARDSIZE)}
lis = [[y*BOARDSIZE + x for y in range(BOARDSIZE)] for x in range(BOARDSIZE)]

start1 = time.time_ns()
res1 = [dic[(kx, ky)] for kx, ky in keys]
stop1 = time.time_ns() - start1

start2 = time.time_ns()
res2 = [lis[kx][ky] for kx, ky in keys]
stop2 = time.time_ns() - start2

print(start1, stop1)
print(start2, stop2)