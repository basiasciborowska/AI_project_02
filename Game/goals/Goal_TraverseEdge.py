import pygame
import Functions as func

class Goal_TraverseEdge:

	def __init__(self, own, edge, isLastEdge):
		self.type = "traverseEdge"
		self.owner = own
		self.status = "inactive" # {active, inactive, completed, failed};
		#the edge the bot will follow
		self.pathEdge = edge
		#true if m_Edge is the last in the path.
		self.isLastEdgeInPath = isLastEdge
		#the estimated time the bot should take to traverse the edge
		self.timeExpected = 0.0
		#this records the time this goal was activated
		self.startTime = 0.0

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

	#returns true if the bot gets stuck
	def isStuck(self):
		timeTaken = pygame.time.get_ticks() - self.startTime
		# if timeTaken > self.timeExpected:
		# 	print 'Bot ' + repr(self.owner.position) + 'is stuck!'
		# 	return True
		return False;

	def activate(self):
		self.status = "active"
		#record the time the bot starts this goal
		self.startTime = pygame.time.get_ticks()
		#calculate the expected time required to reach the this waypoint. This value is used to determine if the bot becomes stuck 
		self.timeExpected = self.owner.calculateTimeToReachPosition(self.pathEdge.to.position)
		#factor in a margin of error for any reactive behavior
		marginOfError = 2.0
		self.timeExpected += marginOfError
		#set the steering target
		self.owner.steeringBehavior.target = self.pathEdge.to.position
		#Set the appropriate steering behavior. If this is the last edge in the path the bot should arrive at the position it points to, else it should seek
		# if self.isLastEdgeInPath:
		# 	self.owner.steeringBehaviorIsOn[3] = True
		# else:
		self.owner.steeringBehaviorIsOn[2] = True

	def process(self):
		#if status is inactive, call Activate()
		self.activateIfInactive()
		#if the bot has become stuck return failure
		if self.isStuck():
			self.status = "failed"
		#if the bot has reached the end of the edge return completed
		else:
			#if self.owner.position == self.pathEdge.to.position:
			if func.distance(self.owner.position, self.pathEdge.to.position) < 10:
				#print 'is completed: ' + repr(self.isComplete())
				self.status = "completed"
				#print 'is completed: ' + repr(self.isComplete())
		#print self.type
		return self.status
		
	def terminate(self):
		#turn off steering behaviors.
		self.owner.steeringBehaviorIsOn[2] = False
		self.owner.steeringBehaviorIsOn[3] = False
		#return max speed back to normal
		#self.owner.velocity = pygame.math.Vector2(0, 0)			??????????????

	def printGoal(self):
	    print repr(self.type)
