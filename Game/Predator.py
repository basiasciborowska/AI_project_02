import pygame
import math
import Functions as func
import SteeringBehavior as sb
import StateMachine as sm

class Predator:

	maxForce = 100
	maxSpeed = 100
	maxHealth = 90
	wander_speed = 20
	attack_speed = 40
	hide_speed = 45

	def __init__ (self, x, y, obstacles, pr):
		self.position = pygame.math.Vector2(x, y)
		self.heading = pygame.math.Vector2(1, 0)
		self.velocity = pygame.math.Vector2(0, 0)
		self.force = pygame.math.Vector2(0, 0)

		self.mass = 1
		self.size = 8
		self.health = self.maxHealth

		self.steering_behavior = sb.SteeringBehavior(self, obstacles)
		self.state_machine = sm.StateMachine(self)

		self.predators = pr
		self.obstacles = obstacles

		self.isInGroup = False
		self.isHidden = False
		
	def drawEntity(self, screen):
		# if self.state_machine.current_state.name == "Attack":
		# 	pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.size, 0)
		# else:
		if self.health > 65:
			pygame.draw.circle(screen, (54, 117, 12), (int(self.position.x), int(self.position.y)), self.size, 0)
		elif self.health < 65 and self.health > 35:
			pygame.draw.circle(screen, (96, 117, 12), (int(self.position.x), int(self.position.y)), self.size, 0)
		elif self.health < 35 and self.health > 0:
			pygame.draw.circle(screen, (178, 172, 91), (int(self.position.x), int(self.position.y)), self.size, 0)

	def updatePosition(self, time, display, victim):
		steering_force_av_corr = self.steering_behavior.playerObstacleAvoidance()
		steering_force_obs_av = self.steering_behavior.obstacleAvoidance() * 10
		steering_force_wall_av = self.steering_behavior.wallAvoidance(display) * 10
		steering_force_sep = self.steering_behavior.separation() * 20

		self.steering_behavior.enforceNonPenetrationConstraint()

		self.isInGroupF()
		self.isHiddenF(victim)

		self.force = self.state_machine.update(self, victim) + steering_force_obs_av + steering_force_wall_av + steering_force_sep

		acceleration = self.force/self.mass 
		self.velocity += acceleration * time
		if self.state_machine.current_state.name == "Wandering" or (self.state_machine.current_state.name == "Hide" and self.isHidden):
			self.velocity = self.velocity.normalize() * self.wander_speed
		elif self.state_machine.current_state.name == "Hide" and self.isHidden == False:
			self.velocity = self.velocity.normalize() * self.hide_speed
		else:
			self.velocity = self.velocity.normalize() * self.attack_speed
		self.position += self.velocity * time + steering_force_av_corr

		self.position = func.walls(self.position, display, self.size)

		if self.velocity.length() != 0:
			self.heading = self.velocity.normalize()

		self.eatBrain(victim)

		self.isInGroup = False
		self.isHidden = False

		if self.health < 1:
			self.predators.remove(self)
			self = None

	# def isInGroup(self):
	# 	predators_number = 1
	# 	for predator in self.predators:
	# 		if predator != self:
	# 			distance = func.distance(self.position, predator.position)
	# 			if distance < 100:
	# 				predators_number += 1
	# 	if predators_number > 4:
	# 		return True
	# 	else:
	# 		return False

	def isInGroupF(self):
		predators_number = 1
		group = 1
		if not self.isInGroup:
			for predator in self.predators:
				if predator != self:
					if not predator.isInGroup:
						distance = func.distance(self.position, predator.position)
						if distance < 100:
							predators_number += 1
		if predators_number > 4:
			for predator in self.predators:
				if group < 7:
					if predator != self:
						if not predator.isInGroup:
							distance = func.distance(self.position, predator.position)
							if distance < 100:
								predator.isInGroup = True
								group += 1
				else:
					break

	def isHiddenF(self, victim):
		vector_to_victim = (victim.position - self.position)
		distance = vector_to_victim.length()
		vector_to_victim_normalized = vector_to_victim.normalize()
		for obstacle in self.obstacles:
			local_obstacle_pos = func.pointToLocalSpace(obstacle.position, vector_to_victim_normalized, self.position)
			if local_obstacle_pos.x > 0 and local_obstacle_pos.x < distance and math.fabs(local_obstacle_pos.y) < obstacle.radius:
				print 'hidden'
				self.isHidden = True

	def eatBrain(self, victim):
		if func.distance(self.position, victim.position) < victim.size/2 + self.size and self.state_machine.current_state.name == "Attack":
			victim.health -= 0.1
