import pygame
import math
import numpy
import random
import Obstacle as obs
import Predator as pr

def perpendicular(vector):
	return pygame.math.Vector2(-vector.y, vector.x)

def rotate(matrix, heading):
	rotation_matrix = ([[heading.x, heading.y, 0], [-heading.y, heading.x, 0], [0, 0, 1]])
	return numpy.dot(matrix, rotation_matrix)

def translate(matrix, position):
	translation_matrix = ([[1, 0, 0], [0, 1, 0], [position.x, position.y, 1]])
	return numpy.dot(matrix, translation_matrix)

def transformVector(matrix, point):
	x = matrix[0, 0] * point.x + matrix[1, 0] * point.y + matrix[2, 0]
	y = matrix[0, 1] * point.x + matrix[1, 1] * point.y + matrix[2, 1]
	return pygame.math.Vector2(x, y)

def pointToLocalSpace(point, heading, position):
	side = perpendicular(heading)
	vector = pygame.math.Vector2(-position.dot(heading), -position.dot(side))
	return pygame.math.Vector2(heading.x * point.x + heading.y * point.y + vector.x, side.x * point.x + side.y * point.y + vector.y)

def pointToWorldSpace(point, heading, position):
	transformation_matrix = numpy.identity(3)
	transformation_matrix = rotate(transformation_matrix, heading)
	transformation_matrix = translate(transformation_matrix, position)
	return transformVector(transformation_matrix, point)

def vectorToWorldSpace(vector, heading):
	transformation_matrix = numpy.identity(3)
	transformation_matrix = rotate(transformation_matrix, heading)
	return transformVector(transformation_matrix, vector)

def truncate(force, max_f):
	if force.x > max_f:
		force.x = max_f
	if force.x < -max_f:
		force.x = -max_f
	if force.y > max_f:
		force.y = max_f
	if force.y < -max_f:
		force.y = -max_f
	return force

def walls(position, display, size):
	if position.x > display[0] - size:
		position.x = display[0] - size
	elif position.x < size:
		position.x = size
	if position.y > display[1] - size:
		position.y = display[1] - size
	elif position.y < size:
		position.y = size
	return position 

def distance(point1, point2):
	return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def vectorFromPointToPoint(point1, point2):
	return pygame.math.Vector2(point2.x - point1.x, point2.y - point1.y)

def addObstacles(no, display):
	Obstacles = []
	tmp_display = [display[0] - 140, display[1] - 140]

	sqrt_no = math.sqrt(no)

	iterator_hor = 0
	iterator_vert = 0
	hor_interval = int(tmp_display[0]/sqrt_no)
	vert_interval = int(tmp_display[1]/sqrt_no)
	for i in range (no):
		if iterator_hor+1 > sqrt_no:
			iterator_hor = 0
			iterator_vert += 1
		x = random.randint(iterator_hor*hor_interval + 60, iterator_hor*hor_interval + hor_interval - 60)
		y = random.randint(iterator_vert*vert_interval + 60, iterator_vert*vert_interval + vert_interval - 60)
		r = random.randrange(30, 50)				# min_r, max_r
		Obstacles.append(obs.Obstacle(x + 70, y + 70, r))
		iterator_hor += 1
	return Obstacles

def addPredators(no, display, obstacles):
	Predators = []

	for i in range(no):
		x = random.randint(20, display[0]-20)
		y = random.randint(20, display[1]-20)
		Predators.append(pr.Predator(x, y, obstacles, Predators))
	return Predators

def get_hiding_position(obstacle, enemy_position):
	distance_from_boundary = 40
	distance_away = obstacle.radius + distance_from_boundary
	vector_to_obstacle = (obstacle.position - enemy_position).normalize()
	return (vector_to_obstacle * distance_away) + obstacle.position #position of hiding spot

def displayMessage(text, display, gameDisplay, x=0.5, y=0.5, fontSize=15, fontStyle=None, update=False):
    x *= display[0]
    y *= display[1]
    if fontStyle is None: fontStyle = pygame.font.Font( 'freesansbold.ttf', fontSize )
    textSurf = fontStyle.render( text, True, (255, 255, 255) )
    textRect = textSurf.get_rect()
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)
    if update: pygame.display.update()

