import random
import Functions as func
import math

class Wandering():

	def __init__(self):
		self.name = "Wandering"

		self.wandering_time = 0

		self.distance_to_enemy_last_step = float('Inf')
		self.distance_to_enemy = float('Inf')
		self.distance_change = 0

	def execute(self, character, victim):
		self.wandering_time += 1
		self.distance_to_enemy_last_step = self.distance_to_enemy
		self.distance_to_enemy = func.distance(character.position, victim.position)
		if self.distance_to_enemy_last_step < float('Inf'):
			self.distance_change = self.distance_to_enemy_last_step - self.distance_to_enemy
		
		steering_force_wan = character.steering_behavior.wander() * 15

		if not character.isHidden:
			if (self.distance_change > character.wander_speed/35 and self.wandering_time > character.wander_speed*2): # or self.wandering_time > 300:
				character.state_machine.changeState(Hide())

		if character.isInGroup:
			character.state_machine.changeState(Attack())

		return steering_force_wan

class Hide():

	def __init__(self):
		self.name = "Hide"

		self.hiding_time = random.randint(0, 120)

	def execute(self, character, victim):
		steering_force_wan = character.steering_behavior.wander() * 5
		steering_force_hide, hiding_spot = character.steering_behavior.hide(victim)

		if character.isHidden:
		# if func.distance(character.position, hiding_spot) < 30:
			self.hiding_time += 1
			if self.hiding_time > 150:
				character.state_machine.changeState(Wandering())

		if character.isInGroup:
			character.state_machine.changeState(Attack())

		return steering_force_hide * 35 + steering_force_wan

class Attack():

	def __init__(self):
		self.name = "Attack"

	def execute(self, character, victim):
		steering_force_att = character.steering_behavior.attack(victim)

		# if not character.isInGroup:
		# 	character.state_machine.changeState(Hide())

		return steering_force_att * 100
