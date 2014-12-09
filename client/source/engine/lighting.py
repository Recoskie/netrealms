import pygame
import math
import numpy

class LightMap:

    def __init__(self, screen, alpha):
        self.screen = screen
        self.alpha = alpha
        self.lights = []
        self.tiles = []
        self.surface = pygame.Surface((1024, 768), pygame.SRCALPHA)
        self.create()

    def create(self):   
        columns = []
        for row in range(64):
            for column in range(48):           #These dimensions mean that the screen is broken up into a grid of ten by ten smaller tiles for lighting.
                tile = pygame.Surface((16, 16))
                tile.fill(pygame.Color(0, 0, 0))
                tile.set_alpha(self.alpha)
                tile.convert_alpha()
                columns.append(tile)
            self.tiles.append(columns)#this now gives you a matrix of surfaces to set alphas to

    def draw(self):
        for row in range(64):
            for column in range(48):
                self.screen.blit(self.tiles[row][column], (row * 16, column * 16))

    def set_all(alpha):
        for column in tiles:
            for tile in column:
                tile.set_alpha(alpha)

    def set_tile(x,y,alpha):        #the x and y args refer to the location on the matrix, not on the screen. So the tile one to the right and one down from the topleft corner, with the topleft coordinates of (64,64), would be sent as 1, 1
        Xindex = 0
        Yindex = 0
        for column in tiles:
            for tile in column:
                if Xindex == x and Yindex == y:
                    tile.set_alpha(alpha)            #when we find the correct tile in the coordinates, we set its alpha and end the function
                    return
                x += 1  


    def drawLight(self, px, py, lightSize):

    px = px << 1
    py = py << 1

    x1 = px
    x2 = px + 1
    y2 = py + 24

    if (y2>(TileMap.tileMapH< <1)) y2=(TileMap.tileMapH<<1);

    int shadeY;
    int light;

    int baseLight=256/(lightSize<<3);
    int lightX;

    int count=0;

    while (count<24) {
    lightX=count*count;

    if (x1>=0 && x1

    y1=py-24;
    if (y1<0) y1=0;

    while (y1<=y2) {
    if (y1>=0 && y1 if (y1 else shadeY=y1-py;

    light=256- ((baseLight)*( (lightX)+ (shadeY*shadeY) ));
    if (light>255) light=255;

    if (light>myWorld.fogMap[x1+(y1*(TileMap.tileMapW< <1))]) {
    if (myWorld.isEdge(x1>>1, y1>>1) || myWorld.getTileRenderMap(x1>>1,y1>>1)>=48) {
    myWorld.fogMap[x1+(y1*(TileMap.tileMapW< <1))]=light;
    }
    }

    }
    y1++;
    }
    }
    x1--;

    if (x2>=0 && x2

    y1=py-24;
    if (y1<0) y1=0;

    while (y1<=y2) {
    if (y1>=0 && y1 if (y1 else shadeY=y1-py;

    light=256- ((baseLight)*( (lightX)+ (shadeY*shadeY) ));
    if (light>255) light=255;

    if (light>myWorld.fogMap[x2+(y1*(TileMap.tileMapW< <1))]) {
    if (myWorld.isEdge(x2>>1, y1>>1) || myWorld.getTileRenderMap(x2>>1,y1>>1)>=48) {
    myWorld.fogMap[x2+(y1*(TileMap.tileMapW<<1))]=light;
    }
    }

    }
    y1++;
    }
    }
    x2++;

    count++;
    }
    }