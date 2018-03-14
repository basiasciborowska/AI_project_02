import numpy
import pygame
import random
import math
import Functions as func

class SteeringBehaviors:

  separationWeight = 10.0
  wallAvoidanceWeight = 10.0
  wanderWeight = 1.0
  seekWeight = 0.5
  arriveWeight = 1.0
  wander_radius = 70
  wander_distance = 570
  wander_jitter = 120

  def __init__(self, own):
    self.steeringForce = pygame.math.Vector2(0, 0)
    self.owner = own
    self.target = None
    self.deceleration = 2
    self.theta = random.random() * 2 * math.pi
    self.wander_target = pygame.math.Vector2(self.wander_radius * math.cos(self.theta), self.wander_radius * math.sin(self.theta))    #create a vector to a target position on the wander circle

  def calculate(self):
    self.steeringForce = pygame.math.Vector2(0, 0)
    self.steeringForce = self.calculatePrioritized()
    return self.steeringForce

  def forwardComponent():
    return numpy.dot(self.owner.heading, self.steeringForce)

  def sideComponent():
    return numpy.dot(func.perpendicular(self.owner.heading), self.steeringForce)

  def accumulateForce(self, runningTot, forceToAdd):
    #calculate how much steering force the vehicle has used so far
    magnitudeSoFar = runningTot.length()
    #calculate how much steering force remains to be used by this vehicle
    magnitudeRemaining = self.owner.maxForce - magnitudeSoFar
    #return false if there is no more force left to use
    if magnitudeRemaining <= 0.0:
      return runningTot
    #calculate the magnitude of the force we want to add
    magnitudeToAdd = forceToAdd.length()
    #if the magnitude of the sum of ForceToAdd and the running total does not exceed the maximum force available to this vehicle, just add together. Otherwise add as much of the ForceToAdd vector is possible without going over the max.
    if magnitudeToAdd < magnitudeRemaining:
      runningTot += forceToAdd
    else:
      magnitudeToAdd = magnitudeRemaining
    #add it to the steering force
    runningTot += forceToAdd.normalize() * magnitudeToAdd
    return runningTot


  def calculatePrioritized(self):
    if self.owner.position == self.target:
      return self.steeringForce
    force = pygame.math.Vector2(0, 0)

    if self.owner.steeringBehaviorIsOn[0] == True:
      print 'wallAvoidance'
      force = self.wallAvoidance() * self.wallAvoidanceWeight
      self.accumulateForce(self.steeringForce, force)
      if self.steeringForce == self.owner.maxForce:
        return self.steeringForce

    if self.owner.steeringBehaviorIsOn[1] == True:
      print 'separation'
      force = self.separation() * self.separationWeight
      self.accumulateForce(self.steeringForce, force)
      if self.steeringForce == self.owner.maxForce:
        return self.steeringForce

    if self.owner.steeringBehaviorIsOn[2] == True:
      print 'seek to ' + repr(self.target)
      force = self.seek(self.target) * self.seekWeight
      if force.length() != 0:
        self.accumulateForce(self.steeringForce, force)
      # else:
      #   print "dsbkjdbvkd"
      if self.steeringForce == self.owner.maxForce:
        return self.steeringForce

    if self.owner.steeringBehaviorIsOn[3] == True:
      print 'arrive'
      force = self.arrive(self.target, self.deceleration) * self.arriveWeight
      self.accumulateForce(self.steeringForce, force)
      if self.steeringForce == self.owner.maxForce:
        return self.steeringForce

    if self.owner.steeringBehaviorIsOn[4] == True:
      print 'wander'
      force = self.wander() * self.wanderWeight
      self.accumulateForce(self.steeringForce, force)
      if self.steeringForce == self.owner.maxForce:
        return self.steeringForce

    #if self.owner.steeringBehaviorIsOn[0] == False and self.owner.steeringBehaviorIsOn[1] == False and self.owner.steeringBehaviorIsOn[2] == False and self.owner.steeringBehaviorIsOn[3] == False and self.owner.steeringBehaviorIsOn[4] == False:
      #print self.steeringForce
    return self.steeringForce

  def seek(self, target):
    desiredVelocity = (target - self.owner.position).normalize() * self.owner.maxSpeed
    #print "maxSpeed: " + repr((target - self.owner.position).normalize() * self.owner.maxSpeed)
    #print "desired velocity: " + repr(desiredVelocity)
    #print "owner's velocity: " + repr(self.owner.velocity)
    return desiredVelocity - self.owner.velocity

  def arrive(self, target, deceleration):
    toTarget = target - self.owner.position
    dist = toTarget.length()
    if dist > 0:
      decelerationTweaker = 0.3
      speed =  dist / (deceleration * decelerationTweaker)
      if speed > self.owner.maxSpeed:
        speed = self.owner.maxSpeed
      desiredVelocity =  toTarget * speed / dist
      return desiredVelocity - self.owner.velocity
    return pygame.math.Vector2(0, 0)

  def wander(self):
    self.wander_target += pygame.math.Vector2(random.uniform(-1,1) * self.wander_jitter, random.uniform(-1,1) * self.wander_jitter)
    self.wander_target = self.wander_target.normalize()
    self.wander_target *= self.wander_radius

    target_local = self.wander_target + pygame.math.Vector2(self.wander_distance, 0)
    target_world = func.pointToWorldSpace(target_local, self.character.heading, self.character.position)
    return target_world - self.character.position 

  def wallAvoidance(self):
    pass

  def separation(self):
    steering_force = pygame.math.Vector2(0, 0)
    for player in self.owner.world.players:
      if player != self.owner:
        if func.distance(player.position, self.owner.position) < 80:
          to_agent = self.owner.position - player.position
          if to_agent.length() != 0:
            steering_force += to_agent.normalize() / to_agent.length()
          else:
            steering_force += self.owner.heading / 0.0001
    return steering_force


