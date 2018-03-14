

class MemoryRecord:

	def __init__(self):
		#records the time the opponent was last sensed (seen or heard). This is used to determine if a bot can 'remember' this record or not. (if CurrentTime() - m_dTimeLastSensed is greater than the bot's memory span, the data in this record is made unavailable to clients)
		self.timeLastSensed = -999
		#it can be useful to know how long an opponent has been visible. This variable is tagged with the current time whenever an opponent first becomes visible. It's then a simple matter to calculate how long the opponent has been in view (CurrentTime - fTimeBecameVisible)
		self.timeBecameVisible = -999
		#it can also be useful to know the last time an opponent was seen
		self.timeLastVisible = 0
		#a vector marking the position where the opponent was last sensed. This can be used to help hunt down an opponent if it goes out of view
		self.lastSensedPosition = None #pygame.math.Vector2
		#set to true if opponent is within the field of view of the owner
		self.withinFOV = False
		#set to true if there is no obstruction between the opponent and the owner, permitting a shot.
		self.shootable = False