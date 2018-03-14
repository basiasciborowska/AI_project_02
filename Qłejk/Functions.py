import pygame
import math
import numpy
import random
#import Player as pls
import Walls as wal
import Graph as gr
import GraphNode as gn
import GraphEdge as ge

def perpendicular(vector):
	return pygame.math.Vector2(-vector.y, vector.x)

def sign(v1, vector):
	if v1.y * vector.x > v1.x * vector.y:
		return -1 # anticlockwise
	else:
		return 1 # clockwise

def rotate(matrix, heading):
	rotation_matrix = ([[heading.x, heading.y, 0], [-heading.y, heading.x, 0], [0, 0, 1]])
	return numpy.dot(matrix, rotation_matrix)

def rotate_angular(matrix, rot):
	sin = math.sin(rot)
	cos = math.cos(rot)
	rotation_matrix = ([[cos, sin, 0], [-sin, cos, 0], [0, 0, 1]])
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

def rotateAroundOrigin(v, ang):
	transformation_matrix = numpy.identity(3)
	transformation_matrix = rotate_angular(transformation_matrix, ang)
	return transformVector(transformation_matrix, v)

def distance(point1, point2):
	return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def distanceSq(point1, point2):
	return (point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2

def vectorFromPointToPoint(point1, point2):
	return pygame.math.Vector2(point2.x - point1.x, point2.y - point1.y)

def isSecondInFOVOfFirst(posFirst, facingFirst, posSecond, fov):
	toTarget = (posSecond - posFirst).normalize()
	return numpy.dot(facingFirst, toTarget) >= math.cos(fov / 2.0)

def displayMessage(text, display, gameDisplay, x=0.5, y=0.5, fontSize=15, fontStyle=None, update=False):
    x *= display[0]
    y *= display[1]
    if fontStyle is None: fontStyle = pygame.font.Font( 'freesansbold.ttf', fontSize )
    textSurf = fontStyle.render( text, True, (255, 255, 255) )
    textRect = textSurf.get_rect()
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)
    if update: pygame.display.update()
