import pygame
import math
import random
import Functions as func
import Walls as wal
import Graph as gr
import Player as pls
import TriggerSystem as ts
import Projectile as p
import GraphSearch_Dijkstra as dij

class Game:

	def __init__(self, display, no_players):
		self.play_game = True
		self.walls = []
		self.graph = gr.Graph()
		self.playersNumber = no_players
		self.players = []
		self.mouseClick = None
		self.triggerSystem = ts.TriggerSystem()
		self.pathCosts = []
		self.projectiles = []
		#self.respawnPoints = [7, 110, 273, 410]
		self.respawnPoints = []

	def calculateCostToTravelBetweenNodes(self, nd1, nd2):
		return self.pathCosts[nd1][nd2]

	def createAllPairsCostsTable(self):
		row = [0.0] * len(self.graph.nodes)
		self.pathCosts = [row] * len(self.graph.nodes)
		for source in range(len(self.graph.nodes)):
			search = dij.GraphSearch_Dijkstra(self.graph, source, None, None)
			search.search()
			for target in range(len(self.graph.nodes)):
				if source != target:
					self.pathCosts[source][target] = search.costToThisNode[target]
		for i in range(len(self.graph.nodes)):
			s = '['
			for j in range(len(self.graph.nodes)):
				s += repr(self.pathCosts[i][j]) + ', '
			s += ']'
			print s

	def addWalls(self):
		f = open('walls.txt', 'r')
		fromm = pygame.math.Vector2(0, 0)
		to = pygame.math.Vector2(0, 0)

		heading = f.readline()

		for line in f:
			idd, fromm.x, fromm.y, to.x, to.y = [float(x) for x in line.split()]
			self.walls.append(wal.Walls(idd, 1.2 * 25 * fromm, 1.2 * 25 * to))
			#self.walls.append(wal.Walls(idd, fromm, to))

	def writeGraphToTxt(self):
		f = open('graph.txt', 'w')
		for node in self.graph.nodes:
			tmp = repr(node.position.x) + ' ' + repr(node.position.y) + ' '
			for edge in self.graph.edges[node]:
				tmp += repr(edge.to.position.x) + ' ' + repr(edge.to.position.y) + ' '
			tmp += '\n'
			f.write(tmp)

	def readGraphFromTxt(self):
		f = open('graph.txt', 'r')
		for line in f:
			edges = [float(x) for x in line.split()]
			node_position_x, node_position_y = edges[0], edges[1]
			self.graph.addNode(pygame.math.Vector2(node_position_x, node_position_y))
			for x, y in zip(edges[0::2], edges[1::2]):
   				to = pygame.math.Vector2(x, y)
   				if node_position_x != x or node_position_y != y:
					self.graph.addEdge(pygame.math.Vector2(node_position_x, node_position_y), to)

	def distanceFromWalls(self, prev_position, position):
		for wall in self.walls:
			vector = (wall.to - wall.fromm).normalize()
			point_in_local_space_to = func.pointToLocalSpace(wall.to, vector, wall.fromm)
			point_in_local_space_prev_node = func.pointToLocalSpace(prev_position, vector, wall.fromm)
			point_in_local_space_node = func.pointToLocalSpace(position, vector, wall.fromm)

			if point_in_local_space_node.x >= -10:
				if point_in_local_space_node.x <= point_in_local_space_to.x:
					if (point_in_local_space_node.y * point_in_local_space_prev_node.y) <= 0 or math.fabs(point_in_local_space_node.y) < 12.5:
						return False
		return True

	def edgeToWallDistance(self, fr, t):
		for wall in self.walls:
			center = (fr + t) / 2.0
			if not self.distanceFromWalls(center, center):
				return False
		return True

	def addDiagonal(self):
		for node in self.graph.nodes:
			new_pos = pygame.math.Vector2(node.position.x + 25, node.position.y + 25)
			if self.graph.nodeAtPosition(new_pos) and self.edgeToWallDistance(node.position, new_pos):
				self.graph.addEdge(node.position, new_pos)
			new_pos = pygame.math.Vector2(node.position.x - 25, node.position.y + 25)
			if self.graph.nodeAtPosition(new_pos) and self.edgeToWallDistance(node.position, new_pos):
				self.graph.addEdge(node.position, new_pos)

	def floodFill(self):
		new_node = True
		self.graph.addNode(pygame.math.Vector2(212.5, 112.5))
		#self.graph.addNode(pygame.math.Vector2(50, 50))
		self.floodFillRec(pygame.math.Vector2(212.5, 112.5), pygame.math.Vector2(237.5, 112.5), new_node)
		#self.floodFillRec(pygame.math.Vector2(50, 50), pygame.math.Vector2(60, 50), new_node)
		self.addDiagonal()

	def floodFillRec(self, prev_pos, position, new_node):
		if not new_node:
			return

		if not self.distanceFromWalls(prev_pos, position):
			return

		new_node = self.graph.addEdge(prev_pos, position)

		self.floodFillRec(position, pygame.math.Vector2(position.x + 25, position.y), new_node)
		self.floodFillRec(position, pygame.math.Vector2(position.x - 25, position.y), new_node)
		self.floodFillRec(position, pygame.math.Vector2(position.x, position.y + 25), new_node)
		self.floodFillRec(position, pygame.math.Vector2(position.x, position.y - 25), new_node)
		# self.floodFillRec(position, pygame.math.Vector2(position.x + 10, position.y), new_node)
		# self.floodFillRec(position, pygame.math.Vector2(position.x - 10, position.y), new_node)
		# self.floodFillRec(position, pygame.math.Vector2(position.x, position.y + 10), new_node)
		# self.floodFillRec(position, pygame.math.Vector2(position.x, position.y - 10), new_node)

	def addRespawnPoints(self):
		for i in range(self.playersNumber):
			idx = random.randint(0, (len(self.graph.nodes) - 1))
			self.respawnPoints.append(idx)

	def addPlayers(self):
		self.addRespawnPoints()
		for i in range(self.playersNumber):
			#idx = random.randint(0, (len(self.graph.nodes) - 1))
			idx = self.respawnPoints[i]
			node = self.graph.nodes[idx]
			self.players.append(pls.Player(node.position.x, node.position.y, self, i))

	def addRocket(self, shooter, target):
		print "ADDIN' ROCKET"
		projectile = p.Projectile(shooter, target, "Rocket")
		self.projectiles.append(projectile)

	def addRailGunSlug(self, shooter, target):
		print "ADDIN' RAILGUN SLUG"
		projectile = p.Projectile(shooter, target, "Railgun")
		self.projectiles.append(projectile)

	def isPathObstructed(self, a, b, boundingRadius):
		toB = (b-a).normalize()
		curPos = pygame.math.Vector2(a.x, a.y)
  		while func.distanceSq(curPos, b) > boundingRadius ** 2:
		    #advance curPos one step
		    curPos += toB * 0.5 * boundingRadius
		    
		    #test all walls against the new position
		    if self.doWallsIntersectCircle(curPos, boundingRadius):
		    	return True
		return False

	def doWallsIntersectCircle(self, p, r):
		#test against the walls
		for wall in self.walls:
			#do a line segment intersection test
		    if (self.lineSegmentCircleIntersection(wall.fromm, wall.to, p, r)):
		    	return True                                                          
		return False

	def lineSegmentCircleIntersection(self, a, b, p, radius):
		#first determine the distance from the center of the circle to the line segment (working in distance squared space)
		distToLineSq = self.distToLineSegmentSq(a, b, p)
		if distToLineSq < radius ** 2:
			return True
		else:
		    return False

	def distToLineSegmentSq(self, a, b, p):
		#if the angle is obtuse between PA and AB is obtuse then the closest vertex must be A
		dotA = (p.x - a.x) * (b.x - a.x) + (p.y - a.y) * (b.y - a.y)
		if (dotA <= 0):
			return func.distanceSq(a, p)
		#if the angle is obtuse between PB and AB is obtuse then the closest vertex must be B
		dotB = (p.x - b.x) * (a.x - b.x) + (p.y - b.y) * (a.y - b.y)		 
		if (dotB <= 0):
			return func.distanceSq(b, p)
		#calculate the point along AB that is the closest to P
		point = a + ((b - a) * dotA) / (dotA + dotB)
		#calculate the distance P-Point
		return func.distanceSq(p, point)

	def distToLineSegment(self, a, b, p):
		#if the angle is obtuse between PA and AB is obtuse then the closest vertex must be A
		dotA = (p.x - a.x) * (b.x - a.x) + (p.y - a.y) * (b.y - a.y)
		if (dotA <= 0):
			return func.distance(a, p)
		#if the angle is obtuse between PB and AB is obtuse then the closest vertex must be B
		dotB = (p.x - b.x) * (a.x - b.x) + (p.y - b.y) * (a.y - b.y)		 
		if (dotB <= 0):
			return func.distance(b, p)
		#calculate the point along AB that is the closest to P
		point = a + ((b - a) * dotA) / (dotA + dotB)
		#calculate the distance P-Point
		return func.distance(p, point)

	def isLOSOkay(self, a, b):
		return not self.doWallsObstructLineSegment(a, b)

	def doWallsObstructLineSegment(self, fromm, to):
		#test against the walls
		for wall in self.walls:
			#do a line segment intersection test
			if self.lineIntersection2D(fromm, to, wall.fromm, wall.to):
				return True
		return False

	def lineIntersection2D(self, A, B, C, D):
		rTop = (A.y-C.y)*(D.x-C.x)-(A.x-C.x)*(D.y-C.y)
		sTop = (A.y-C.y)*(B.x-A.x)-(A.x-C.x)*(B.y-A.y)
		bot = (B.x-A.x)*(D.y-C.y)-(B.y-A.y)*(D.x-C.x)
		if bot == 0: #parallel
			return False
		r = rTop/bot
		s = sTop/bot
		if (r > 0) and (r < 1) and (s > 0) and (s < 1):
			#lines intersect
			return True
		#lines do not intersect
		return False

	def lineIntersection2D_dist_point(self, A, B, C, D):
		rTop = (A.y-C.y)*(D.x-C.x)-(A.x-C.x)*(D.y-C.y)
		rBot = (B.x-A.x)*(D.y-C.y)-(B.y-A.y)*(D.x-C.x)

		sTop = (A.y-C.y)*(B.x-A.x)-(A.x-C.x)*(B.y-A.y)
		sBot = (B.x-A.x)*(D.y-C.y)-(B.y-A.y)*(D.x-C.x)
		if rBot == 0 or sBot == 0:
			#lines are parallel
			return False, 0, None # dist, point
		r = rTop/rBot
		s = sTop/sBot
		if (r > 0) and (r < 1) and (s > 0) and (s < 1):
			dist = func.distance(A, B) * r
			point = A + r * (B - A)
			return True, dist, point
		else:
			#dist = 0
			return False, 0, None #dist, point

	def findClosestPointOfIntersectionWithWalls(self, a, b):
		distance = float('Inf')
		for wall in self.walls:
			#dist = 0
			isIntersecting, dist, point = self.lineIntersection2D_dist_point(a, b, wall.fromm, wall.to)
			if isIntersecting:
				if dist < distance:
					distance = dist
					ip = point
		if distance < float('Inf'):
			return ip
		return None