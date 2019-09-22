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
        self.bullets_count=100
        self.gameExit = False

    def init2(self):
        self.x = (self.display_width * 0.45)
        self.y = (self.display_height * 0.8)
        self.x_change = 0
        self.thing_startx = random.randrange(70, self.display_width-self.car_width-70)
        self.thing_starty = -100
        self.thing_speed = 0.5
        self.thing_width = 30
        self.thing_height = 30
        self.dodged = 0
        self.li=[]
        
    def canvas(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('Space Impact_In_Progress')
        self.clock = pygame.time.Clock()
        self.carImg = pygame.image.load('images/car.png')

    def things_dodged(self):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Dodged: "+str(self.dodged), True, self.black)
        self.gameDisplay.blit(text,(0,0))

    def thing(self,thingx, thingy, thingw, thingh, color):
        pygame.draw.rect(self.gameDisplay, color, [thingx, thingy, thingw, thingh])
        
    def thing_creation(self):
        self.thing(self.thing_startx, self.thing_starty, self.thing_width, self.thing_height, self.block_color)
    
    def thing_cross(self):
        if self.thing_starty > self.display_height:
            self.thing_starty = 0 - self.thing_height
            self.thing_startx = random.randrange(0,self.display_width)
            self.dodged += 1
            self.thing_speed += 0.1
            self.thing_width += (self.dodged * 0.12)
            
    def thing_hit(self):
        if self.y < self.thing_starty+self.thing_height:
            if self.x > self.thing_startx and self.x < self.thing_startx + self.thing_width or self.x+self.car_width > self.thing_startx and self.x + self.car_width < self.thing_startx+self.thing_width:
                self.crash()
        
    def bullet(self,tup):
        pygame.draw.rect(self.gameDisplay, self.black, [tup[0], tup[1], 3, 3])
    
    def bullet_creation(self):
        for i in range(len(self.li)):           
            self.li[i][1]-=1
            self.bullet(self.li[i])
            
    def bullet_deletion(self):
        temp=[]
        for i in range(len(self.li)):
            if self.li[i][1]>-100:
                temp.append(self.li[i])
        self.li=temp

    def bullet_hit(self):
        temp2=[]
        for i in range(len(self.li)):
            if self.li[i][1] <= self.thing_starty+self.thing_height:
                if self.li[i][0] >= self.thing_startx and self.li[i][0] <=self.thing_startx + self.thing_width:  
                    self.thing_starty = 0 - self.thing_height
                    self.thing_startx = random.randrange(0,self.display_width)
                    self.dodged += 1
                    self.thing_speed += 0.1
                    self.thing_width += (self.dodged * 0.12)
                else:
                    temp2.append(self.li[i])
            else:
                temp2.append(self.li[i])
        self.li=temp2
        
    def bullets_remaining(self):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Bullets: "+str(self.bullets_count), True, self.black)
        self.gameDisplay.blit(text,(700,0))
            
    def car(self,x,y):
        self.gameDisplay.blit(self.carImg,(x,y))
        
    def car_boundary_cross(self):
        if self.x > self.display_width - self.car_width or self.x < 0:
            self.crash()

    def text_objects(self,text, font):
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()

    def message_display(self,text):
        largeText = pygame.font.Font('freesansbold.ttf',80)
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
        self.message_display('You Crashed at ' + str(self.dodged))
    
    def game_loop(self):
        self.init2()
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit=True
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x_change = -5
                    if event.key == pygame.K_RIGHT:
                        self.x_change = 5
                    if event.key == pygame.K_1 and self.bullets_count>0:
                        self.li.append([self.x+33,self.y])
                        self.bullets_count-=1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.x_change = 0
            
            if self.gameExit==True:
                break
            
            self.x += self.x_change
            self.gameDisplay.fill(self.white)
            
            self.thing_creation()
            
            self.bullet_creation()
                
            self.bullet_deletion()
            
            self.thing_starty += self.thing_speed
            
            self.car(self.x,self.y)
            
            self.things_dodged()
            
            self.bullets_remaining()
            
            self.car_boundary_cross()

            self.thing_cross()
                
            self.bullet_hit()

            self.thing_hit()
            
            if self.gameExit==False:
                pygame.display.update()
                
            self.clock.tick(100)

obj=game()
obj.canvas()
obj.game_loop()
