import pygame
import math
import Game as game
import Functions as func

pygame.init()
clock = pygame.time.Clock() #tworzy zegar,ktory kontroluje ilosc klatek na sekunde.

no_players = 4

display_width = 960 #800 #1280
display_height = 720 #600 #720

frames_per_second = 30 #ilosc klatek na sekunde
dt = 1. / frames_per_second

bg = pygame.image.load('bg.png')

screen = pygame.display.set_mode((display_width, display_height))

new_game = game.Game((display_width, display_height), no_players)
new_game.addWalls()
new_game.readGraphFromTxt()
#new_game.floodFill()
#new_game.writeGraphToTxt()
#new_game.graph.printGraph()
new_game.triggerSystem.addTriggers(new_game.graph)

#new_game.createAllPairsCostsTable()

for trigger in new_game.triggerSystem.triggers:
   print trigger.graphNodeId
# for node in new_game.graph.nodes:
#    print node.extra_info
new_game.addPlayers()
for player in new_game.players:
    print "player's id: " + repr(player.id)

#glowna petla gry
while new_game.play_game:
	#obsluga przyciskow    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            new_game.play_game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            new_game.mouseClick = pygame.math.Vector2(x, y)
    
    #rysowanie tla
    pygame.display.flip()							#czarne tlo
    #screen.blit(bg, (0,0))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, display_width, display_height))
    for wall in new_game.walls:
        wall.drawWall(screen)

    new_game.graph.drawGraph(screen)

    new_game.triggerSystem.update(new_game.players)

    #print new_game.players

    #obliczanie pozycji gracza i rysowanie postaci
    for player in new_game.players:
        print "player: " + repr(player.id) + ", " + repr(player.health)
        if player.isAlive:
            player.update(dt, screen)
    for player in new_game.players: 
        print "player: " + repr(player.id) + ", " + repr(player.health)
        player.updateLife()
        if player.isAlive:
            player.drawEntity(screen)
    print "Projectiles: " + repr(new_game.projectiles)
    for projectile in new_game.projectiles:
        if not projectile.dead:
            if projectile.type == "Rocket":
                projectile.update_rocket()
                projectile.render_rocket(screen)
            elif projectile.type == "Railgun":
                projectile.update_rail()
                projectile.render_rail(screen)
        else:
            new_game.projectiles.remove(projectile)
            projectile = None

    #new_game.mouseClick = None
    new_game.triggerSystem.drawTriggers(screen, new_game)


    clock.tick(frames_per_second) #ilosc klatek na sekunde, czyli ile razy zegar ma tyknac w tym czasie.

pygame.quit() 
quit() 													#wychodzimy z Pythona.