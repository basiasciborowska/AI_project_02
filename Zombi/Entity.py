import pygame
import math
import Functions as func
import SteeringBehavior as sb

class Entity:

	maxForce = 50
	maxSpeed = 130
	maxHeath = 100

	def __init__ (self, x, y, obstacles):
		self.position = pygame.math.Vector2(x, y)
		self.heading = pygame.math.Vector2(1, 0)
		self.velocity = pygame.math.Vector2(0, 0)
		self.force = pygame.math.Vector2(0, 0)

		self.mass = 1
		self.size = 30
		self.health = self.maxHeath

		self.steering_behavior = sb.SteeringBehavior(self, obstacles)
		
	def drawEntity(self, screen):
		side = func.perpendicular(self.heading)
		a = self.position + self.heading * 20
		b = self.position - self.heading * 20 + 17 * side
		c = self.position - self.heading * 20 - 17 * side
		pygame.draw.polygon(screen, (102, 0, 51), [[a.x, a.y], [b.x, b.y], [c.x, c.y]])

	def drawHealthbar(self, screen):
		pygame.draw.rect(screen, (230, 230, 230), (screen.get_width() - self.maxHeath * 1.5 - 20, 20, self.maxHeath * 1.5, 20), 2)
		if self.health > 50:
			pygame.draw.rect(screen, (0, 255, 0), (screen.get_width() - self.maxHeath * 1.5 - 20, 20, max(self.health * 1.5, 0), 20))
		elif self.health > 20:
			pygame.draw.rect(screen, (255, 255, 0), (screen.get_width() - self.maxHeath * 1.5 - 20, 20, max(self.health * 1.5, 0), 20))
		elif self.health > 0:
			pygame.draw.rect(screen, (255, 0, 0), (screen.get_width() - self.maxHeath * 1.5 - 20, 20, max(self.health * 1.5, 0), 20))

	def moveLeft(self):
		self.force += (-200, 0)

	def moveRight(self):
		self.force += (200, 0)

	def moveUp(self):
		self.force += (0, -200)

	def moveDown(self):
		self.force += (0, 200)

	def stop(self, is_up_or_down):
		if is_up_or_down:
			self.force.y = 0
			self.velocity.y = 0
		else:
			self.force.x = 0
			self.velocity.x = 0

	def updatePosition(self, time, display):
		steering_force = self.steering_behavior.playerObstacleAvoidance()

		acceleration = self.force/self.mass
		self.velocity += acceleration * time
		self.velocity = func.truncate(self.velocity, self.maxSpeed)
		self.position += self.velocity * time + steering_force
		
		self.position = func.walls(self.position, display, self.size/2)

		self.heading = (pygame.mouse.get_pos() - self.position).normalize()

		