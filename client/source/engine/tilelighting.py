import pygame
import math
import numpy

class LightMap:

    def __init__(self, screen, alpha):
        self.screen = screen
        self.alpha = alpha
        self.lights = []

    def draw(self):
        if self.alpha > 0: #there is no darkness, no need to draw lights
            self.image = pygame.Surface((self.screen.get_size()), pygame.SRCALPHA)
            self.image.fill((0,0,0, self.alpha))

            for light in self.lights:
                light.draw()


                self.image.unlock()
                self.screen.blit(self.image, (0, 0))
                self.image.lock()

    def addLight(self, size, source, alpha):
        self.lights.append(LightSource(size, source, self, alpha))

class LightSource:

    def __init__(self, size, source, lightMap, alpha):
        self.size = size
        self.source = source
        self.lightMap = lightMap
        self.alpha = alpha

    def draw(self):
        size = self.size
        x, y = self.source.physics['x'], self.source.physics['y'] #position of light source

        x = x + 32
        y = y + 48

        #get the closest tile
        x = math.floor(x / 8)
        y = math.floor(y / 8)

        #get the pixel value of the closest tile
        x = x * 8
        y = y * 8

        pygame.surfarray.pixels_alpha(self.lightMap.image)[x:x+8, y:y+8] = self.alpha