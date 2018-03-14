import pygame

class GraphNode:

	def __init__(self, index, pos, ex_inf):
		self.id = index
		self.position = pos
		self.extra_info = ex_inf

	def drawNode(self, screen):
		tmp = self.id % 256
		pygame.draw.circle(screen, (102, tmp, 51), (int(self.position.x), int(self.position.y)), 2 , 0)

