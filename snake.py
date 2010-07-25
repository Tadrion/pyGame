import pygame,sys,os,random
from pygame.locals import *

pygame.init()

screenWidth = 800
screenHeight = 600
black = (0,0,0)
red = (255,0,0)
white = (255,255,255)

def moveRect ( rect,velocityx,velocityy ):
    return rect[0]+velocityx,rect[1]+velocityy,rect[2],rect[3]

def rectCollide (rect1, rect2):
    if rect1 == rect2:
        return True
    else:
        return False

class Snake:
    global controller,apples
    def __init__(self):
        self.tail = []
        self.rect = (300,300,10,10)
        self.velocityx = 0
        self.velocityy = 0
        self.size = 3
        for i in range(self.size):
            self.tail.append( (0,0,0,0) );

    def update(self):
        velocityx = 10 * (controller.r - controller.l)
        velocityy = 10 * (controller.d - controller.u)
        
        self.tail[0] = self.rect 

        for i in range(self.size - 1,0,-1):
            self.tail[i] = self.tail[i-1]

        self.moveRect(velocityx,velocityy)
    
        if self.rect[0] <= 0 or self.rect[0] >= screenWidth-10 or self.rect[1] <= 0 or self.rect[1] >= screenHeight-10:
            sys.exit(0)

        for i in range(3,self.size):
            if ( (velocityx != 0 or velocityy != 0) and  rectCollide(self.rect,self.tail[i])):
                print i
                sys.exit(0)

        for i in range(len(apples)-1):
            if apples[i].rect == self.rect:
                self.size = self.size + 1
                self.tail.append( (0,0,0,0) )
                print self.size
                apples[i].life = 3000

    def moveRect(self,velocityx,velocityy):
        self.rect = moveRect(self.rect,velocityx,velocityy)

snake = Snake()
apples = range(0,0)
class Controller:
    global started
    def __init__(self):
        self.u = 0
        self.d = 0
        self.l = 0
        self.r = 0
        
    def keyPressed(self,key):
        if key == K_UP : 
            if self.d == 0:
                self.u = 1
                self.d = self.l = self.r = 0
        if key == K_DOWN :
            if self.u == 0:
                self.d = 1
                self.u = self.l = self.r = 0
        if key == K_LEFT : 
            if self.r == 0:
                self.l = 1
                self.u = self.d = self.r = 0
        if key == K_RIGHT : 
            if self.l == 0:
                self.r = 1 
                self.u = self.d = self.l = 0

controller = Controller()

window = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('Snake')
screen = pygame.display.get_surface()

class Apple:
    def __init__(self,x,y):
        self.rect = (x,y,10,10)
        self.life = 0

    def update(self):
        self.life = self.life + 1
    
def input(events):
    global controller,snake
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            controller.keyPressed( event.key )    

def updateimage():
    screen.fill(black)
    snake.update()
    pygame.draw.rect(screen, white, snake.rect, 0)
    for i in range(snake.size):
        pygame.draw.rect(screen, white, snake.tail[i], 0)
    myval = random.randint(1,5)
    if myval == 3:
        varr = True
        newapple = Apple( 10* (random.randint(10,70)), 10*(random.randint(10,50)) )
        
        if newapple.rect == snake.rect:
            varr = False
     
        if len(apples) > 1:
            varr = False
       
        for j in range(snake.size):
            if newapple.rect == snake.tail[j]:
                varr = False
                
        if varr:
            apples.append(newapple)

    for i in range( len(apples) - 1):
        apples[i].update()
        pygame.draw.rect(screen,red, apples[i].rect, 0)
        if apples[i].life >= 90:
            apples.pop(i)

    pygame.display.update()
    pygame.time.delay(100)
    
while True:
    input(pygame.event.get())
    updateimage()
