import pygame

class GraphEdge:

	def __init__(self, fromm, to, cost):
		self.fromm = fromm
		self.to = to
		self.cost = cost
		self.color = pygame.math.Vector3(102, self.to.id % 256, 51)

	def drawEdge(self, screen):
		#tmp = self.to.id % 256
		if self.color.z == 255 or self.color.x == 255:
			pygame.draw.line(screen, (self.color.x, self.color.y, self.color.z), self.fromm.position, self.to.position, 3)
		else:
			pygame.draw.line(screen, (self.color.x, self.color.y, self.color.z), self.fromm.position, self.to.position)
