import pygame
import Functions as func

class Walls:

	def __init__ (self, i, f, t):
		self.id = i
		self.fromm = pygame.math.Vector2(f.x, f.y)
		self.to = pygame.math.Vector2(t.x, t.y)
		self.normal = func.perpendicular(self.to - self.fromm).normalize()

	def drawWall(self, screen):
		pygame.draw.line(screen, (255,255,255), self.fromm, self.to)
		mid_point = (self.fromm + self.to) / 2
		pygame.draw.line(screen, (0, 255, 255), mid_point, mid_point + self.normal * 20)

