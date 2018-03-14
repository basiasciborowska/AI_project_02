import pygame
import Functions as func
import MemoryRecord as mr

class SensoryMemory:

  def __init__(self, own, ms):
    #the owner of this instance
    self.owner = own
    #this container is used to simulate memory of sensory events. A MemoryRecord is created for each opponent in the environment. Each record is updated whenever the opponent is encountered. (when it is seen or heard)
    self.memoryMap = [None] * self.owner.world.playersNumber
    #a bot has a memory span equivalent to this value. When a bot requests a list of all recently sensed opponents this value is used to determine if the bot is able to remember an opponent or not.
    self.memorySpan = ms

  #this methods checks to see if there is an existing record for pBot. If not a new MemoryRecord record is made and added to the memory map.(called by UpdateWithSoundSource & UpdateVision)
  def makeNewRecordIfNotAlreadyPresent(self, player):
    #check to see if this Opponent already exists in the memory. If it doesn't, create a new record
    if self.memoryMap[player.id] == None:
      self.memoryMap[player.id] = mr.MemoryRecord()

  #this removes a bot's record from memory
  def removeBotFromMemory(self, player):
    if self.memoryMap[player.id] != None:
      self.memoryMap[player.id] = None

  #this method is used to update the memory map whenever an opponent makes a noise
  def updateWithSoundSource(self, playerNoiseMaker):
    pass

  #this method iterates through all the opponents in the game world and updates the records of those that are in the owner's FOV
  def updateVision(self):
    #for each bot in the world test to see if it is visible to the owner of this class
    for player in self.owner.world.players:
      if self.owner != player:
        self.makeNewRecordIfNotAlreadyPresent(player)
        info = self.memoryMap[player.id]
        if self.owner.world.isLOSOkay(self.owner.position, player.position):
          info.shootable = True
          #test if the bot is within FOV
          if self.owner.position != player.position:
            if func.isSecondInFOVOfFirst(self.owner.position, self.owner.heading, player.position, self.owner.fieldOfView):
              info.timeLastSensed = pygame.time.get_ticks()      # ???????????
              #print "time last sensed: " + repr(info.timeLastSensed)
              info.lastSensedPosition = player.position
              info.timeLastVisible = pygame.time.get_ticks()      # ????????????
              #print "time last visible: " + repr(info.timeLastVisible)
              if info.withinFOV == False:
                info.withinFOV = True
                info.timeBecameVisible = info.timeLastSensed
            else:
              info.withinFOV = False
          else:
            info.withinFOV = True
        else:
          info.shootable = False
          info.withinFOV = False

        #print "player's id: " + repr(player.id)
        #print "info: " + repr(info)
        #print "memory map's player" + repr(self.memoryMap[player.id])
    #print "memoryMap[0]: " + repr(self.memoryMap[0]) + " memoryMap[1]: " + repr(self.memoryMap[1]) + "memoryMap[2]: " + repr(self.memoryMap[2]) + " memoryMap[3]: " + repr(self.memoryMap[3])

  def isOpponentShootable(self, opponent):
    if opponent != None:
      if self.memoryMap[opponent.id] != None:
        return self.memoryMap[opponent.id].shootable
    return False

  def isOpponentWithinFOV(self, opponent):
    if opponent != None:
      if self.memoryMap[opponent.id] != None:
        return self.memoryMap[opponent.id].withinFOV
    return False

  def getLastRecordedPositionOfOpponent(self, opponent):
    if opponent != None:
      if self.memoryMap[opponent.id] != None:
        return self.memoryMap[opponent.id].lastSensedPosition
    else:
      print "Attempting to get position of unrecorded bot"
      return pygame.math.Vector2(-1, -1)

  def getTimeOpponentHasBeenVisible(self, opponent):
    if opponent != None:
      if self.memoryMap[opponent.id] != None and self.memoryMap[opponent.id].withinFOV:
        #print pygame.time.get_ticks() - self.memoryMap[opponent.id].timeBecameVisible
        return pygame.time.get_ticks() - self.memoryMap[opponent.id].timeBecameVisible
    return 0

  def getTimeSinceLastSensed(self, opponent):
    if opponent != None:
      if self.memoryMap[opponent.id] != None and self.memoryMap[opponent.id].withinFOV:
        #print pygame.time.get_ticks() - self.memoryMap[opponent.id].timeLastSensed
        return pygame.time.get_ticks() - self.memoryMap[opponent.id].timeLastSensed
    return 0

  def getTimeOpponentHasBeenOutOfView(self, opponent):
    if opponent != None:
      if self.memoryMap[opponent.id] != None:
        #print pygame.time.get_ticks() - self.memoryMap[opponent.id].timeLastVisible
        return pygame.time.get_ticks() - self.memoryMap[opponent.id].timeLastVisible
    return float('Inf')

  #this method returns a list of all the opponents that have had their records updated within the last m_dMemorySpan seconds.
  def getListOfRecentlySensedOpponents(self):
    #this will store all the opponents the bot can remember
    opponents = []
    currentTime = pygame.time.get_ticks()
    #print "current time: " + repr(currentTime)
    for record in self.memoryMap:
      if record != None:
        if (currentTime - record.timeLastSensed) <= self.memorySpan:
          idx = self.memoryMap.index(record)
          #print "index: " + repr(idx)
          opponents.append(self.owner.world.players[idx])
    #print "opponents: (should be instances of Player)" + repr(opponents)
    return opponents
