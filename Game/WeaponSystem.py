import random
import Functions as func
import Weapon as w

class WeaponSystem:
  def __init__(self, own, rt, aa, ap):
    self.owner = own
    #pointers to the weapons the bot is carrying (a bot may only carry one instance of each weapon)
    self.weapon = [None, None] # railgun, rocket
    #a pointer to the weapon the bot is currently holding
    self.currentWeapon = None
    #this is the minimum amount of time a bot needs to see an opponent before it can react to it. This variable is used to prevent a bot shooting at an opponent the instant it becomes visible.
    self.reactionTime = rt
    #each time the current weapon is fired a certain amount of random noise is added to the the angle of the shot. This prevents the bots from hitting their opponents 100% of the time. The lower this value the more accurate a bot's aim will be. Recommended values are between 0 and 0.2 (the value represents the max deviation in radians that can be added to each shot).
    self.aimAccuracy = aa # 0.2
    #the amount of time a bot will continue aiming at the position of the target even if the target disappears from view.
    self.aimPersistance = ap

  #predicts where the target will be by the time it takes the current weapon's projectile type to reach it. Used by TakeAimAndShoot
  def predictFuturePositionOfTarget(self):
    maxSpeed = self.currentWeapon.maxProjectileSpeed
    #if the target is ahead and facing the agent shoot at its current pos
    toEnemy = self.owner.targetingSystem.currentTarget.position - self.owner.position
    #the lookahead time is proportional to the distance between the enemy and the pursuer; and is inversely proportional to the sum of the agent's velocities
    lookAheadTime = toEnemy.length() / (self.owner.maxSpeed + self.owner.targetingSystem.currentTarget.maxSpeed)
    #return the predicted future position of the enemy
    return self.owner.targetingSystem.currentTarget.position + self.owner.targetingSystem.currentTarget.velocity * lookAheadTime

  #adds a random deviation to the firing angle not greater than m_dAimAccuracy rads
  def addNoiseToAim(self, aimingPos):
    toPos = aimingPos - self.owner.position
    toPos = func.rotateAroundOrigin(toPos, random.uniform(-self.aimAccuracy, self.aimAccuracy))
    aimingPos = toPos + self.owner.position
    return aimingPos

  #this method aims the bot's current weapon at the target (if there is a target) and, if aimed correctly, fires a round. (Called each update-step from Raven_Bot::Update)
  def takeAimAndShoot(self):
    #aim the weapon only if the current target is shootable or if it has only very recently gone out of view (this latter condition is to ensure the weapon is aimed at the target even if it temporarily dodges behind a wall or other cover)
    if self.currentWeapon and (self.owner.targetingSystem.isTargetShootable() or self.owner.targetingSystem.getTimeTargetHasBeenOutOfView() < self.aimPersistance):
      #the position the weapon will be aimed at
      aimingPos = self.owner.targetingSystem.currentTarget.position
      #if the current weapon is not an instant hit type gun the target position must be adjusted to take into account the predicted movement of the target
      if self.currentWeapon.type == "Rocket":
        aimingPos = self.predictFuturePositionOfTarget()
        #if the weapon is aimed correctly, there is line of sight between the bot and the aiming position and it has been in view for a period longer than the bot's reaction time, shoot the weapon
        if self.owner.rotateFacingTowardPosition(aimingPos) and self.owner.targetingSystem.getTimeTargetHasBeenVisible() > self.reactionTime and self.owner.hasLOSto(aimingPos):
          aimingPos = self.addNoiseToAim(aimingPos)
          self.currentWeapon.shootAt(aimingPos)
      #no need to predict movement, aim directly at target
      else:
        #if the weapon is aimed correctly and it has been in view for a period longer than the bot's reaction time, shoot the weapon
        if self.owner.rotateFacingTowardPosition(aimingPos) and self.owner.targetingSystem.getTimeTargetHasBeenVisible() > self.reactionTime:
          aimingPos = self.addNoiseToAim(aimingPos)
          self.currentWeapon.shootAt(aimingPos)
    #no target to shoot at so rotate facing to be parallel with the bot's heading direction
    else:
      self.owner.rotateFacingTowardPosition(self.owner.position + self.owner.heading)

  #this method determines the most appropriate weapon to use given the current game state. (Called every n update-steps from Raven_Bot::Update)
  def selectWeapon(self):
    print self.owner.targetingSystem.isTargetPresent()
    if self.owner.targetingSystem.isTargetPresent():
      distanceToTarget = func.distance(self.owner.position, self.owner.targetingSystem.currentTarget.position)
      bestSoFar = -1
      for weapon in self.weapon:
        if weapon != None:
          score = weapon.getDesirability(distanceToTarget)
          if score > bestSoFar:
            bestSoFar = score
            self.currentWeapon = weapon

  #this will add a weapon of the specified type to the bot's inventory. If the bot already has a weapon of this type only the ammo is added. (called by the weapon giver-triggers to give a bot a weapon)
  def addWeapon(self, weapon_type):
    #create an instance of this weapon
    weapon = None
    weapon = w.Weapon(self.owner, weapon_type)
    #if the bot already holds a weapon of this type, just add its ammo
    present = self.getWeaponFromInventory(weapon_type)
    if present:
      present.incrementRounds(weapon.numRoundsRemaining)
    #if not already holding, add to inventory
    else:
      if weapon_type == "Railgun":
        self.weapon[0] = weapon
      if weapon_type == "Rocket":
        self.weapon[1] = weapon

  #changes the current weapon to one of the specified type (provided that type is in the bot's possession)
  def changeWeapon(self, weapon_type):
    weapon = self.getWeaponFromInventory(weapon_type)
    if weapon:
      self.currentWeapon = weapon

  #shoots the current weapon at the given position
  def shootAt(self, pos):
    self.currentWeapon.shootAt(pos)

  #returns a pointer to the specified weapon type (if in inventory, null if not)
  def getWeaponFromInventory(self, weapon_type):
    if weapon_type == "Railgun":
      return self.weapon[0]
    if weapon_type == "Rocket":
      return self.weapon[1]

  #returns the amount of ammo remaining for the specified weapon
  def getAmmoRemainingForWeapon(self, weapon_type):
    if weapon_type == "Railgun" and self.weapon[0] != None:
      return self.weapon[0].numRoundsRemaining
    if weapon_type == "Rocket" and self.weapon[1] != None:
      return self.weapon[1].numRoundsRemaining
    return 0