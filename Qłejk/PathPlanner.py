import pygame
import Functions as func
import GraphNode as gn
import GraphEdge as ge
import GraphSearch_AStar as aStar
import GraphSearch_Dijkstra as dij

class PathPlanner:

	def __init__(self, own, gr):
		self.owner = own
		self.navGraph = gr
		self.destination = pygame.math.Vector2(-1, -1)
		self.pathPlanned = False

	def getCostToClosestItem(giverType):
		nd = self.getClosestNodeToPosition(self.owner.position)
		if nd == -1:
			return -1
		closestSoFar = float('Inf')
		for trigger in self.owner.world.triggerSystem.triggers:
			if trigger.type == giverType and trigger.isActive:
				cost = self.owner.world.calculateCostToTravelBetweenNodes(nd, trigger.graphNodeId)
				if cost < closestSoFar:
					closestSoFar = cost
		if closestSoFar == float('Inf'):
			return -1
		return closestSoFar

	def getClosestNodeToPosition(self, pos):
		closestSoFar = float('Inf')
		closestNode  = -1
		#when the cell space is queried this the the range searched for neighboring graph nodes. This value is inversely proportional to the density of a navigation graph (less dense = bigger values)
		neighbors = []
		#print pos.x
		#print pos.y
		for node in self.navGraph.nodes:
			if node.position == pos:
				#print 'neighbor position: ' + repr(node.position.x) + ", " + repr(node.position.y)
				#print node.id
				return node.id
			elif func.distance(node.position, pos) < 36:
				neighbors.append(node)
		for neighbor in neighbors:
			#print 'neighbor position: ' + repr(neighbor.position.x) + ", " + repr(neighbor.position.y)
			#if the path between this node and pos is unobstructed calculate the distance
			if not self.owner.world.isPathObstructed(pos, neighbor.position, self.owner.size):
				dist = func.distanceSq(pos, neighbor.position)
				#keep a record of the closest so far
				if dist < closestSoFar:
					closestSoFar = dist
					closestNode  = neighbor.id
					#print closestNode
		#print closestNode
		return closestNode

	def smoothPath(self, path):
		edge1 = 0
		edge2 = 0
		while edge1 <= len(path):
			edge2 = edge1
			edge2 += 1
			while edge2 < len(path):
				if not self.owner.world.isPathObstructed(path[edge1].fromm.position, path[edge2].to.position, self.owner.size):
					path[edge1].to = path[edge2].to
					edge1 += 1
					while edge1 <= edge2:
						path.remove(path[edge1])
						edge1 += 1
					edge2 += 1
					edge1 = edge2
					edge1 -= 1
				else:
					edge2 += 1
				print 'edge1: ' + repr(edge1)
				print 'edge2: ' + repr(edge2)
			edge1 += 1
		return path

	def smoothPath2(self, path):
		edge1 = 0
		edge2 = 1
		while edge2 < len(path):
			if not self.owner.world.isPathObstructed(path[edge1].fromm.position, path[edge2].to.position, self.owner.size):
				path[edge1].to = path[edge2].to
				path.remove(path[edge2])
			else:
				edge1 = edge2
				edge2 += 1
			#print 'edge1: ' + repr(edge1)
			#print 'edge2: ' + repr(edge2)
		return path

	def createPathToPosition(self, targer_pos):
		#destinationPosition = targer_pos
		path = []
		closestNodeToTarget = self.getClosestNodeToPosition(targer_pos)
		if closestNodeToTarget == -1:
			#no path posiible
			return path
		if not self.owner.world.isPathObstructed(self.owner.position, targer_pos, self.owner.size):
			print 'path unobstructed'
			path.append(ge.GraphEdge(gn.GraphNode(-1, pygame.math.Vector2(self.owner.position.x, self.owner.position.y), None), gn.GraphNode(-1, targer_pos, None), func.distance(self.owner.position, targer_pos)))
			self.pathPlanned = True
			return path
		closestNodeToBot = self.getClosestNodeToPosition(self.owner.position)
		if closestNodeToBot == -1:
			#no path posiible
			return path
		grSearch = aStar.GraphSearch_AStar(self.navGraph, closestNodeToBot, closestNodeToTarget)
		grSearch.search()
		path = grSearch.getEdgePath()
		if path:
			node_own_pos = gn.GraphNode(-1, pygame.math.Vector2(self.owner.position.x, self.owner.position.y), None)
			path.insert(0, ge.GraphEdge(node_own_pos, path[0].fromm, func.distance(self.owner.position, path[0].fromm.position)))
			path.append(ge.GraphEdge(path[len(path) - 1].to, gn.GraphNode(-1, targer_pos, None), func.distance(targer_pos, path[len(path) - 1].to.position)))
			for edge in path:
				#print 'from: ' + repr(edge.fromm.position) + 'to: ' + repr(edge.to.position)
				edge.color = pygame.math.Vector3(0, 255, 255)
			self.pathPlanned = True
			path = self.smoothPath(path)
			return path
		else:
			#no path find by search
			return path

	def createPathToItem(self, item_type, weapon_type):
		path = []
		closestNodeToBot = self.getClosestNodeToPosition(self.owner.position)
		if closestNodeToBot == -1:
			return path
		grSearch = dij.GraphSearch_Dijkstra(self.navGraph, closestNodeToBot, item_type, weapon_type)
		grSearch.search()
		path = grSearch.getEdgePath()
		if path:
			node_own_pos = gn.GraphNode(-1, pygame.math.Vector2(self.owner.position.x, self.owner.position.y), None)
			if path[0].fromm.position != node_own_pos.position:
				path.insert(0, ge.GraphEdge(node_own_pos, path[0].fromm, func.distance(self.owner.position, path[0].fromm.position)))
			for edge in path:
				#print 'from: ' + repr(edge.fromm.position) + 'to: ' + repr(edge.to.position)
				edge.color = pygame.math.Vector3(255, 0, 0)
			self.pathPlanned = True
			edge = path[0]
			#path.remove(edge)
			#path = self.smoothPath(path)
			return path
		else:
			#no path find by search
			return path