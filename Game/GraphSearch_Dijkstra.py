import Functions as func
import PriorityQueue as pque
import GraphEdge as ge

class GraphSearch_Dijkstra:

	def __init__(self, gr, source, target, target_weapon):
		self.graph = gr
		self.costToThisNode = [0] * len(self.graph.nodes)
		self.shortestPathTree = [None] * len(self.graph.nodes)
		self.searchFrontier = [None] * len(self.graph.nodes)
		self.source = source
		self.target = target
		self.target_weapon = target_weapon

	def getCostToNode(nd):
		return self.costToThisNode[nd]

	def isSatisfied(self, currentNodeId):
		isSatisfied = False
		node = self.graph.nodes[currentNodeId]
		if node.extra_info != None:
			if node.extra_info.isActive and node.extra_info.type == self.target:
				if self.target == "Weapon_Giver":
					if node.extra_info.weapon == self.target_weapon:
						isSatisfied = True
				if self.target == "Health_Giver":
					isSatisfied = True
		return isSatisfied

	def getPathToTarget(self):
		path = []
		#just return an empty path if no target or no path found
  		if self.target < 0:  
  			return path  
  		nd = self.target
		path.insert(0, nd)
		print "nd: " + repr(nd)
		while nd != self.source and self.shortestPathTree[nd] != None:
			nd = self.shortestPathTree[nd].fromm.id
			path.insert(0, nd)
		return path

	def getEdgePath(self):
		path = self.getPathToTarget()
		edgePath = []
		for idx in path:
			idx_next = path[path.index(idx) + 1 % len(path)]
			node_from = self.graph.nodes[idx]
			node_to = self.graph.nodes[idx_next]
			edgePath.append(ge.GraphEdge(node_from, node_to, func.distance(node_from.position, node_to.position)))
			if idx_next == path[len(path) - 1]:
				break
		return edgePath

	def search(self):
		pq = pque.IndexedPriorityQLow(self.costToThisNode, len(self.graph.nodes))
		pq.insert(self.source)
		while not pq.empty():
			nextClosesNode = pq.pop()
			self.shortestPathTree[nextClosesNode] = self.searchFrontier[nextClosesNode]
			#if nextClosesNode == self.target:
			#	return
			if self.isSatisfied(nextClosesNode):
				self.target = nextClosesNode
				return
			for edge in self.graph.edges[self.graph.nodes[nextClosesNode]]:
				newCost = self.costToThisNode[nextClosesNode] + edge.cost
				if self.searchFrontier[edge.to.id] == None:
					self.costToThisNode[edge.to.id] = newCost
					pq.insert(edge.to.id)
					self.searchFrontier[edge.to.id] = edge
				elif newCost < self.costToThisNode[edge.to.id] and self.shortestPathTree[edge.to.id] == None:
					self.costToThisNode[edge.to.id] = newCost
					pq.changePriority(edge.to.id)
					self.searchFrontier[edge.to.id] = edge
		print "pq empty"
		self.target = self.source
