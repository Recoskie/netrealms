#!/usr/bin/python
#Import PyGame
import pygame
from pygame.locals import *
import sys, os
from engine import engine
from engine import player

pygame.init()

icon = pygame.image.load("sword-icon.png")

pygame.display.set_caption("PyRealms - 2D Online RPG Engine")

clock = pygame.time.Clock()

pygame.display.set_icon(icon)

currentGameState = 0

screen = pygame.display.set_mode((800, 600))#, pygame.FULLSCREEN)

Player=0

#load the map

tileset, layer1, layer2, fringe1, blockedtiles, tilewidth, tileheight = engine.LoadMap("resources/maps/map1.map")

#player one and two instance

P=[player.Player(screen), player.Player(screen) ]

#load player in player one

P[0].loadPlayerSprites(engine.LoadSpriteSheet("resources/gfx/sprites/BODY_male.png", 64, 64))
P[0].loadPlayerFeet(engine.LoadSpriteSheet("resources/gfx/sprites/FEET_shoes_brown.png", 64, 64))
P[0].loadPlayerLegs(engine.LoadSpriteSheet("resources/gfx/sprites/LEGS_robe_skirt.png", 64, 64))
P[0].loadPlayerChest(engine.LoadSpriteSheet("resources/gfx/sprites/TORSO_robe_shirt_brown.png", 64, 64))
P[0].loadPlayerHat(engine.LoadSpriteSheet("resources/gfx/sprites/HEAD_robe_hood.png", 64, 64))

#load player in player two

P[1].loadPlayerSprites(engine.LoadSpriteSheet("resources/gfx/sprites/BODY_skeleton.png", 64, 64))
P[1].loadPlayerFeet(engine.LoadSpriteSheet("resources/gfx/sprites/FEET_plate_armor_shoes.png", 64, 64))
P[1].loadPlayerLegs(engine.LoadSpriteSheet("resources/gfx/sprites/LEGS_pants_greenish.png", 64, 64))
P[1].loadPlayerChest(engine.LoadSpriteSheet("resources/gfx/sprites/TORSO_leather_armor_shoulders.png", 64, 64))
P[1].loadPlayerHat(engine.LoadSpriteSheet("resources/gfx/sprites/HEAD_chain_armor_hood.png", 64, 64))

#set the player Collision engine

P[0].setCollision(blockedtiles)
P[1].setCollision(blockedtiles)

#set Player two away from the other player

P[1].setPlayerPos(100, 100 )

#set player one and two name

P[0].setPlayerName("Player1")
P[1].setPlayerName("Player2")

#start background music

pygame.mixer.music.load("resources/music/sketchy2.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.7)

mx=0
my=0

#I plan to eventually have the engine have an Render function for the other loaded in Players

running = True

while running:
        clock.tick(60)

        screen.fill((255,255,255))

        engine.DrawLayer(screen, layer1, tileset, tilewidth, tileheight)
        #engine.DrawLayer(screen, layer2, tileset, tilewidth, tileheight)

        key = pygame.key.get_pressed()

        #hit the key X to enable path finder debug mode

        if key[K_x]:
                P[Player].setPathFinderDebug(True)

        #hit the key C to disable path finder debug mode

        elif key[K_c]:
                P[Player].setPathFinderDebug(False)

        #for testing only switch player with Z key
        
        if key[K_z]:
                P[Player].resetPathFinder()
                Player+=1
                if Player==2:
                        Player=0

        #perfect path finding
        
        if not P[Player].checkPathEnd():
                P[Player].pathMoveStep(screen)

        #end game
        
        if key[K_ESCAPE]:
                pygame.display.toggle_fullscreen()
                P[Player].resetPathFinder()
                running = False
                pygame.quit()
                quit()
                break
        
        #move player
        
        if key[K_LEFT] or key[K_a]:
                P[Player].resetPathFinder()
                P[Player].playerMoveLeft(screen)
                
        elif key[K_RIGHT] or key[K_d]:
                P[Player].resetPathFinder()
                P[Player].playerMoveRight(screen)
                
        elif key[K_UP] or key[K_w]:
                P[Player].resetPathFinder()
                P[Player].playerMoveUp(screen)

        elif key[K_DOWN] or key[K_s]:
                P[Player].resetPathFinder()
                P[Player].playerMoveDown(screen)

        elif P[Player].checkPathEnd():
                P[Player].drawPlayer(screen, 0 )

        #set the player speed

        if key[K_LSHIFT]:
                P[Player].setSpeed(7)
        else:
                P[Player].setSpeed(5)

        #record mouse down position and start pathfinding
                                        
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = event.pos

                        #calculate path finder path points
                        P[Player].resetPathFinder()
                        P[Player].calculatePath(screen, mx, my )

        #draw other players except for the player you are controlling as it draws in the else statement for elif not gotob:

        for i in range(0,len(P)):
                if not i==Player:
                        P[i].drawPlayer(screen, 0 )
		
        #engine.DrawLayer(screen, fringe1, tileset, tilewidth, tileheight)
        
        pygame.display.flip()

        for event in pygame.event.get():
                if event.type == QUIT:
                        running = False
                        pygame.quit()
                        quit()
                        break
