import pygame
import Entity as ent
import Obstacle as obs
import SteeringBehavior as sb
import math
import Functions as func
import Gun as gun
import Game as game

pygame.init()
clock = pygame.time.Clock() #tworzy zegar,ktory kontroluje ilosc klatek na sekunde.

no_obstacles = 4
no_predators = 20

display_width = 800 #1280
display_height = 600 #720

frames_per_second = 30 #ilosc klatek na sekunde
dt = 1. / frames_per_second

bg = pygame.image.load('bg.png')

screen = pygame.display.set_mode((display_width, display_height))

new_game = game.Game(no_obstacles, no_predators, (display_width, display_height))

#glowna petla gry
while new_game.play_game:
	#obsluga przyciskow    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            new_game.play_game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
            	new_game.Victim.moveLeft()
            elif event.key == pygame.K_f:
            	new_game.Victim.moveRight()
            if event.key == pygame.K_e:
            	new_game.Victim.moveUp()
            elif event.key == pygame.K_d:
            	new_game.Victim.moveDown()
            if event.key == pygame.K_SPACE:
                new_game.RailGun = gun.Gun(new_game.Victim, new_game.Obstacles, new_game.Predators)
        if event.type == pygame.KEYUP:
        	if event.key == pygame.K_s or event.key == pygame.K_f:
        		new_game.Victim.stop(False)
        	if event.key == pygame.K_e or event.key == pygame.K_d:
        		new_game.Victim.stop(True)
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_game.RailGun = gun.Gun(new_game.Victim, new_game.Obstacles, new_game.Predators)

    if new_game.Victim.health < 0 or len(new_game.Predators) == 0:
        if new_game.Victim.health < 0:
            func.displayMessage("You're dead! Play again? Y/N?", (display_width, display_height), screen, fontSize=50, update=True)
        elif len(new_game.Predators) == 0:
            func.displayMessage("You killed all the zombies, congrats! Play again? Y/N?", (display_width, display_height), screen, fontSize=50, update=True)
        while True:                         #zamraza scene do czasu nacisniecia przycisku
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        new_game = game.Game(no_obstacles, no_predators, (display_width, display_height))
                    if event.key == pygame.K_n: 
                        new_game.play_game = False
                    break
                if event.type == pygame.QUIT:
                    new_game.play_game = False
                    break
            else: continue #executed if 'for' loop ended without 'break'
            break
    
    #rysowanie tla
    pygame.display.flip()							#czarne tlo
    screen.blit(bg, (0,0))

    #obliczanie pozycji gracza
    new_game.Victim.updatePosition(dt, (display_width, display_height))
    for predator in new_game.Predators:
    	predator.updatePosition(dt, (display_width, display_height), new_game.Victim)

    #rysowanie postaci
    new_game.Victim.drawEntity(screen)
    for obstacle in new_game.Obstacles:
    	obstacle.drawObstacle(screen)
    for predator in new_game.Predators:
    	predator.drawEntity(screen)
    if new_game.RailGun:
        new_game.RailGun.drawRay(screen)
    new_game.Victim.drawHealthbar(screen)

    new_game.RailGun = None

    clock.tick(frames_per_second) #ilosc klatek na sekunde, czyli ile razy zegar ma tyknac w tym czasie.

pygame.quit() 
quit() 													#wychodzimy z Pythona.