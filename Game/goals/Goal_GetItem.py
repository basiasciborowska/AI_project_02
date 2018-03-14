import Goal_FollowPath as fp

def itemTypeToGoalType(itemType, weaponType):
	if itemType == "Health_Giver":
		return "getItem_health"
	if itemType == "Weapon_Giver":
		if weaponType == "Railgun":
			return "getItem_railgun"
		if weaponType == "Rocket":
			return "getItem_rocket"

class Goal_GetItem:

	def __init__(self, own, itemType, weaponType):
		self.type = itemTypeToGoalType(itemType, weaponType)
		self.owner = own
		self.status = "inactive" # {active, inactive, completed, failed};
		self.subGoals = []
		self.itemToGet = (itemType, weaponType)
		self.isFollowingPath = False
        #self.giverTrigger = None #trigger

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
			#self.subGoals.pop(self.subGoals.index(self.subGoals[0]))
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
		#self.giverTrigger = None
		itemType, weaponType = self.itemToGet
		self.owner.path = self.owner.pathPlanner.createPathToItem(itemType, weaponType)
		self.removeAllSubgoals()
		self.addSubgoal(fp.Goal_FollowPath(self.owner))
		#self.giverTrigger = static_cast<Raven_Map::TriggerType*>(msg.ExtraInfo) # lokacja konkretnego celu na mapie - wykrywanie czy trigger zostal skradziony

	def process(self):
		self.activateIfInactive()
		# if self.hasItemBeenStolen():
		# 	self.terminate()
		# else:
		self.status = self.processSubgoals()
		#print self.type
		return self.status

	def terminate(self):
		self.status = "completed"

	def hasItemBeenStolen():
		pass

	def printGoal(self):
	    print repr(self.type) + ': '
	    for subgoal in self.subGoals:
	      subgoal.printGoal()
