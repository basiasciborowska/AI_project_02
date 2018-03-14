import pygame
import Functions as func

class Projectile:

  def __init__(self, own, targ, t):
    self.type = t

    self.shooter = own
    self.target = targ
    #self.world = self.shooter.world # !!!
    self.origin = pygame.math.Vector2(self.shooter.position.x, self.shooter.position.y)
    self.dead = False
    self.impacted = False
    self.impactPoint = None
    self.timeOfCreation = pygame.time.get_ticks()

    self.position = pygame.math.Vector2(self.shooter.position.x, self.shooter.position.y)
    self.velocity = pygame.math.Vector2(0, 0)
    self.heading = pygame.math.Vector2(self.shooter.facing.x, self.shooter.facing.y)
    if self.type == "Rocket":
      self.damageInflicted = 60
      self.splashDamage = 40
      self.mass = 1
      self.maxSpeed = 9.0
      self.maxForce = 30.0
      self.currentBlastRadius = 0.0
      self.blastRadius = 60
    if self.type == "Railgun":
      self.damageInflicted = 80
      self.mass = 0.1
      self.maxSpeed = 5000
      self.maxForce = 10000
      self.timeShotIsVisible = 10
      #self.timeShotIsVisible = 0.2

  def getClosestIntersectingBot(self, fromm, to):
    closestIntersectingBot = None
    closestSoFar = float('Inf')
    for player in self.shooter.world.players:
      if player != self.shooter:
        if self.shooter.world.distToLineSegment(fromm, to, player.position) < player.size:
          dist = func.distanceSq(player.position, self.origin)
          if dist < closestSoFar:
            dist = closestSoFar
            closestIntersectingBot = player
    return closestIntersectingBot

  def getListOfIntersectingBots(self, fromm, to):
    hits = [] # players
    for player in self.shooter.world.players:
      if player != self.shooter:
        if self.shooter.world.distToLineSegment(fromm, to, player.position) < player.size:
          hits.append(player)
    return hits

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  

  def update_rocket(self):
    if not self.impacted:
      self.velocity = self.maxSpeed * self.heading
      if self.velocity.length() > self.maxSpeed:
        self.velocity = self.velocity.normalize() * self.maxSpeed
      self.position += self.velocity
      self.testForImpact_rocket()
    else:
      self.currentBlastRadius += 2 # Rocket_ExplosionDecayRate = 2.0   --how fast the explosion occurs (in secs)
      if self.currentBlastRadius > self.blastRadius:
        self.dead = True

  def update_rail(self):
    if not self.impacted:
      desiredVelocity = (self.target - self.position).normalize() * self.maxSpeed
      sf = desiredVelocity - self.velocity
      accel = sf / self.mass
      self.velocity += accel
      if self.velocity.length() > self.maxSpeed:
        self.velocity = self.velocity.normalize() * self.maxSpeed
      self.position += self.velocity
      self.testForImpact_rail()
    elif not self.isVisibleToPlayer():
      self.dead = True

  def render_rocket(self, screen):
    pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), 2, 0)
    if self.impacted:
      pygame.draw.circle(screen, (120, 120, 120), (int(self.position.x), int(self.position.y)), int(self.currentBlastRadius) + 2, 2)

  def render_rail(self, screen):
    if self.isVisibleToPlayer() and self.impacted:
      pygame.draw.line(screen, (255, 255, 255), (int(self.origin.x), int(self.origin.y)), (int(self.impactPoint.x), int(self.impactPoint.y)), 3)

    #ROCKET

  def inflictDamageOnBotsWithinBlastRadius(self):
    for player in self.shooter.world.players:
      if player.isAlive:
        if func.distance(self.position, player.position) < self.blastRadius + player.size: 
          player.hit = True
          player.attacker = self.shooter
          player.health -= self.splashDamage

  def testForImpact_rocket(self):
    hit = self.getClosestIntersectingBot(self.position - self.velocity, self.position)
    if hit and hit.isAlive:
      self.impacted = True
      hit.hit = True
      hit.attacker = self.shooter
      hit.health -= self.damageInflicted
      self.inflictDamageOnBotsWithinBlastRadius()
    #test for impact with a wall
    self.impactPoint = self.shooter.world.findClosestPointOfIntersectionWithWalls(self.position - self.velocity, self.position)
    if self.impactPoint:
      self.impacted = True
      self.inflictDamageOnBotsWithinBlastRadius()
      self.position = self.impactPoint
      return
    tolerance = 5.0
    if func.distanceSq(self.position, self.target) < (tolerance * tolerance):
      self.impacted = True
      self.inflictDamageOnBotsWithinBlastRadius()

    #RAIL

  def testForImpact_rail(self):
    self.impacted = True
    self.impactPoint = self.shooter.world.findClosestPointOfIntersectionWithWalls(self.position - self.velocity, self.position)
    hits = self.getListOfIntersectingBots(self.origin, self.position)
    if not hits:
      return
    for hit in hits:
      if hit.isAlive:
        hit.hit = True
        hit.attacker = self.shooter
        hit.health -= self.damageInflicted

  def isVisibleToPlayer(self):
    return pygame.time.get_ticks() < self.timeOfCreation + self.timeShotIsVisible
              