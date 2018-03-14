import random
import Goal_MoveToPosition as mp
import Goal_Explore as e
import Goal_GetItem as gi
import Goal_AttackTarget as at
import Evaluators as ev

class Goal_Think:

  lowRangeOfBias = 0.5
  highRangeOfBias = 1.5

  def __init__(self, own):
    self.healthBias = random.uniform(self.lowRangeOfBias, self.highRangeOfBias)
    self.rocketLauncherBias = random.uniform(self.lowRangeOfBias, self.highRangeOfBias)
    self.railgunBias = random.uniform(self.lowRangeOfBias, self.highRangeOfBias)
    self.exploreBias = random.uniform(self.lowRangeOfBias, self.highRangeOfBias)
    self.attackBias = random.uniform(self.lowRangeOfBias, self.highRangeOfBias)
    self.type = "think"
    self.owner = own
    self.status = "inactive" # {active, inactive, completed, failed};
    self.subGoals = []
    self.evaluators = [ev.GetHealthGoal_Evaluator(self.healthBias), ev.ExploreGoal_Evaluator(self.exploreBias), ev.AttackTargetGoal_Evaluator(self.attackBias), ev.GetWeaponGoal_Evaluator(self.railgunBias, "Railgun"), ev.GetWeaponGoal_Evaluator(self.rocketLauncherBias, "Rocket")]
    #self.evaluators = [ev.GetHealthGoal_Evaluator(self.healthBias), ev.GetWeaponGoal_Evaluator(self.railgunBias, "Railgun"), ev.GetWeaponGoal_Evaluator(self.rocketLauncherBias, "Rocket")]

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
    self.arbitrate()
    self.status = "active"

  def process(self):
    self.activateIfInactive()
    subgoalStatus = self.processSubgoals()
    if subgoalStatus == "completed" or subgoalStatus == "failed":
      self.status = "inactive"
    return self.status

  def terminate():
    pass

  def arbitrate(self):
    best = 0
    mostDesirable = None
    for evaluator in self.evaluators:
      desirabilty = evaluator.calculateDesirability(self.owner)
      if desirabilty >= best:
        best = desirabilty
        mostDesirable = evaluator
    if mostDesirable:
      mostDesirable.setGoal(self.owner)

  def notPresent(self, GoalType):
    if self.subGoals:
      return self.subGoals[0].type != GoalType
    return True

  def addGoal_MoveToPosition(self, pos):
    self.addSubgoal(mp.Goal_MoveToPosition(self.owner, pos))

  def addGoal_Explore(self):
    if self.notPresent("explore"):
      self.removeAllSubgoals()
      self.addSubgoal(e.Goal_Explore(self.owner))

  def addGoal_GetItem(self, ItemType, WeaponType):
    if self.notPresent(gi.itemTypeToGoalType(ItemType, WeaponType)):
      self.removeAllSubgoals()
      self.addSubgoal(gi.Goal_GetItem(self.owner, ItemType, WeaponType))

  def addGoal_AttackTarget(self):
    if self.notPresent("attackTarget"):
      self.removeAllSubgoals()
      self.addSubgoal(at.Goal_AttackTarget(self.owner))

    def printGoal(self):
      print repr(self.type) + ': '
      for subgoal in self.subGoals:
        subgoal.printGoal()
