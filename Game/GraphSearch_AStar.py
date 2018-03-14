import Functions as func
import PriorityQueue as pque
import GraphEdge as ge

class GraphSearch_AStar:

	def __init__(self, gr, source, target):
		self.graph = gr
		self.gCosts = [0] * len(self.graph.nodes)
		self.fCosts = [0] * len(self.graph.nodes)
		self.shortestPathTree = [None] * len(self.graph.nodes)
		self.searchFrontier = [None] * len(self.graph.nodes)
		self.source = source
		self.target = target

	def calculateHeuristicCost(self, node_1_id, node_2_id):
		return func.distance(self.graph.nodes[node_1_id].position, self.graph.nodes[node_2_id].position)

	def getCostToTheTarget(self):
		return self.gCosts[self.target]

	def getPathToTarget(self):
		#print self.shortestPathTree
		#print self.searchFrontier
		path = []
		#just return an empty path if no target or no path found
  		if self.target < 0:  
  			return path  
  		nd = self.target
  		#print 'target: ' + repr(nd)
  		#print 'source: ' + repr(self.source)
  		#print self.shortestPathTree[nd]
		path.insert(0, nd)
		while nd != self.source and self.shortestPathTree[nd] != None:
			nd = self.shortestPathTree[nd].fromm.id
			path.insert(0, nd)
			#print nd
			#print self.shortestPathTree[nd]
		return path

	def getEdgePath(self):
		path = self.getPathToTarget()
		#print 'path:' + repr(path)
		edgePath = []
		for idx in path:
			idx_next = path[path.index(idx) + 1 % len(path)]
			#print repr(idx) + ', ' + repr(idx_next)	
			node_from = self.graph.nodes[idx]
			node_to = self.graph.nodes[idx_next]
			edgePath.append(ge.GraphEdge(node_from, node_to, func.distance(node_from.position, node_to.position)))
			if idx_next == path[len(path) - 1]:
				break
		return edgePath

	def search(self):
		pq = pque.IndexedPriorityQLow(self.fCosts, len(self.graph.nodes))
		pq.insert(self.source)
		while not pq.empty():
			nextClosesNode = pq.pop()
			self.shortestPathTree[nextClosesNode] = self.searchFrontier[nextClosesNode]
			if nextClosesNode == self.target:
				return
			for edge in self.graph.edges[self.graph.nodes[nextClosesNode]]:
				hcost = self.calculateHeuristicCost(self.target, edge.to.id)
				gcost = self.gCosts[nextClosesNode] + edge.cost
				if self.searchFrontier[edge.to.id] == None:
					self.fCosts[edge.to.id] = gcost + hcost
					self.gCosts[edge.to.id] = gcost
					pq.insert(edge.to.id)
					self.searchFrontier[edge.to.id] = edge
				elif gcost < self.gCosts[edge.to.id] and self.shortestPathTree[edge.to.id] == None:
					self.fCosts[edge.to.id] = gcost + hcost
					self.gCosts[edge.to.id] = gcost
					pq.changePriority(edge.to.id)
					self.searchFrontier[edge.to.id] = edge
