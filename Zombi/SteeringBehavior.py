import pygame
import Obstacle as obs
import Entity as ent
import math
import Functions as func
import numpy
import random

class SteeringBehavior:

	wander_radius = 70
	wander_distance = 570
	wander_jitter = 120

	def __init__(self, charact, obstcs):
		self.character = charact
		self.obstacles = obstcs
		self.theta = random.random() * 2 * math.pi
  		self.wander_target = pygame.math.Vector2(self.wander_radius * math.cos(self.theta), self.wander_radius * math.sin(self.theta))		#create a vector to a target position on the wander circle

	def obstacleAvoidance(self):
		box_length = 50 + self.character.velocity.length()/self.character.maxForce * 50
		colliding_obstacle = None
		distance_to_intersection_point = float('Inf')
		local_pos_of_intersecting_obs = pygame.math.Vector2(0, 0)
		steering_force = pygame.math.Vector2(0, 0)

		for obstacle in self.obstacles:
			position_in_local_space = func.pointToLocalSpace(obstacle.position, self.character.heading, self.character.position)

			if position_in_local_space.x > 0 and position_in_local_space.x < box_length:
				expanded_radius = obstacle.radius + self.character.size/2
				if math.fabs(position_in_local_space.y) < expanded_radius:
					sqrt = math.sqrt(expanded_radius ** 2 - position_in_local_space.y ** 2)
					intersection_point = position_in_local_space.x - sqrt
					if intersection_point <= 0:
						intersection_point = position_in_local_space.x + sqrt
					if intersection_point < distance_to_intersection_point:
						distance_to_intersection_point = intersection_point
						colliding_obstacle = obstacle
						local_pos_of_intersecting_obs = position_in_local_space
		if(colliding_obstacle):
			y_const = 80 + (box_length - local_pos_of_intersecting_obs.x) / box_length
			steering_force.y = (colliding_obstacle.radius - local_pos_of_intersecting_obs.y) * y_const * (colliding_obstacle.radius ** 4) * 100
			steering_force.x = (colliding_obstacle.radius - local_pos_of_intersecting_obs.x) * 2.5 * (colliding_obstacle.radius ** 4)#brakingweight = 0.2
			return func.vectorToWorldSpace(steering_force, self.character.heading)
		else:
			return pygame.math.Vector2(0, 0)


	def playerObstacleAvoidance(self):
		for obstacle in self.obstacles:
			expanded_radius = obstacle.radius + self.character.size/2
			dist = func.distance(self.character.position, obstacle.position)
			if dist < expanded_radius:
				vector_from_obs_to_char = func.vectorFromPointToPoint(obstacle.position, self.character.position).normalize()
				return vector_from_obs_to_char * (expanded_radius - dist)
		return pygame.math.Vector2(0, 0)

	def wander(self):
		self.wander_target += pygame.math.Vector2(random.uniform(-1,1) * self.wander_jitter, random.uniform(-1,1) * self.wander_jitter)
		self.wander_target = self.wander_target.normalize()
		self.wander_target *= self.wander_radius

		target_local = self.wander_target + pygame.math.Vector2(self.wander_distance, 0)
		target_world = func.pointToWorldSpace(target_local, self.character.heading, self.character.position)
		return target_world - self.character.position	

	def hide(self, enemy):
		hiding_spot = None
		distance_to_hiding_position = float('Inf')

		for obstacle in self.obstacles:
			hiding_spot_temp = func.get_hiding_position(obstacle, enemy.position)
			distance = func.distance(hiding_spot_temp, self.character.position)
			if distance < distance_to_hiding_position:
				distance_to_hiding_position = distance
				hiding_spot = hiding_spot_temp
		if distance_to_hiding_position != float('Inf'):
			return hiding_spot - self.character.position, hiding_spot

	def attack(self, enemy):
		velocity = (enemy.position - self.character.position).normalize() * self.character.attack_speed
		return velocity# - self.character.velocity

	def wallAvoidance(self, display):
		feeler_end_position = self.character.position + (self.character.heading * self.character.velocity.length()) / 30
		intersection_point = pygame.math.Vector2(0, 0)
		force = pygame.math.Vector2(0, 0)

		if feeler_end_position.x > display[0] - self.character.size:
			intersection_point.x = display[0]
			a = (feeler_end_position.x - display[0]) / self.character.heading.x
			intersection_point.y = feeler_end_position.y - a * self.character.heading.y

			distance = func.distance(feeler_end_position, intersection_point)
			force = distance * pygame.math.Vector2(-1, 0)

		elif feeler_end_position.x < self.character.size:
			intersection_point.x = 0
			a = (feeler_end_position.x) / self.character.heading.x
			intersection_point.y = feeler_end_position.y - a * self.character.heading.y

			distance = func.distance(feeler_end_position, intersection_point)
			force = distance * pygame.math.Vector2(1, 0)

		if feeler_end_position.y > display[1] - self.character.size:
			intersection_point.y = display[1]
			a = (feeler_end_position.y - display[1]) / self.character.heading.y
			intersection_point.x = feeler_end_position.x - a * self.character.heading.x

			distance = func.distance(feeler_end_position, intersection_point)
			force = distance * pygame.math.Vector2(0, -1)

		elif feeler_end_position.y < self.character.size:
			intersection_point.y = 0
			a = (feeler_end_position.y) / self.character.heading.y
			intersection_point.x = feeler_end_position.x - a * self.character.heading.x

			distance = func.distance(feeler_end_position, intersection_point)
			force = distance * pygame.math.Vector2(0, 1)

		return force * 200

	def separation(self):
		steering_force = pygame.math.Vector2(0, 0)
		for predator in self.character.predators:
			if predator != self.character:
				if func.distance(predator.position, self.character.position) < 80:
					to_agent = self.character.position - predator.position
					if to_agent.length() != 0:
						steering_force += to_agent.normalize() / to_agent.length()
					else:
						steering_force += self.character.heading / 0.0001
		return steering_force * 50

	def enforceNonPenetrationConstraint(self):
		for predator in self.character.predators:
			if predator != self.character:
				if func.distance(predator.position, self.character.position) < 80:
					to_agent = self.character.position - predator.position
					distance_from_each_other = to_agent.length()
					amount_of_overlap = predator.size * 2 - distance_from_each_other
					if amount_of_overlap >= 0:
						if to_agent.length() != 0:
							self.character.position += to_agent.normalize() * amount_of_overlap
						else:
							self.character.position += self.character.heading * amount_of_overlap





