import random

class AttackTargetGoal_Evaluator:

  def __init__(self, cb):
    self.characterBias = cb
  
  def calculateDesirability(self, bot):
    desirability = 0.0
    if bot.targetingSystem.isTargetPresent():
      tweaker = 1.0
      desirability = tweaker * bot.getHealth() * bot.totalWeaponStrength()
      desirability *= self.characterBias
    return desirability

  def setGoal(self, bot):
    bot.brain.addGoal_AttackTarget()

class ExploreGoal_Evaluator:

  def __init__(self, cb):
    self.characterBias = cb

  def calculateDesirability(self, bot):
    desirability = 0.05
    desirability *= self.characterBias
    return desirability

  def setGoal(self, bot):
    bot.brain.addGoal_Explore()

class GetHealthGoal_Evaluator:

  def __init__(self, cb):
    self.characterBias = cb

  def calculateDesirability(self, bot):
    distance = bot.distanceToItem("Health_Giver", None)
    if distance == 1:
      return 0
    else:
      tweaker = 0.2
      if distance != 0:
        desirability = (tweaker * (1 - bot.getHealth())) / distance
      else:
        desirability = 1
      if desirability < 0:
        desirability = 0
      if desirability > 1:
        desirability = 1
      desirability *= self.characterBias
      return desirability # random.random()

  def setGoal(self, bot):
    print "setting goal get health"
    bot.brain.addGoal_GetItem("Health_Giver", None)

class GetWeaponGoal_Evaluator:

  def __init__(self, cb, wt):
    self.characterBias = cb
    self.weaponType = wt

  def calculateDesirability(self, bot):
    distance = bot.distanceToItem("Weapon_Giver", self.weaponType)
    if distance == 1:
      return 0
    else:
      tweaker = 0.15
      if distance != 0:
        desirability = (tweaker * bot.getHealth() * (1 - bot.individualWeaponStrength(self.weaponType))) / distance
      else:
        desirability = 1
      if desirability < 0:
        desirability = 0
      if desirability > 1:
        desirability = 1
      desirability *= self.characterBias
      return desirability # random.random()

  def setGoal(self, bot):
    print "settin goal get weapon " + repr(self.weaponType)
    bot.brain.addGoal_GetItem("Weapon_Giver", self.weaponType)