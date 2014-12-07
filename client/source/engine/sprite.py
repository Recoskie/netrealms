import pygame

class Sprite:

	def __init__(self, spritesheet, tilewidth, tileheight):
		self.tiles, self.tileheight, self.tilewidth = self.load(spritesheet, tilewidth, tileheight)

	tileheight = 0
	tilewidth = 0
	tiles = []

	def load(self, spritesheet, tilewidth, tileheight):
	    spritesheet = pygame.image.load(spritesheet).convert_alpha()
	    sheetwidth, sheetheight = spritesheet.get_size()

	    sprites = []
	    
	    for tile_x in range(0, sheetwidth / tilewidth):
	        line = []
	        sprites.append(line)
	        for tile_y in range(0, sheetheight/tileheight):
	            rect = (tile_x * tilewidth, tile_y * tileheight, tilewidth, tileheight)
	            line.append(spritesheet.subsurface(rect))

	    return sprites, tileheight, tilewidth