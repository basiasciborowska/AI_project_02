import Goal_MoveToPosition as mtp
import Goal_HuntTarget as ht

class Goal_AttackTarget:

	def __init__(self, own):
		self.type = "attackTarget"
		self.owner = own
		self.status = "inactive" # {active, inactive, completed, failed};
		self.subGoals = []

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
		#remove all completed and failed goals from the front of the subgoal list
		while self.subGoals and (self.subGoals[0].isComplete() or self.subGoals[0].hasFailed()):
			self.subGoals[0].terminate()
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
		self.subGoals.insert(0, goal)

	def activate(self):
		self.status = "active"
		self.removeAllSubgoals()
		if not self.owner.targetingSystem.isTargetPresent():
			self.status = "completed"
			return
		if self.owner.targetingSystem.isTargetShootable():
			self.addSubgoal(mtp.Goal_MoveToPosition(self.owner, self.owner.targetingSystem.currentTarget.position))
		else:
			self.addSubgoal(ht.Goal_HuntTarget(self.owner))

	def process(self):
		self.activateIfInactive()
		self.status = self.processSubgoals()
		self.reactivateIfFailed()
		#print self.type
		return self.status

	def terminate(self):
		self.status = "completed"

	def printGoal(self):
	    print repr(self.type) + ': '
	    for subgoal in self.subGoals:
	      subgoal.printGoal()