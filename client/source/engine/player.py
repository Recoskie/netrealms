import pygame
import pathfinding

class Player:

    def __init__(self, screen):
        self.screen = screen

    properties = dict(
        name = str,
        inventory = list,
        equipment = list,
        sitting = bool,
        mounted = bool,
        resting = bool,
        faction = int,
        pclass = int,
        currentMap = None
    )

    network = dict(
        connected = bool,
        ping = int
    )

    animations = dict(
        animLeft = int, 
        animRight = int, 
        animUp = int, 
        animDown = int
    )
    
    sprites = dict(
        playerBody = list,
        playerFeet = list,
        playerLegs = list,
        playerChest = list,
        playerHat = list
    )

    pathfinding = dict(
        finderPoints = list,
        currentPoint = int,
        pathEnd = bool,
        isDebug = bool
    )

    stats = dict(
        level = int,
        experience = int,
        health = float,
        kills = int,
        deaths = int,
        stamina = float,
        mana = float
    )

    skills = dict(
        woodcutting = int,
        cooking = int,
        attack = int
    )

    physics = dict(
        x = int,
        y = int,
        speed = int,
        direction = int
    )

    playerName = ""
    
    left = 0 #sprite animation left
    right = 0 #sprite animation right
    up = 0 #sprite animation up
    down = 0 #sprite animation down
    direction = 0 #player direction
    
    
    playersprite = []
    playerfeet = []
    playerlegs = []
    playerchest = []
    playerhat = []
    
    PathFinderPoints = [] #path finders calculated points
    PathPoint = 0 #changes as each point is reached
    pathEnd = True #when path reached it's end
    
    level = 0
    experience = 0

    x, y, speed = 50, 50, 5
    oldpos = x, y

    blocktiles = []

    def isColliding(self, posX, posY, blockedTiles):

            for i in range(0,len(blockedTiles)-2,2):
                tileX, tileY = int(blockedTiles[i]) * 32, int (blockedTiles[i+1]) * 32
                if (posX + 18 <= tileX + 32 and posX + 48 >= tileX or posX + 48 >= tileX and posX + 18 <= tileX + 32):
                    if(posY + 48 <= tileY + 32 and posY + 64 >= tileY):
                        return True
            return False

    def setPathFinderDebug(self, YesNo ):
        pathfinding.setDebugMode(YesNo)

    #*****************reset calculate path and path count******************

    def resetPathFinder(self ):
        pathfinding.Points = []
        self.PathPoint = 0
        self.pathEnd = True

    #***********************Get The Players Position***********************

    def playerPos(self ):
        return(self.x, self.y )

    #****************set the players position if necessary*****************

    def setPlayerPos(self, x, y):
        self.x=x
        self.y=y

    #************************set the players Name**************************

    def setPlayerName(self, name ):
        self.playerName=name

    #**********************load the players sprites************************

    def loadPlayerSprites(self, ps ):
        self.playersprite=ps

    def loadPlayerFeet(self, pf ):
        self.playerfeet=pf

    def loadPlayerLegs(self, pl ):
        self.playerlegs=pl

    def loadPlayerChest(self, pc ):
        self.playerchest=pc

    def loadPlayerHat(self, ph ):
        self.playerhat=ph

    #***************wish I could remove this line some how*****************

    def setCollision(self, blocks ):
        self.blocktiles=blocks

    #************************set The Players speed*************************

    def setSpeed(self, speed):
        self.speed=speed

    #**********************move and animate the player*********************

    def playerMoveRight(self, screen):
        self.oldpos = self.x, self.y
        self.x+=self.speed
        self.direction=3
        self.drawPlayer(screen, self.right)
        self.right+=1
        if self. right==9:
           self.right=0
        pygame.time.wait(60)

    def playerMoveLeft(self, screen):
        self.oldpos = self.x, self.y
        self.x-=self.speed
        self.direction=1
        self.drawPlayer(screen, self.left)
        self.left+=1
        if self.left==9:
            self.left=0
        pygame.time.wait(60)
        
    def playerMoveUp(self, screen):
        self.oldpos = self.x, self.y
        self.y-=self.speed
        self.direction=0
        self.drawPlayer(screen, self.up)
        self.up+=1
        if self.up==9:
            self.up=0
        pygame.time.wait(60)

    def playerMoveDown(self, screen):
        self.oldpos = self.x, self.y
        self.y+=self.speed
        self.direction=2
        self.drawPlayer(screen, self.down)
        self.down+=1
        if self.down==9:
            self.down=0
        pygame.time.wait(60)

    #*****************************calculate path****************************

    def calculatePath(self,screen, x, y):
        PathPoint = 0
        self.PathFinderPoints = pathfinding.findPath(screen, self.x+32, self.y+48, x-16, y, self.blocktiles)
        self.pathEnd=False
        
    #********************move though Path finder Points********************
    
    def pathMoveStep(self, screen ):

        #draw rectangles to where each point goes on screen only if debug mode is active

        if pathfinding.isDebugOn():
            for i in self.PathFinderPoints:
                pygame.draw.rect(screen,(255,0,0), (i[0],i[1],32,32), 1)

        #*****************auto move Player to each point*******************
        
        if self.PathFinderPoints[self.PathPoint][0]-16<self.x:
            self.playerMoveLeft(screen)
        elif self.PathFinderPoints[self.PathPoint][0]-(16+self.speed)>self.x:
            self.playerMoveRight(screen)
        elif self.PathFinderPoints[self.PathPoint][1]-32<self.y:
            self.playerMoveUp(screen)
        elif self.PathFinderPoints[self.PathPoint][1]-(32+self.speed)>self.y:
            self.playerMoveDown(screen)
        else:
            self.drawPlayer(screen, 0 ) #draw when changing point to stop flicker

            #*************if no more movement and reached end**************
            
            self.PathPoint+=1
            
            #***************if all points gone though stop*****************
            
            if(self.PathPoint>len(self.PathFinderPoints)-1):
                self.PathPoint=0
                self.pathEnd=True


    def checkPathEnd(self ):
        return self.pathEnd

    def drawPlayer(self, screen, spriteX):

        
        if self.isColliding(self.x, self.y, self.blocktiles):
            if self.pathEnd:
                self.x, self.y = self.oldpos
                
        screen.blit(self.playersprite[spriteX][self.direction], (self.x, self.y))
        screen.blit(self.playerfeet[spriteX][self.direction], (self.x, self.y))
        screen.blit(self.playerlegs[spriteX][self.direction], (self.x, self.y))
        screen.blit(self.playerchest[spriteX][self.direction], (self.x, self.y))
        screen.blit(self.playerhat[spriteX][self.direction], (self.x, self.y))
        
        textFont = pygame.font.Font(None, 20)
        playername = textFont.render(self.playerName, True, (255, 255, 255))
        screen.blit(playername, (self.x,self.y))

        if pathfinding.isDebugOn():
            textFont=pygame.font.Font(None, 50)
            Render=textFont.render("Path Finder Debug Mode Is turned On", True, (255,0,0))
            screen.blit(Render, (0,0))
        
