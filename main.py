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
        self.car_width = 53
        self.total_thing=5
        self.gameExit = False
        self.thing_list=[]

    def init2(self):
        self.x = (self.display_width * 0.45)
        self.y = (self.display_height * 0.8)
        self.x_change = 0
        self.thing_startx = random.randrange(200, self.display_width-self.car_width-500)
        self.thing_starty = random.randint(-200,-10)
        self.thing_speed = 0.5
        self.thing_width = 30
        self.thing_height = 30
        self.bullets_count=100
        self.dodged = 0
        self.bullet_list=[]
        
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
        for i in self.thing_list:
            i[1] += self.thing_speed
            self.thing(i[0],i[1],i[2],i[3],i[4])
    
    def thing_cross(self):
        for i in self.thing_list:
            if i[1] > self.display_height:
                i[1] = random.randint(-200,-10)
                i[0] = random.randrange(0,self.display_width)
                self.dodged += 1
                self.thing_speed += 0.1
                #i[2] += (self.dodged * 0.12)
            
    def thing_hit(self):
        for i in self.thing_list:
            if self.y <= i[1] + i[3]:
                if (i[0] >= self.x and i[0] <= (self.x + self.car_width)) or ((i[0] + i[2]) >= self.x and (i[0] + i[2]) <= (self.x + self.car_width)):
                    self.crash()
        
    def bullet(self,tup):
        pygame.draw.rect(self.gameDisplay, self.black, [tup[0], tup[1], 3, 3])
    
    def bullet_creation(self):
        for i in range(len(self.bullet_list)):           
            self.bullet_list[i][1]-=1
            self.bullet(self.bullet_list[i])
            
    def bullet_deletion(self):
        temp=[]
        for i in range(len(self.bullet_list)):
            if self.bullet_list[i][1]>-100:
                temp.append(self.bullet_list[i])
        self.bullet_list=temp

    def bullet_hit(self,li):
        temp2=[]
        for i in range(len(self.bullet_list)):
            if self.bullet_list[i][1] <= li[1] + li[3]:
                if self.bullet_list[i][0] >= li[0] and self.bullet_list[i][0] <= li[0] + li[2]:  
                    li[1] = 0 - li[3]
                    li[0] = random.randrange(0,self.display_width)
                    self.dodged += 1
                    self.thing_speed += 0.1
                    li[2] += (self.dodged * 0.12)
                else:
                    temp2.append(self.bullet_list[i])
            else:
                temp2.append(self.bullet_list[i])
        self.bullet_list=temp2
        
    def bullets_remaining(self):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Bullets: "+str(self.bullets_count), True, self.black)
        self.gameDisplay.blit(text,(700,0))
            
    def car(self,x,y):
        self.gameDisplay.blit(self.carImg,(x,y))
        
    def car_boundary_cross(self):
        if (self.x + self.car_width + 15) >= self.display_width or self.x < 0:
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
        self.thing_list=[]
        self.game_loop()
    
    def crash(self):
        self.message_display('You Crashed at ' + str(self.dodged))
    
    def game_loop(self):
        
        for i in range(self.total_thing):
            self.init2()
            self.thing_list.append([self.thing_startx,self.thing_starty,self.thing_width,self.thing_height,self.block_color])
            
        print(len(self.thing_list))
        
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit=True
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x_change = -3
                    if event.key == pygame.K_RIGHT:
                        self.x_change = 3
                    if event.key == pygame.K_1 and self.bullets_count>0:
                        self.bullet_list.append([self.x+33,self.y])
                        self.bullets_count-=1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.x_change = 0
            
            if self.gameExit==True:
                break
            
            self.x += self.x_change
            self.gameDisplay.fill(self.white)
            
            self.thing_creation()#
            
            self.bullet_creation()#
                
            self.bullet_deletion()#
            
            self.car(self.x,self.y)#
            
            self.things_dodged()#
            
            self.bullets_remaining()#
            
            self.car_boundary_cross()#

            self.thing_cross()#
                
            for i in self.thing_list:
                self.bullet_hit(i)#

            self.thing_hit()#
            
            if self.gameExit==False:
                pygame.display.update()
                
            self.clock.tick(100)

obj=game()
obj.canvas()
obj.game_loop()
