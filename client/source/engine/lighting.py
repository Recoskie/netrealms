import pygame

class LightMap:

	def __init__(self, screen, alpha):
		self.screen = screen
		self.alpha = alpha
		self.lights = []

	def draw(self):
		self.image = pygame.Surface((self.screen.get_size()), pygame.SRCALPHA)
		self.image.fill((0,0,0, self.alpha))

		for light in self.lights:
			light.draw()

		self.image.unlock()
		self.screen.blit(self.image, (0, 0))
		self.image.lock()

	def addLight(self, size, source, luminosity):
		self.lights.append(LightSource(size, source, self, luminosity))

class LightSource:

	def __init__(self, size, source, lightMap, luminosity):
		self.size = size
		self.source = source
		self.lightMap = lightMap
		self.luminosity = luminosity

	def draw(self):
		size = self.size
		x, y = self.source.physics['x'] + 32, self.source.physics['y'] + 48 #position of light source

		if self.lightMap.alpha > self.luminosity:

			tempsize = size - 1

			lumino = self.luminosity

			while tempsize > 1:
				if lumino > 0:
					lumino = lumino - 1
				pygame.surfarray.pixels_alpha(self.lightMap.image)[x - tempsize / 2:x + tempsize / 2, y - tempsize / 2:y + tempsize / 2] = lumino
				tempsize = tempsize - 1
			#tempsize = fraction
			pygame.surfarray.pixels_alpha(self.lightMap.image)[x - tempsize / 2:x + tempsize / 2, y - tempsize / 2:y + tempsize / 2] = lumino


		