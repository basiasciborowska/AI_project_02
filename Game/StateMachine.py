import PredatorStates as ps

class StateMachine:
	
	def __init__(self, own):
		self.owner = own
		self.current_state = ps.Hide()

	def update(self, character, victim):
		print self.current_state.name
		return self.current_state.execute(character, victim)

	def changeState(self, new_state):
		self.current_state = new_state