#coding: utf-8

import pygame
import math
import numpy
import random
import Functions as func
import PathPlanner as pp
import SteeringBehaviors as sb
import SensoryMemory as sm
import TargetingSystem as ts
import WeaponSystem as ws
import Weapon as w

import sys
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/goals')

import Goal_Think as th
import Goal_MoveToPosition as mp

class Player:

	#maxSpeedVector = pygame.math.Vector2(100, 100)
	maxSpeed = 80
	maxHealth = 100
	maxForce = 10000000
	maxTurnRate = 0.2

	def __init__ (self, x, y, game, i):
		self.id = i

		self.position = pygame.math.Vector2(x, y)
		self.heading = pygame.math.Vector2(1, 0)
		self.facing = pygame.math.Vector2(1, 0)
		self.velocity = pygame.math.Vector2(0, 0)
		self.force = pygame.math.Vector2(0, 0)

		self.mass = 0.02
		self.size = 11
		self.health = self.maxHealth
		self.isAlive = True
		self.dead = 0
		self.respawnTime = 40
		self.fieldOfView = math.radians(180) #from degrees to radians

		#self.weapon = [None, None] # railgun, rocket launcher
		#self.ammo = [0, 0]
		#self.maxAmmo = [20, 40]

		self.world = game

		self.steeringBehavior = sb.SteeringBehaviors(self)
		self.steeringBehaviorIsOn = [False, False, False, False, False] # wall avoidance, separation, seek, arrive, wander
		self.pathPlanner = pp.PathPlanner(self, self.world.graph)
		self.path = []
		self.sensoryMemory = sm.SensoryMemory(self, 3000) # 5 - bot_memory_span
		self.targetingSystem = ts.TargetingSystem(self)
		self.weaponSystem = ws.WeaponSystem(self, 0.2, 0.1, 1) # reactionTime = 0.2, aimAccuracy = 0.0 ~ 0.2, aimPersistance = 1

		#self.goal = None
		self.brain = th.Goal_Think(self)

		self.hit = False
		self.attacher = None
		self.thinkinTime = 10
		self.think = 0
		#self.isFacingTowardsTarget = False
		
	def drawEntity(self, screen):
		pygame.draw.circle(screen, (self.health * 2, self.id * 85, 102), (int(self.position.x), int(self.position.y)), self.size, 0)
		# if self.health > 65:
		# 	pygame.draw.circle(screen, (255, 0, 127), (int(self.position.x), int(self.position.y)), self.size, 0)
		# elif self.health < 65 and self.health > 35:
		# 	pygame.draw.circle(screen, (96, 117, 12), (int(self.position.x), int(self.position.y)), self.size, 0)
		# elif self.health < 35 and self.health > 0:
		# 	pygame.draw.circle(screen, (178, 172, 91), (int(self.position.x), int(self.position.y)), self.size, 0)

	def drawTarget(self, attacker, screen):
		print attacker.health
		pygame.draw.circle(screen, (attacker.health * 2, attacker.id * 85, 102), (int(self.position.x), int(self.position.y)), self.size + 5, 3)

	def calculateTimeToReachPosition(self, pos):
		return func.distance(self.position, pos) / (self.maxSpeed * 30) #1/30 = 30, albo 60

	# def pickupWeapon(self, weapon):
	# 	print "weapon: " + repr(weapon)
	# 	if weapon == 'Railgun':
	# 		print "pickin' up railgun by player: " + repr(self.id)
	# 		if self.weapon[0] == None:
	# 			self.weapon[0] = w.Weapon("Railgun")
	# 			self.weapon[0].owner = self
	# 		self.ammo[0] = self.maxAmmo[0]
	# 		self.weapon[0].numRoundsRemaining = 50
	# 	if weapon == 'Rocket':
	# 		print "pickin' up rocket louncher by player: " + repr(self.id)
	# 		if self.weapon[1] == None:
	# 			self.weapon[1] = w.Weapon("Rocket")
	# 			self.weapon[1].owner = self
	# 		self.ammo[1] = self.maxAmmo[1]
	# 		self.weapon[1].numRoundsRemaining = 50

	def update(self, time, screen):
		#self.isFacingTowardsTarget = False
		self.brain.process()
		self.updateMovement(time)
		self.sensoryMemory.updateVision()
		self.targetingSystem.update()
		print "current target: " + repr(self.targetingSystem.currentTarget)
		self.think += 1
		if self.think == self.thinkinTime:
			self.brain.arbitrate()
			self.think = 0
		self.sensoryMemory.updateVision()
		print "weapons: " + repr(self.weaponSystem.weapon)
		if self.targetingSystem.currentTarget:
			self.weaponSystem.selectWeapon()
			#print "weapon: " + repr(self.weaponSystem.currentWeapon)
			self.weaponSystem.takeAimAndShoot()
			if self.health >= 0:
				self.targetingSystem.currentTarget.drawTarget(self, screen)
		if self.path:
			for edge in self.path:
				edge.drawEdge(screen)	
			# self.world.players.remove(self)
			# self = None
			# return

	def updateLife(self):
		if self.health <= 0:
			self.isAlive = False
			self.health = 0
			self.dead += 1
			if self.dead == self.respawnTime:
				self.isAlive = True
				self.health = self.maxHealth
				self.dead = 0
				i = random.randint(0, self.world.playersNumber - 1)
				idx = self.world.respawnPoints[i]
				node = self.world.graph.nodes[idx]
				self.position = pygame.math.Vector2(node.position.x, node.position.y)
				#self = self.Player(node.position.x, node.position.y, self, self.id)

	def update2(self, time, screen):
		#path = []
		if self.world.mouseClick:
			#if not self.pathPlanner.pathPlanned:
			#self.path = self.pathPlanner.createPathToPosition(pygame.math.Vector2(self.world.mouseClick.x, self.world.mouseClick.y))
			#self.path = self.pathPlanner.createPathToItem("Health_Giver", None)
			#self.path = self.pathPlanner.createPathToItem("Weapon_Giver", "Railgun")
			#self.path = self.pathPlanner.createPathToItem("Weapon_Giver", "Rocket")
			#print "bksfdsbvsdb" 
			# if self.position == self.world.mouseClick:
			# 	self.pathPlanner.pathPlanned = False
			#self.world.mouseClick = None
			self.goal = mp.Goal_MoveToPosition(self, pygame.math.Vector2(self.world.mouseClick.x, self.world.mouseClick.y))
			#self.updateMovement(time)
			# self.steeringBehaviorIsOn[2] = True # 2 := seek, 3 := arrive
			# print self.steeringBehaviorIsOn
			# self.steeringBehavior.target = pygame.math.Vector2(self.world.mouseClick.x, self.world.mouseClick.y)
			# self.steeringBehavior.calculate()
			# print self.steeringBehavior.steeringForce
			# self.updateMovement(time)

		self.brain.process()
		#self.brain.printGoal()

		if self.health <= 0:
			self.isAlive = False
			self.world.players.remove(self)
			self = None
			return
		
		if self.path:
			for edge in self.path:
				edge.drawEdge(screen)

			s = '['
			for edge in self.path:
				s += repr(self.path.index(edge)) + ', '
			s += ']'
			print s
		else:
			print self.path
		if self.goal:
			#print 'σκξδβφξκδσβω'
			self.goal.process()
			self.goal.printGoal()

		self.updateMovement(time)

		#print 'τι κανεις;'

		# if self.path:
		# 	if self.position != self.path[0].to.position:
		# 		self.updateMovement(time, (self.path[0].to.position - self.position))
		# 	else:
		# 		self.path.remove(path[0])
		#self.health -= 1

	def updateMovement(self, time):
		# if force.length() > 1:
		# 	self.force = force.normalize()
		# else:
		# 	self.force = force

		#self.force = self.steeringBehavior.arrive(pygame.math.Vector2(self.world.mouseClick.x, self.world.mouseClick.y), 6)
		#self.force = self.steeringBehavior.seek(pygame.math.Vector2(self.world.mouseClick.x, self.world.mouseClick.y)) #
		self.steeringBehavior.calculate()
		self.force = self.steeringBehavior.steeringForce

		acceleration = self.force/self.mass
		#print self.velocity
		#print acceleration
		self.velocity += acceleration * time
		if self.velocity.length() >= self.maxSpeed:
			self.velocity = self.velocity.normalize() * self.maxSpeed;
		self.position += self.velocity * time# + steering_force_av_corr

		#print "player's velocity: " + repr(self.velocity)

		if self.velocity.length() != 0:
			self.heading = self.velocity.normalize()
		#if not self.isFacingTowardsTarget:
		#	self.facing = pygame.math.Vector2(self.heading.x, self.heading.y)

	# feature:

	def distanceToItem(self, itemType, weaponType):
		path = self.pathPlanner.createPathToItem(itemType, weaponType)
		distanceToItem = 0
		if path:
			for edge in path:
				distanceToItem += edge.cost
		else:
			return 1
		#these values represent cutoffs. Any distance over MaxDistance results in a value of 0, and value below MinDistance results in a value of 1
		if distanceToItem > 500.0:
			return 0
		if distanceToItem < 50.0:
			return 1.0 / 500.0
		return distanceToItem / 500.0

	# def getMaxRoundsBotCanCarryForWeapon(self, weaponType):
	# 	if weaponType == "Railgun":
	# 		return 50
	# 	if weaponType == "Rocket":
	# 		return 50

	def individualWeaponStrength(self, weaponType):
		if weaponType == "Railgun" and self.weaponSystem.weapon[0] != None:
			return self.weaponSystem.weapon[0].numRoundsRemaining / self.weaponSystem.weapon[0].maxRoundsCarried
		if weaponType == "Rocket" and self.weaponSystem.weapon[1] != None:
			return self.weaponSystem.weapon[1].numRoundsRemaining / self.weaponSystem.weapon[1].maxRoundsCarried
		else:
			return 0

	def totalWeaponStrength(self):
		totalRoundsCarryable = 100 #= self.weaponSystem.weapon[0].maxRoundsCarried + self.weaponSystem.weapon[1].maxRoundsCarried
		numSlugs = 0
		numRockets = 0
		if self.weaponSystem.weapon[0] != None:
			numSlugs = self.weaponSystem.weapon[0].numRoundsRemaining
		if self.weaponSystem.weapon[1] != None:
			numRockets = self.weaponSystem.weapon[1].numRoundsRemaining

		return (numSlugs + numRockets)/(totalRoundsCarryable)

	def getHealth(self):
		return self.health / self.maxHealth

	#given a target position, this method rotates the bot's facing vector by an amount not greater than m_dMaxTurnRate until it directly faces the target.
	#returns true when the heading is facing in the desired direction
	def rotateFacingTowardPosition(self, target):
		#self.isFacingTowardsTarget = True
		toTarget = (target - self.position).normalize()
		dot = numpy.dot(self.facing, toTarget)
		if dot < -1:
			dot = -1
		if dot > 1:
			dot = 1
		#determine the angle between the heading vector and the target
		angle = math.acos(dot)
		#return true if the bot's facing is within WeaponAimTolerance degs of facing the target
		weaponAimTolerance = 0.01 # 2 degs approx
		if angle < weaponAimTolerance:
			self.facing = toTarget
			return True
		#clamp the amount to turn to the max turn rate
		if angle > self.maxTurnRate:
			angle = self.maxTurnRate
		#The next few lines use a rotation matrix to rotate the player's facing vector accordingly
		rotationMatrix = numpy.identity(3)
		#notice how the direction of rotation has to be determined when creating the rotation matrix
		rotationMatrix = func.rotate_angular(rotationMatrix, angle * func.sign(self.facing, toTarget))
		self.facing = func.transformVector(rotationMatrix, self.facing)
		return False

	def hasLOSto(self, pos):
		return self.world.isLOSOkay(self.position, pos)
