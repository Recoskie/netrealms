import pygame

class Sprite:

	def __init__(self, spritesheet, tilewidth, tileheight):
		self.tileData = {
			'tiles': [],
			'tilewidth': 0,
			'tileheight': 0
		}

		self.load(spritesheet, tilewidth, tileheight)

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

	    self.tileData['tiles'], self.tileData['tileheight'], self.tileData['tilewidth'] = sprites, tileheight, tilewidth