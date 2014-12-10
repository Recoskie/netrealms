#!/usr/bin/python

import pygame
from pygame.locals import *
import sys, os

from engine import player
from engine import maps
from engine import sprite
from engine import pathfinding
from engine import lighting

pygame.init()

icon = pygame.image.load("icon.png")
pygame.display.set_caption("netrealms")
pygame.display.set_icon(icon)

fullscreen = False

if fullscreen:
        screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.ASYNCBLIT)
else:
        screen = pygame.display.set_mode((800,600))#(1366, 768), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)

clock = pygame.time.Clock()

currentMap = maps.Map(screen, "0")

Player = player.Player(currentMap, screen)
Player2 = player.Player(currentMap, screen)

Player2.physics['x'] = 100
Player2.physics['y'] = 100
Player2.setPlayerName("NPC")

Player2.sprites['playerBody'] = sprite.Sprite("resources/gfx/sprites/BODY_male.png", 64, 64)
Player2.sprites['playerFeet'] = sprite.Sprite("resources/gfx/sprites/FEET_shoes_brown.png", 64, 64)
Player2.sprites['playerLegs'] = sprite.Sprite("resources/gfx/sprites/LEGS_robe_skirt.png", 64, 64)
Player2.sprites['playerHead'] = sprite.Sprite("resources/gfx/sprites/HEAD_robe_hood.png", 64, 64)
Player2.sprites['playerChest'] = sprite.Sprite("resources/gfx/sprites/TORSO_robe_shirt_brown.png", 64, 64)


Player.pathfinder = pathfinding.Pathfinder(currentMap, Player, screen)

Player.sprites['playerBody'] = sprite.Sprite("resources/gfx/sprites/BODY_male.png", 64, 64)
Player.sprites['playerFeet'] = sprite.Sprite("resources/gfx/sprites/FEET_shoes_brown.png", 64, 64)
Player.sprites['playerLegs'] = sprite.Sprite("resources/gfx/sprites/LEGS_robe_skirt.png", 64, 64)
Player.sprites['playerHead'] = sprite.Sprite("resources/gfx/sprites/HEAD_robe_hood.png", 64, 64)
Player.sprites['playerChest'] = sprite.Sprite("resources/gfx/sprites/TORSO_robe_shirt_brown.png", 64, 64)

Player.setPlayerName("Player1")

pygame.mixer.music.load("resources/music/tjungle.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.7)

running = True

darkness = 100

lightMap = lighting.LightMap(screen, darkness)
#lightMap = tilelighting.LightMap(screen, 200)
light2 = lightMap.addLight(6, Player2)
light = lightMap.addLight(6, Player)
lightx = lightMap.addStaticLight(6, 500, 500)
lightxp = lightMap.addStaticLight(6, 200, 200)

#the tile the mouse is over top of
MTileY=-32
MTileX=-32

while running:
        clock.tick(60)
        screen.fill((255,255,255))

        key = pygame.key.get_pressed()
        
        currentMap.DrawGround()
        #Player.drawPlayer(screen, 0)

        if not Player.pathfinder.checkPathEnd():
                Player.pathfinder.pathMoveStep(screen)

        if key[K_PAGEUP]:
                if darkness < 255:
                        darkness = darkness + 5
                        lightMap.set_alpha(darkness)

        if key[K_PAGEDOWN]:
                if darkness > 0:
                        darkness = darkness - 5
                        lightMap.set_alpha(darkness)

        #end game
        if key[K_ESCAPE]:
                if fullscreen:
                        pygame.display.toggle_fullscreen()
                sys.exit()
                break

        if Player.pathfinder.checkPathEnd():
                Player.drawPlayer(screen, 0)

        #set the player speed
        if key[K_LSHIFT]:
                Player.setSpeed(5)
        else:
                Player.setSpeed(2)

        Player2.drawPlayer(screen, 0)
        lightMap.draw()

        textFont = pygame.font.Font(None, 20)
        fps = textFont.render("%.0f" % round(clock.get_fps(),0) + " fps", True, (250, 250, 250))
        screen.blit(fps, (0,0))
        
        #show seelected tile
        
        pygame.draw.rect(screen, (255, 0, 0 ), ( MTileX ,MTileY , 32, 32 ), 1 )

        pygame.display.flip()

        for event in pygame.event.get():
                        
                #record mouse down position and start pathfinding
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = event.pos

                        #calculate path finder path points
                        
                        Player.pathfinder.resetPathFinder()
                        Player.pathfinder.calculatePath(screen, mx, my)
                        
                #show the current tile mouse is over top of

                if event.type == pygame.MOUSEMOTION:
                        mx, my = event.pos

                        MTileX = int( mx / 32 + 0.5 ) * 32
                        MTileY = int( my / 32 + 0.5 ) * 32
                
                if event.type == QUIT:
                        running = False
                        sys.exit()
                        break
