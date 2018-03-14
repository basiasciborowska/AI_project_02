import pygame
import Functions as func

class Trigger:

	def __init__(self, graphId, numUpBetRes, t, w):
		self.regionOfInfluenceRadius = 25
		self.isActive = True
		self.graphNodeId = graphId
		self.numUpdatesBetweenRespawns = numUpBetRes
		self.numUpdatesRemainingUntilRespawn = numUpBetRes
		self.type = t
		self.weapon = w

	def isTouchingTrigger(self, player):
		if func.distance(player.world.graph.nodes[self.graphNodeId].position, player.position) <= (player.size + self.regionOfInfluenceRadius):
			return True
		else:
			return False

	def tryTrigger(self, player):
		if self.isActive and self.isTouchingTrigger(player):
			if self.type == "Weapon_Giver":
				#player.pickupWeapon(self.weapon)
				player.weaponSystem.addWeapon(self.weapon)
			if self.type == "Health_Giver":
				player.health = player.maxHealth
			self.isActive = False

	def updateTrigger(self):
		if not self.isActive:
			self.numUpdatesRemainingUntilRespawn -= 1
			if self.numUpdatesRemainingUntilRespawn <= 0:
				self.isActive = True
				self.numUpdatesRemainingUntilRespawn = self.numUpdatesBetweenRespawns

	def drawTrigger(self, screen, game):
		if self.isActive:
			if self.type == "Weapon_Giver":
				if self.weapon == "Railgun":
					screen.blit(pygame.image.load('rail.png'), (game.graph.nodes[self.graphNodeId].position.x - 12, game.graph.nodes[self.graphNodeId].position.y - 12))
				if self.weapon == "Rocket":
					screen.blit(pygame.image.load('rocket.png'), (game.graph.nodes[self.graphNodeId].position.x - 12, game.graph.nodes[self.graphNodeId].position.y - 12))
			if self.type == "Health_Giver":
				screen.blit(pygame.image.load('health2.png'), (game.graph.nodes[self.graphNodeId].position.x - 12, game.graph.nodes[self.graphNodeId].position.y - 12))
