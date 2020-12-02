class Path():
  def __init__(self, x, y, isGoal = False): 
    self.pos = (x, y)
    self.isGoal = isGoal
    self.subPath = {}