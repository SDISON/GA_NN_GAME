import pygame
import time
import random
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
    
    def canvas(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('Space Impact')
        self.clock = pygame.time.Clock()
        self.carImg = pygame.image.load('images/car.png')

    def things_dodged(self,count):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Dodged: "+str(count), True, self.black)
        self.gameDisplay.blit(text,(0,0))

    def things(self,thingx, thingy, thingw, thingh, color):
        pygame.draw.rect(self.gameDisplay, color, [thingx, thingy, thingw, thingh])

    def car(self,x,y):
        self.gameDisplay.blit(self.carImg,(x,y))

    def text_objects(self,text, font):
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()

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
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit=True
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -5
                    if event.key == pygame.K_RIGHT:
                        x_change = 5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_change = 0
            if self.gameExit==True:
                break
            x += x_change
            self.gameDisplay.fill(self.white)
            self.things(thing_startx, thing_starty, thing_width, thing_height, self.block_color)
            thing_starty += thing_speed
            self.car(x,y)
            self.things_dodged(dodged)
            if x > self.display_width - self.car_width or x < 0:
                self.crash()

            if thing_starty > self.display_height:
                thing_starty = 0 - thing_height
                thing_startx = random.randrange(0,self.display_width)
                dodged += 1
                thing_speed += 1
                thing_width += (dodged * 1.2)

            if y < thing_starty+thing_height:
                if x > thing_startx and x < thing_startx + thing_width or x+self.car_width > thing_startx and x + self.car_width < thing_startx+thing_width:
                    self.crash()
            if self.gameExit==False:
                pygame.display.update()
            self.clock.tick(100)

obj=game()
obj.canvas()
obj.game_loop()
