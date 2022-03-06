import pygame as py
import sys
import os

py.init()

screenwidth = 1280
screenheight = 700

playerwidth = 80

screen = py.display.set_mode((screenwidth, 700))
slash_sound = py.mixer.Sound("slash.wav")

py.display.set_caption("Object")

class player(object):
    walkL = [py.image.load("L1.png").convert_alpha(), py.image.load("L2.png").convert_alpha(), py.image.load("L3.png").convert_alpha(), py.image.load("L4.png").convert_alpha(), py.image.load("L5.png").convert_alpha(), py.image.load("L6.png").convert_alpha(), py.image.load("L7.png").convert_alpha(), py.image.load("L8.png").convert_alpha(), py.image.load("L9.png").convert_alpha()]
    walkR = [py.image.load("R1.png").convert_alpha(), py.image.load("R2.png").convert_alpha(), py.image.load("R3.png").convert_alpha(), py.image.load("R4.png").convert_alpha(), py.image.load("R5.png").convert_alpha(), py.image.load("R6.png").convert_alpha(), py.image.load("R7.png").convert_alpha(), py.image.load("R8.png").convert_alpha(), py.image.load("R9.png").convert_alpha()]
    not_moving = py.image.load("stationary.png").convert_alpha()

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel = 5
        self.v = 10
        self.m = 1
        self.jumping = False
        self.left = False
        self.right = False
        self.framecount = 0
        self.stationary = True
        self.hitbox = (self.x+20, self.y+5, self.w-40, self.h-18)
        self.got_hit = False
        
        
    def move(self):
        global screenwidth
        
        if py.key.get_pressed()[py.K_d] and self.x < screenwidth-(self.w):
            self.x += self.vel
            self.right = True
            self.left = False
            self.stationary = False
            
        elif py.key.get_pressed()[py.K_a] and self.x > 0:
            self.x -= self.vel
            self.left = True
            self.right = False
            self.stationary = False
            
        else:
            self.stationary = True
            self.framecount = 0
        
        if py.key.get_pressed()[py.K_SPACE]:
            self.jumping = True
            self.framecount = 0
            
        if self.jumping:
            KE = (1/2)*self.m*(self.v**2)
            self.y -= KE
            self.v -= 1
            
            if self.v == 0 or self.v < 0:
                self.m = -1  
                
        if self.v == -11:
            self.jumping = False 
            self.v = 10
            self.m = 1
        
        
    def draw(self, screen):
        global running
        
        self.hitbox = (self.x+20, self.y+5, self.w-40, self.h-18)
        
        if self.framecount + 1 >= 27:
            self.framecount = 0
        
        if self.stationary:
            if not self.left and not self.right:
                screen.blit(self.not_moving, (self.x, self.y))
            
        
        if not self.stationary:
            if self.left:
                screen.blit(self.walkL[self.framecount//3], (self.x, self.y))
                self.framecount += 1
        
            elif self.right:
                screen.blit(self.walkR[self.framecount//3], (self.x, self.y))
                self.framecount += 1
        
        else :
            if self.left:
                screen.blit(self.walkL[0], (self.x, self.y))
                
            elif self.right:
                screen.blit(self.walkR[0], (self.x, self.y))
                
        #py.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        
        
        if self.got_hit:
            s.count = 0
            self.got_hit = False
            

class slash(object):
    slashL = [py.image.load("slash1L.png").convert_alpha(), py.image.load("slash2L.png").convert_alpha(), py.image.load("slash3L.png").convert_alpha(), py.image.load("slash4L.png").convert_alpha()]
    slashR = [py.image.load("slash1R.png").convert_alpha(), py.image.load("slash2R.png").convert_alpha(), py.image.load("slash3R.png").convert_alpha(), py.image.load("slash4R.png").convert_alpha()]
    sword = []
    hit = False
    count = 0
    
    def __init__(self, x, y, w, h, time):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
       
        self.slashing = False
        self.get_time = 0
        self.direction = 0        
        self.framecount = 0
        self.hitbox = (p.x+20+(40*self.direction), p.y, p.w-40, p.h)
        
    def move(self):
        self.x = p.x
        self.y = p.y - 20 
                
    def draw(self, screen):
        self.move()
        
        if self.framecount + 1 >= 12:
            self.framecount = 0
        
        if not self.slashing:      
            if py.key.get_pressed()[py.K_k]:
                self.slashing = True
                
                       
        if self.slashing:
            py.mixer.Sound.play(slash_sound)
            py.mixer.music.stop()
            self.get_time += time
            
            if p.right:
                self.direction = 1
                screen.blit(self.slashR[self.framecount//3], (self.x+20, self.y))
                self.framecount += 1
                #py.draw.rect(screen, (255, 0, 0), (p.x+20+(40*self.direction), p.y, p.w-40, p.h), 2)
                if self.get_time >= 300:
                    self.slashing = False
                    self.get_time = 0
                    self.hit = False

            if p.left:
                self.direction = -1
                screen.blit(self.slashL[self.framecount//3], (self.x-55 , self.y))
                self.framecount += 1
                #py.draw.rect(screen, (255, 0, 0), (p.x+20+(40*self.direction), p.y, p.w-40, p.h), 2)
                if self.get_time >= 300:
                    self.slashing = False
                    self.get_time = 0
                    self.hit = False

class hollow(object):
    walkL = [py.image.load("EL1.png").convert_alpha() ,py.image.load("EL2.png").convert_alpha(), py.image.load("EL3.png").convert_alpha(), py.image.load("EL4.png").convert_alpha(), py.image.load("EL5.png").convert_alpha(), py.image.load("EL6.png").convert_alpha(), py.image.load("EL7.png").convert_alpha(), py.image.load("EL8.png").convert_alpha(), py.image.load("EL9.png").convert_alpha(), py.image.load("EL10.png").convert_alpha()]
    walkR = [py.image.load("ER1.png").convert_alpha() ,py.image.load("ER2.png").convert_alpha(), py.image.load("ER3.png").convert_alpha(), py.image.load("ER4.png").convert_alpha(), py.image.load("ER5.png").convert_alpha(), py.image.load("ER6.png").convert_alpha(), py.image.load("ER7.png").convert_alpha(), py.image.load("ER8.png").convert_alpha(), py.image.load("ER9.png").convert_alpha(), py.image.load("ER10.png").convert_alpha()]
    #dead = [py.image.load("Edead (1).png").convert_alpha() ,py.image.load("Edead (2).png").convert_alpha(), py.image.load("Edead (3).png").convert_alpha(), py.image.load("Edead (4).png").convert_alpha()]
    
    def __init__(self, x, y, w, h, x2, vel):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel = vel
        self.x2 = x2
        self.path = [self.x, self.x2]
        self.framecount = 0
        self.hitbox = (self.x+18, self.y+4, self.w-35, self.h-10)
        self.got_hit = False
        
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[0]:
                self.x += self.vel
                
            else:
                self.vel = self.vel * -1
                self.framecount = 0
                
        else: #if self.vel < 0:
            if self.x - self.vel > self.path[1]:
                self.x += self.vel
            
            else:
                self.vel = self.vel * -1
                self.framecount = 0
    
    def draw(self, screen):
        
        if not self.got_hit:
            self.hitbox = (self.x+18, self.y+4, self.w-35, self.h-10)
            
            if self.framecount >= 30:
                self.framecount = 0
            
            
            if self.vel > 0:
                screen.blit(self.walkR[self.framecount//3], (self.x, self.y))
                self.framecount += 1
                
            else: #if self.vel < 0:
                screen.blit(self.walkL[self.framecount//3], (self.x, self.y))
                self.framecount += 1
        
            #py.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
            """else:
                self.vel = 0"""
            
            #getting hit
                
            if s.slashing:    
                if p.left:                
                    if s.y - s.h < self.hitbox[1] + self.hitbox[3] and s.y + s.h > self.hitbox[1]:
                       if s.x+85 + s.w-40 > self.hitbox[0] and s.x+85 - s.w-40 < self.hitbox[0] + self.hitbox[2]: #issue
                           self.collision()
                           s.hit = True
                           s.count += 1
                           
                elif p.right:
                    if s.y - s.h < self.hitbox[1] + self.hitbox[3] and s.y + s.h > self.hitbox[1]:
                       if s.x+20+40 + self.w-40 > self.hitbox[0] and s.x+20+40 - s.w-40 < self.hitbox[0] + self.hitbox[2]: #issue
                           self.collision()
                           s.hit = True
                           s.count += 1
                           
                        
        
    def collision(self):
        """if self.framecount >= 12:
            self.framecount = 0
            
        if not s.hit:
            screen.blit(self.dead[self.framecount//3], (self.x, self.y))
            self.framecount += 1"""    
        print("Victory Achieved")
        self.got_hit = True
        
    def attack(self):
        if not self.got_hit:
            if p.hitbox[1] - p.hitbox[3] <= self.hitbox[1]+5 + self.hitbox[3]-10 and p.hitbox[1] + p.hitbox[3] >= self.hitbox[1]+5:
                if p.hitbox[0] + p.hitbox[2] >= self.hitbox[0] and p.hitbox[0] - p.hitbox[2] <= self.hitbox[0] + self.hitbox[2]-10:
                    print("dead")
                    p.got_hit = True

                    play_again_menu()
                    
                    
    def update(self):
        self.draw(screen)
        self.move()
        self.attack()
    
                    
back = py.image.load("background1.png").convert()


clock = py.time.Clock()

#player
p = player(0, 540, 80, 80)

#weapon
s = slash(0, 540, 80, 80, clock.tick(30))

#enemies
h1 = hollow(1200, 540, 80, 80, 0, 7)
h2 = hollow(900, 540, 80, 80, 200, 7)
h3 = hollow(1700, 540, 80, 80, 0, 8)
h4 = hollow(2000, 540, 80, 80, 0, 7)
h5 = hollow(2200, 540, 80, 80, 0, 8)
h6 = hollow(2400, 540, 80, 80, 0, 7)
h7 = hollow(2600, 540, 80, 80, 0, 8)
h8 = hollow(2700, 540, 80, 80, 0, 8)
h9 = hollow(3000, 540, 80, 80, 0, 7)
h10 = hollow(3200, 540, 80, 80, 0, 9)
h11 = hollow(3500, 540, 80, 80, 0, 7)
h12 = hollow(3500, 540, 80, 80, 0, 8)
h13 = hollow(3500, 540, 80, 80, 0, 9)
h14 = hollow(3900, 540, 80, 80, 0, 8)
h15 = hollow(3700, 540, 80, 80, 0, 8)
h16 = hollow(3900, 540, 80, 80, 0, 7)
h17 = hollow(4100, 540, 80, 80, 0, 8)
h18 = hollow(4300, 540, 80, 80, 0, 8)
h19 = hollow(4500, 540, 80, 80, 0, 9)
h20 = hollow(4600, 540, 80, 80, 0, 8)
h21 = hollow(4700, 540, 80, 80, 0, 8)
h22 = hollow(4900, 540, 80, 80, 0, 8)
h23 = hollow(4700, 540, 80, 80, 0, 7)
h24 = hollow(4900, 540, 80, 80, 0, 8)
h25 = hollow(5100, 540, 80, 80, 0, 9)


def menu_window():
    click = False
    font1 = py.font.SysFont("Arial", 100)
    font2 = py.font.SysFont("Arial", 20)
    font = py.font.SysFont("Arial", 25)
    
    while True:
        clock.tick(30)  
        for event in py.event.get():
            if event.type == py.QUIT:
                py.display.quit()
                sys.exit()
                
            if event.type == py.MOUSEBUTTONDOWN :
                if event.button == 1:
                    click = True
                
        screen.blit(back, [0, 0])
                
        mouse_x, mouse_y = py.mouse.get_pos()
        
        #start button                
        start_button = py.Rect(screenwidth/2 - 60, screenheight/2 + 50, 120, 30)
        #py.draw.rect(screen, (255, 0, 0), (screenwidth/2 - 60, screenheight/2, 120, 30), 2)
        
        #quit button
        quit_button = py.Rect(screenwidth/2 - 60, screenheight/2 + 80, 60, 30)
        #py.draw.rect(screen, (255, 0, 0), (screenwidth/2 - 60, screenheight/2 + 30, 60, 30), 2)
        
        if start_button.collidepoint((mouse_x, mouse_y)):
            if click:
                game()
        
        if quit_button.collidepoint((mouse_x, mouse_y)):
            if click:
                py.display.quit()
                sys.exit()
                
    
        start = font.render("New Game", True, (0, 0, 0))
        _exit = font.render("Quit", True, (0, 0, 0))
        dark_souls = font1.render("DARK SOULS", True, (0, 0, 0))
        edition = font2.render("The Hollow Knight Edition", True, (0, 0, 0))
        
        screen.blit(start, [screenwidth/2 - 60, screenheight/2 + 50])
        screen.blit(_exit, [screenwidth/2 - 60, screenheight/2 + 80])
        screen.blit(dark_souls, [screenwidth/2 - 240, screenheight/2 - 100])
        screen.blit(edition, [screenwidth/2 - 100, screenheight/2])
        
        
        highscore()
        
        py.display.flip()
        
def play_again_menu():
    click = False
    font = py.font.SysFont("Arial", 25)
    font1 = py.font.SysFont("Arial", 100)
    
    
    while True:
        clock.tick(30)
        for event in py.event.get():
            if event.type == py.QUIT:
                py.display.quit()
                sys.exit()
                
            if event.type == py.MOUSEBUTTONDOWN :
                if event.button == 1:
                    click = True
                
        screen.blit(back, [0, 0])
        
        mouse_x, mouse_y = py.mouse.get_pos()
        
        #Buttons
        play_again_button =  py.Rect(screenwidth/2 - 60, screenheight/2 + 30, 120, 30) 
        #py.draw.rect(screen, (255, 0, 0), (screenwidth/2 - 60, screenheight/2, 120, 30), 2)
        main_menu_button = py.Rect(screenwidth/2 - 60, screenheight/2 + 60, 120, 30)
        #py.draw.rect(screen, (255, 0, 0), (screenwidth/2 - 60, screenheight/2+30, 120, 30), 2)
        quit_button = py.Rect(screenwidth/2 - 60, screenheight/2 + 90, 60, 30)
        
        #Button_texts
        play_again = font.render("Play Again", True, (0, 0, 0))
        main_menu = font.render("Main Menu", True, (0, 0, 0))
        _exit = font.render("Quit", True, (0, 0, 0))
        
        #Texts
        you_died = font1.render("YOU DIED", True, (0, 0, 0))
        
        #Button_workings
        if play_again_button.collidepoint(mouse_x, mouse_y):
            if click:
                game()
                
        if main_menu_button.collidepoint(mouse_x, mouse_y):
            if click:
                menu_window()
                
        if quit_button.collidepoint(mouse_x, mouse_y):
            if click:
                py.display.quit()
                sys.exit()                    
                
        screen.blit(you_died, [screenwidth/2 - 200, screenheight/2 - 100])
        screen.blit(play_again, [screenwidth/2 - 60, screenheight/2 + 30])
        screen.blit(main_menu, [screenwidth/2 - 60, screenheight/2 + 60])
        screen.blit(_exit, [screenwidth/2 - 60, screenheight/2 + 90])
        
        highscore()
        
        py.display.flip()
        
def pause_menu():
    click = False
    font = py.font.SysFont("Arial", 25)
    font1 = py.font.SysFont("Arial", 100)
    
    
    while True:
        clock.tick(30)
        for event in py.event.get():
            if event.type == py.QUIT:
                py.display.quit()
                sys.exit()
                
            if event.type == py.MOUSEBUTTONDOWN :
                if event.button == 1:
                    click = True
                
        screen.blit(back, [0, 0])
        
        mouse_x, mouse_y = py.mouse.get_pos()
        
        #Buttons
        play_again_button =  py.Rect(screenwidth/2 - 60, screenheight/2 + 30, 120, 30) 
        #py.draw.rect(screen, (255, 0, 0), (screenwidth/2 - 60, screenheight/2, 120, 30), 2)
        main_menu_button = py.Rect(screenwidth/2 - 60, screenheight/2 + 60, 120, 30)
        #py.draw.rect(screen, (255, 0, 0), (screenwidth/2 - 60, screenheight/2+30, 120, 30), 2)
        quit_button = py.Rect(screenwidth/2 - 60, screenheight/2 + 90, 60, 30)
        
        #Button_texts
        play_again = font.render("Continue", True, (0, 0, 0))
        main_menu = font.render("Main Menu", True, (0, 0, 0))
        _exit = font.render("Quit", True, (0, 0, 0))
        
        #Texts
        you_died = font1.render("Paused", True, (0, 0, 0))
        
        #Button_workings
        if play_again_button.collidepoint(mouse_x, mouse_y):
            if click:
                game()
                
        if main_menu_button.collidepoint(mouse_x, mouse_y):
            if click:
                menu_window()
                
        if quit_button.collidepoint(mouse_x, mouse_y):
            if click:
                py.display.quit()
                sys.exit()                    
                
        screen.blit(you_died, [screenwidth/2 - 150, screenheight/2 - 100])
        screen.blit(play_again, [screenwidth/2 - 60, screenheight/2 + 30])
        screen.blit(main_menu, [screenwidth/2 - 60, screenheight/2 + 60])
        screen.blit(_exit, [screenwidth/2 - 60, screenheight/2 + 90])
        
        highscore()
        
        py.display.flip()
        
def score(score):
    font1 = py.font.SysFont("Arial", 100)
    font = py.font.SysFont("Arial", 25)
    text = font.render("Hollow Slayed : " + str(score), True, (0, 0, 0))
    screen.blit(text, [0, 0])
    if score == 25:
        win = font1.render("Victory Achieved", True, (0, 0, 0))
        screen.blit(win, [screenwidth/2 - 300, screenheight/2 - 100])
   

HS = "score.txt"

def highscore():
    
    direction = os.path.dirname(__file__)
    with open(os.path.join(direction, HS), "r") as f:
        try :
            highscore = int(f.read())
        except :
            highscore = 0
    
    if s.count > highscore:  
        highscore = s.count
        with open(os.path.join(direction, HS), "w") as f:
            f.write(str(highscore))
         
        font = py.font.SysFont("Arial", 25)
        new = font.render("NEW HIGH SCORE!!!", True, (0, 0, 0))
        screen.blit(new, [130, 0])
        
    font = py.font.SysFont("Arial", 25)
    highscore = font.render("Highscore :" + str(highscore), True, (0, 0, 0))
    
    screen.blit(highscore, [0, 0])        
            

            
def game():
    global time
    while True:
        time = clock.tick(30)
        
        for event in py.event.get():
            if event.type == py.QUIT:
                py.display.quit()
                sys.exit()
               
        if py.key.get_pressed()[py.K_ESCAPE]:
            pause_menu()
            
        screen.blit(back, (0, 0))
           
        #Player
        p.move()
        p.draw(screen)
        
        #wepon
        s.draw(screen)
        
        #enemies
        h1.update()   
        h2.update()   
        h3.update()   
        h4.update()   
        h5.update()   
        h6.update()   
        h7.update()
        h8.update()   
        h9.update()
        h10.update()
        h11.update()
        h12.update()
        h13.update()
        h14.update()
        h15.update()
        h16.update()
        h17.update()
        h18.update()
        h19.update()
        h20.update()
        h21.update()
        h22.update()
        h23.update()
        h24.update()
        h25.update()
        #functions
        score(s.count)
        
        py.display.update()

menu_window()        








