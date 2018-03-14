import Functions as func
import pygame
import math

class Gun:

	length = 800

	def __init__(self, own, obs, pr):
		self.owner = own
		self.position = self.owner.position
		self.direction = self.owner.heading
		self.obstacles = obs
		self.predators = pr

	def drawRay(self, screen):
		obstacle = self.hitObstacle()
		target = self.hitTarget()
		if obstacle and target:
			dist_obs = func.distance(obstacle.position, self.position)
			dist_tg = func.distance(target.position, self.position)
			if dist_obs < dist_tg:
				target = None
			elif dist_tg < dist_obs:
				obstacle = None
		if target:
			local = func.pointToLocalSpace(target.position, self.direction, self.position)
			d = local.x - math.sqrt(target.size ** 2 - local.y ** 2)
			pygame.draw.line(screen, (255, 255, 255), self.position, self.position + d * self.direction, 3)
			target.health -= 30
		elif obstacle:
			local = func.pointToLocalSpace(obstacle.position, self.direction, self.position)
			d = local.x - math.sqrt(obstacle.radius ** 2 - local.y ** 2)
			pygame.draw.line(screen, (255, 255, 255), self.position, self.position + d * self.direction, 3)
		else:
			pygame.draw.line(screen, (255, 255, 255), self.position, self.position + 1000 * self.direction, 3)

	def hitObstacle(self):
		hit_obstacles = []
		distance = float('Inf')
		target = None
		for obstacle in self.obstacles:
			position_in_local_space_o = func.pointToLocalSpace(obstacle.position, self.direction, self.position)
			if math.fabs(position_in_local_space_o.y) < obstacle.radius and position_in_local_space_o.x > 0:
				hit_obstacles.append(obstacle)
		if len(hit_obstacles) == 0:
			return None
		for hit in hit_obstacles:
			tmp_distance = func.distance(hit.position, self.position)
			if tmp_distance < distance:
				distance = tmp_distance
				target = hit
		return target

	def hitTarget(self):
		hit_targets = []
		distance = float('Inf')
		target = None
		for predator in self.predators:
			position_in_local_space_p = func.pointToLocalSpace(predator.position, self.direction, self.position)
			if math.fabs(position_in_local_space_p.y) < predator.size and position_in_local_space_p.x > 0:
				hit_targets.append(predator)
		if len(hit_targets) == 0:
			return None
		for hit in hit_targets:
			tmp_distance = func.distance(hit.position, self.position)
			if tmp_distance < distance:
				distance = tmp_distance
				target = hit
		return target		

