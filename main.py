import pygame
import time
import random
from nnlib import nn
import numpy as np
import copy
class car:
    def __init__(self,width,height,carImg,brain=None):
        self.x=width*0.45
        self.y=height*0.8
        self.fitness=0
        self.carImg=carImg
        if(brain==None):
            self.brain=nn([4,4,4,3],['leaky_relu','leaky_relu','leaky_relu','softmax'],4)
        else:
            self.brain=brain
    def predict(self,input):
        input=np.array(input).reshape(4,1)
        out=self.brain.predict(input)
        return np.argmax(out)
    def re_init(self,width,height):
        self.x=width*0.5
        self.y=height*0.8
        self.fitness=0
class game:  
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.block_color = (53,115,255)
        self.car_width = 73
        self.gameExit = False
        self.gen=[]
        self.size=10
        self.gen_stack=[]
    
    def canvas(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('Space Impact')
        self.clock = pygame.time.Clock()
        self.carImg = pygame.image.load('images/car.png')
        for i in range(self.size): self.gen.append(car(self.display_width,self.display_height,self.carImg))

    def things_dodged(self,count):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Dodged: "+str(count), True, self.black)
        self.gameDisplay.blit(text,(0,0))

    def things(self,thingx, thingy, thingw, thingh, color):
        pygame.draw.rect(self.gameDisplay, color, [thingx, thingy, thingw, thingh])

    def text_objects(self,text, font):
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()
    def displayCar(self,car):
        self.gameDisplay.blit(car.carImg,(car.x,car.y))
    def message_display(self,text):
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((self.display_width/2),(self.display_height/2))
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        time.sleep(0.5)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit=True
                    pygame.quit()
        self.game_loop()
    
    def crash(self):
        self.message_display('You Crashed')
    def generate(self):
        for car in self.gen_stack:
            car.re_init(self.display_width,self.display_height)
            self.gen.append(car)
        self.size=len(self.gen)
        self.gen_stack=[]
        print(self.size)

    def game_loop(self):
        x = (self.display_width * 0.45)
        y = (self.display_height * 0.8)
        x_change = 0
        thing_startx = random.randrange(0, self.display_width)
        thing_starty = -600
        thing_speed = 4
        thing_width = 100
        thing_height = 100
        dodged = 0
        flag=0
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit=True
                    pygame.quit()
            if self.gameExit==True:
                break
            self.gameDisplay.fill(self.white)
            self.things(thing_startx, thing_starty, thing_width, thing_height, self.block_color)
            thing_starty += thing_speed
            i=0
            while i<len(self.gen) and i>=0:
                Car=self.gen[i];
                if(self.size<=1):
                    self.generate()
                    dodged=0
                    thing_speed=4
                    thing_width=100
                    thing_height=100
                    break
                output=Car.predict([random.randint(1,100),random.randint(1,100),random.randint(1,100),random.randint(1,100)])
                if(output==1): x_change=-5
                if(output==2): x_change=5
                Car.x += x_change
                self.things_dodged(dodged)
                if Car.x > self.display_width - self.car_width or Car.x < 0:
                    self.size-=1
                    self.gen_stack.append(self.gen.pop(i))
                    i-=1
                    continue

                if Car.y < thing_starty+thing_height:
                    if Car.x > thing_startx and Car.x < thing_startx + thing_width or Car.x+self.car_width > thing_startx and Car.x + self.car_width < thing_startx+thing_width:
                        self.size-=1
                        self.gen_stack.append(self.gen.pop(i))
                        i-=1
                        continue
                if thing_starty > self.display_height:
                    thing_starty = 0 - thing_height
                    thing_startx = random.randrange(0,self.display_width)
                    dodged += 1
                    Car.fitness+=1
                    thing_speed += 1
                    thing_width += (dodged * 1.2)
                self.displayCar(Car)
                i+=1
            if self.gameExit==False:
                pygame.display.update()
            self.clock.tick(100)

obj=game()
obj.canvas()
obj.game_loop()