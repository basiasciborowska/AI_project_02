import pygame
import Goal_TraverseEdge as te

class Goal_FollowPath:

	def __init__(self, own):
		self.type = "followPath"
		self.owner = own
		self.status = "inactive" # {active, inactive, completed, failed};
		self.subGoals = []
		#self.path = path

	def isComplete(self):
		return self.status == "completed"

	def isActive(self):
		return self.status == "active"

	def isInactive(self):
		return self.status == "inactive"

	def hasFailed(self):
		return self.status == "failed"

	def reactivateIfFailed(self):
		if self.hasFailed():
			self.status = "inactive"
  
	def activateIfInactive(self):
		if self.isInactive():
			self.activate()

	def removeAllSubgoals(self):
		for subGoal in self.subGoals:
			subGoal.terminate()
		self.subGoals = []
 
	def processSubgoals(self):
		# if item had been stolen
		#print self.owner.path
		if self.owner.path:
			if self.owner.path[len(self.owner.path)-1].to.extra_info:
				if not self.owner.path[len(self.owner.path)-1].to.extra_info.isActive:
					self.owner.path = []
					return "completed"
		#remove all completed and failed goals from the front of the subgoal list
		#print 'self.subgoals: ' + repr(self.subGoals[0])
		#print 'subgoal[0].isCompleted:' + repr(self.subGoals[0].isComplete())
		#print 'subgoal[0].hasFailed: ' + repr(self.subGoals[0].hasFailed())
		while self.subGoals and (self.subGoals[0].isComplete() or self.subGoals[0].hasFailed()):
			self.subGoals[0].terminate()
			#print 'self.subgoals: ' + repr(self.subGoals[0])
			self.subGoals.pop(0)
		#if any subgoals remain, process the one at the front of the list
		if self.subGoals:
			#grab the status of the front-most subgoal
			statusOfSubGoals = self.subGoals[0].process()
			#we have to test for the special case where the front-most subgoal reports 'completed' *and* the subgoal list contains additional goals.When this is the case, to ensure the parent keeps processing its subgoal list we must return the 'active' status.
			if statusOfSubGoals == "completed" and len(self.subGoals) > 1:
				return "active"
			return statusOfSubGoals  
		#no more subgoals to process - return 'completed'
		else:
			return "completed"

	def addSubgoal(self, goal):
		#self.subGoals.insert(0, goal)
		self.subGoals.append(goal)

	def activate(self):
		self.status = "active"
		s = '['
		for edge in self.owner.path:
			s += repr(self.owner.path.index(edge)) + ', '
		s += ']'
		print s
		self.owner.velocity = pygame.math.Vector2(0,0)
		if not self.owner.path:
			self.status = "completed"
			return
		edge = self.owner.path[0]
		self.owner.path.remove(edge)
		#edge = self.path.pop([0])
		if self.owner.path:
			self.addSubgoal(te.Goal_TraverseEdge(self.owner, edge, False))
		else:
			self.addSubgoal(te.Goal_TraverseEdge(self.owner, edge, True))

	def process(self):
		self.activateIfInactive()
		self.status = self.processSubgoals()
		#if there are no subgoals present check to see if the path still has edges remaining. If it does then call activate to grab the next edge.
		if self.status == "completed" and self.owner.path:
			self.activate()
		#print self.type
		return self.status

	def terminate(self):
		pass

	def printGoal(self):
	    print repr(self.type) + ': '
	    for subgoal in self.subGoals:
	      subgoal.printGoal()
