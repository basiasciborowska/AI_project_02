import pygame
import GraphNode as gn
import GraphEdge as ge
import Functions as func

class Graph:

	def __init__(self):
		self.nodes = []
		self.edges = {}
		self.nextNodeId = 0

	def addNode(self, position):
		node = gn.GraphNode(self.nextNodeId, position, None)
		if self.isNewNode(node):
			self.nodes.append(node)
			self.edges[node] = []
			self.nextNodeId += 1
			return True
		return False

	def addEdge(self, fr, t):
		distance = func.distance(fr, t)
		node_from = self.nodeAtPosition(fr)
		if self.isNewEdge(node_from, t):		
			new_node = self.addNode(t)
			node_to = self.nodeAtPosition(t)
			self.edges[node_from].append(ge.GraphEdge(node_from, node_to, distance))
			self.edges[node_to].append(ge.GraphEdge(node_to, node_from, distance))
			return new_node
		return False

	def isNewNode(self, node):
		for n in self.nodes:
			if n.position == node.position:
				return False
		return True

	def isNewEdge(self, node, t):
		for e in self.edges[node]:
			if e.to.position == t:
				return False
		return True

	def drawGraph(self, screen):
		for node in self.nodes:
			node.drawNode(screen)
			for edge in self.edges[node]:
				edge.drawEdge(screen)

	def printGraph(self):
		for node in self.nodes:
			tmp = repr(node.id) + ': '
			for edge in self.edges[node]:
				tmp += repr(edge.to.id) + ', '
			print tmp
	
	def nodeAtPosition(self, position):
		for node in self.nodes:
			if node.position == position:
				return node
		return None
		