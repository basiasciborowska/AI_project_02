import pygame

class Obstacle:

	def __init__(self, x, y, r):
		self.position = pygame.math.Vector2(x, y)
		self.radius = r

	def drawObstacle(self, screen):
		#screen.blit(self.img, (self.position.x, self.position.y))
		pygame.draw.circle(screen, (80, 80, 80), (int(self.position.x), int(self.position.y)), self.radius, 0)