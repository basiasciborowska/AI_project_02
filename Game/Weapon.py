import pygame
import Functions as func

class Weapon:

	def __init__(self, own, type_of_gun):
		self.owner = own
		self.type = type_of_gun
		if self.type == "Railgun":
			#this is the prefered distance from the enemy when using this weapon
			self.idealRange = 200
			#the number of times this weapon can be fired per second
			self.rateOfFire = 0.01
			#the max speed of the projectile this weapon fires
			self.maxProjectileSpeed = 5000
		if self.type == "Rocket":
			#this is the prefered distance from the enemy when using this weapon
			self.idealRange = 150
			#the number of times this weapon can be fired per second
			self.rateOfFire = 0.0015
			#the max speed of the projectile this weapon fires
			self.maxProjectileSpeed = 9
		#amount of ammo carried for this weapon
		self.numRoundsRemaining = 15
		#maximum number of rounds a bot can carry for this weapon
		self.maxRoundsCarried  = 50
		#the earliest time the next shot can be taken
		self.timeNextAvailable = pygame.time.get_ticks()
		self.desirability = 0

	#The number of times a weapon can be discharges depends on its rate of fire. This method returns true if the weapon is able to be discharged at the current time. (called from ShootAt() )
	def isReadyForNextShot(self):
		if pygame.time.get_ticks() > self.timeNextAvailable:
			return True
		return False

	#this is called when a shot is fired to update m_dTimeNextAvailable
	def updateTimeWeaponIsNextAvailable(self):
		self.timeNextAvailable = pygame.time.get_ticks() + (1.0 / self.rateOfFire) * 10 # 10?

	#this method aims the weapon at the given target by rotating the weapon's owner's facing direction (constrained by the bot's turning rate). It returns  true if the weapon is directly facing the target.
	def aimAt(self, target):
		return self.owner.rotateFacingTowardPosition(target)

	#this discharges a projectile from the weapon at the given target position (provided the weapon is ready to be discharged... every weapon has its own rate of fire)
	def shootAt(self, pos): #= 0;
		if self.numRoundsRemaining > 0 and self.isReadyForNextShot():
			if self.type == "Railgun":
				self.owner.world.addRailGunSlug(self.owner, pos)
			if self.type == "Rocket":
				self.owner.world.addRocket(self.owner, pos) #!!!!!!!!!!!!!
			self.updateTimeWeaponIsNextAvailable()
			self.numRoundsRemaining -= 1

	#this method returns a value representing the desirability of using the weapon. This is used by the AI to select the most suitable weapon for a bot's current situation. This value is calculated using fuzzy logic
	def getDesirability(self, distToTarget): #= 0;
		if self.numRoundsRemaining == 0:
			self.desirability = 0
		else:
			if distToTarget != 0:
				desirability = self.numRoundsRemaining / (self.maxRoundsCarried * distToTarget)
			#//fuzzify distance and amount of ammo
			#m_FuzzyModule.Fuzzify("DistanceToTarget", DistToTarget)
			#m_FuzzyModule.Fuzzify("AmmoStatus", (double)m_iNumRoundsLeft)
			#self.desirability = m_FuzzyModule.DeFuzzify("Desirability", FuzzyModule::max_av)
		return self.desirability

	def decrementNumRounds(self):
		if self.numRoundsRemaining > 0:
			self.numRoundsRemaining -= 1

	def incrementRounds(self, num):
		self.numRoundsRemaining += num
		if self.numRoundsRemaining > self.maxRoundsCarried:
			self.numRoundsRemaining = self.maxRoundsCarried

