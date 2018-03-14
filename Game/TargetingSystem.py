import Functions as func

class TargetingSystem:

  def __init__(self, own):
    self.owner = own
    self.currentTarget = None

  #each time this method is called the opponents in the owner's sensory memory are examined and the closest  is assigned to m_pCurrentTarget. if there are no opponents that have had their memory records updated within the memory span of the owner then the current target is set to null
  def update(self):
    closestDistSoFar = float('Inf')
    self.currentTarget = None
    sensedBots = self.owner.sensoryMemory.getListOfRecentlySensedOpponents()
    for bot in sensedBots:
      if bot.isAlive and bot != self.owner:
        dist = func.distanceSq(bot.position, self.owner.position)
        if dist < closestDistSoFar:
          closestDistSoFar = dist
          self.currentTarget = bot

  #returns true if there is a currently assigned target
  def isTargetPresent(self):
    return self.currentTarget != None

  #returns true if the target is within the field of view of the owner
  def isTargetWithinFOV(self):
    return self.owner.sensoryMemory.isOpponentWithinFOV(self.currentTarget)

  #returns true if there is unobstructed line of sight between the target and the owner
  def isTargetShootable(self):
    return self.owner.sensoryMemory.isOpponentShootable(self.currentTarget)

  #returns the position the target was last seen. Throws an exception if there is no target currently assigned
  def getLastRecordedPosition(self):
    return self.owner.sensoryMemory.getLastRecordedPositionOfOpponent(self.currentTarget)

  #returns the amount of time the target has been in the field of view
  def getTimeTargetHasBeenVisible(self):
    return self.owner.sensoryMemory.getTimeOpponentHasBeenVisible(self.currentTarget)

  #returns the amount of time the target has been out of view
  def getTimeTargetHasBeenOutOfView(self):
    return self.owner.sensoryMemory.getTimeOpponentHasBeenOutOfView(self.currentTarget)

  #sets the target pointer to null
  def clearTarget(self):
    self.currentTarget = None
