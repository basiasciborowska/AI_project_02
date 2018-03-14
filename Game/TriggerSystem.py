import Trigger as tr

class TriggerSystem:

	def __init__(self):
		self.triggers = []

	def addTriggers(self, graph):
		no_heathGivers = 5
		no_weaponGivers = 10
		no_railguns = 5
		no_rocket = 5
		for i in range(no_heathGivers):
			node_id = i * 29
			trigger = tr.Trigger(node_id, 60, "Health_Giver", None)
			self.triggers.append(trigger)
			graph.nodes[node_id].extra_info = trigger
		for i in range(no_railguns):
			node_id = (5 + i) * 29
			trigger = tr.Trigger(node_id, 100, "Weapon_Giver", "Railgun")
			self.triggers.append(trigger)
			graph.nodes[node_id].extra_info = trigger
		for i in range(no_rocket):
			node_id = (10 + i) * 29
			trigger = tr.Trigger(node_id, 100, "Weapon_Giver", "Rocket")
			self.triggers.append(trigger)
			graph.nodes[node_id].extra_info = trigger
		
	def updateTriggers(self):
		for trigger in self.triggers:
			trigger.updateTrigger()

	def tryTriggers(self, players):
		for player in players:
			if player.isAlive: # and isReadyForTriggerUpdate
				for trigger in self.triggers:
					trigger.tryTrigger(player)

	def update(self, players):
		self.updateTriggers()
		self.tryTriggers(players)

	def drawTriggers(self, screen, game):
		for trigger in self.triggers:
			trigger.drawTrigger(screen, game)