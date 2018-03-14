import Functions as func
import Entity as ent

class Game:

	def __init__(self, no_obstacles, no_predators, display):
		self.play_game = True

		self.Obstacles = func.addObstacles(no_obstacles, (display[0], display[1]))
		self.Victim = ent.Entity(400, 300, self.Obstacles)
		self.Predators = func.addPredators(no_predators, (display[0], display[1]), self.Obstacles)
		#self.Victom = ent.Entity(display_width/2, display_height/2, self.Obstacles)
		self.RailGun = None