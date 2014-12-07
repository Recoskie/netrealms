#!/usr/bin/python
import pygame
import ConfigParser
from player import Player

def LoadMap(filename):

    #Map Variables
    tileset = []
    layer1 = {}
    layer2 = {}
    fringe1 = {}
    
    #Parse the map file into lists and strings

    parser = ConfigParser.ConfigParser()

    parser.read(filename)
    
    filepath = parser.get("level", "tileset")
    
    tilewidth = int(parser.get("level", "tilewidth"))

    tileheight = int(parser.get("level", "tileheight"))

    layer1 = parser.get("layer1", "map").split("\n")
    
    layer2 = parser.get("layer2", "map").split("\n")
    
    fringe1 = parser.get("fringe1", "map").split("\n")
    
    blockedtiles = parser.get("level", "blockedtiles").split(",")

    #print(str(blockedtiles))
    
    #Load the tiles

    tileset=LoadSpriteSheet(filepath,tilewidth,tileheight)
            
    return tileset, layer1, layer2, fringe1, blockedtiles, tilewidth, tileheight

def LoadSpriteSheet(spritesheet, tilewidth, tileheight):
    spritesheet = pygame.image.load(spritesheet).convert_alpha()
    sheetwidth, sheetheight = spritesheet.get_size()

    sprites = []
    
    for tile_x in range(0, sheetwidth/tilewidth):
        line = []
        sprites.append(line)
        for tile_y in range(0, sheetheight/tileheight):
            rect = (tile_x*tilewidth, tile_y*tileheight, tilewidth, tileheight)
            line.append(spritesheet.subsurface(rect))

    return sprites


def getTileCoord(tileX, tileY):
    return tileX * 32, tileY * 32

#*******************check if player is Colliding into an block tile********************

def isColliding(posX, posY, blockedTiles):

            for i in range(0,len(blockedTiles)-2,2):
                tileX, tileY = int(blockedTiles[i]) * 32, int (blockedTiles[i+1]) * 32
                if (posX + 18 <= tileX + 32 and posX + 48 >= tileX or posX + 48 >= tileX and posX + 18 <= tileX + 32):
                    if(posY + 48 <= tileY + 32 and posY + 64 >= tileY):
                        return True
            return False

#path finder helper function test tile position directly for if there is an block tile

def isBlockTiles(TilePosX, TilePosY, blockedTiles):
    for i in range(0,len(blockedTiles)-2,2):
        tileX, tileY= int(blockedTiles[i])*32, int (blockedTiles[i+1])*32
        if(TilePosX==tileX and TilePosY==tileY):
            return(True)
    return(False)

#*****************************draw an layer of tiles***********************************
	
def DrawLayer(screen, layer, tileset, tilewidth, tileheight):
        for map_y, line in enumerate(layer):
                        tilenums = line.split(",")
                        map_x = 0
                        for i in tilenums:
                                tilex = int(i[0])
                                tiley = int(i[1])
                                screen.blit(tileset[tilex][tiley], (map_x*tilewidth, map_y*tileheight))
                                map_x = map_x + 1
                                if map_y == 32:
                                        map_x = 0
