#!/usr/bin/python

import pygame
from pygame.locals import *
import sys, os

from engine import player
from engine import maps
from engine import sprite
from engine import pathfinding

pygame.init()

icon = pygame.image.load("icon.png")
pygame.display.set_caption("pyrealms")
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((800, 600))#, pygame.FULLSCREEN)

clock = pygame.time.Clock()

currentMap = maps.Map(screen, "0")

Player = player.Player(currentMap, screen)
Player.pathfinder = pathfinding.Pathfinder(currentMap, Player, screen)

Player.sprites['playerBody'] = sprite.Sprite("resources/gfx/sprites/BODY_male.png", 64, 64)
Player.sprites['playerFeet'] = sprite.Sprite("resources/gfx/sprites/FEET_shoes_brown.png", 64, 64)
Player.sprites['playerLegs'] = sprite.Sprite("resources/gfx/sprites/LEGS_robe_skirt.png", 64, 64)
Player.sprites['playerHead'] = sprite.Sprite("resources/gfx/sprites/HEAD_robe_hood.png", 64, 64)
Player.sprites['playerChest'] = sprite.Sprite("resources/gfx/sprites/TORSO_robe_shirt_brown.png", 64, 64)

Player.setPlayerName("Player1")

#start background music
pygame.mixer.music.load("resources/music/tjungle.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.7)

running = True

while running:
        clock.tick(60)

        screen.fill((255,255,255))

        key = pygame.key.get_pressed()
        
        currentMap.DrawGround()
        #Player.drawPlayer(screen, 0)

        if not Player.pathfinder.checkPathEnd():
                Player.pathfinder.pathMoveStep(screen)

        #end game
        if key[K_ESCAPE]:
                sys.exit()
                break

        if Player.pathfinder.checkPathEnd():
                Player.drawPlayer(screen, 0)

        #set the player speed
        if key[K_LSHIFT]:
                Player.setSpeed(7)
        else:
                Player.setSpeed(5)

        #record mouse down position and start pathfinding
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = event.pos

                        #calculate path finder path points
                        Player.pathfinder.resetPathFinder()
                        Player.pathfinder.calculatePath(screen, mx, my)


        pygame.display.flip()

        for event in pygame.event.get():
                if event.type == QUIT:
                        running = False
                        sys.exit()
                        break
