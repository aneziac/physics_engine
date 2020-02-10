import pygame as pg
import sys
import time
import random as rm
from math import sqrt, ceil


def engine():

    # Initialization
    pg.init()
    pg.display.init()
    SCR_HEIGHT, SCR_WIDTH = 400, 400  # screen dimensions
    WLD_HEIGHT, WLD_WIDTH = 200, 200  # earth dimensions
    SPACE_HEIGHT, SPACE_WIDTH = 400, 400 #space dimensions
    UNIT = "m" # unit for Y-axis scale
    TICK_MARKS = 5  # number of Y-axis tick marks
    SCREEN = pg.display.set_mode([SCR_WIDTH, SCR_HEIGHT]) # creates screen
    SCREEN.fill((255, 255, 255))  # blanks screen
    pg.display.set_caption("physics_engine v.0.2.0")
    FONT = pg.font.Font("Beckman-Free.otf", 30) # regular font
    FONTS = pg.font.Font("Beckman-Free.otf", 20) # small font
    SIMS = ["Earth 01", "Space 01"] # simulation names
    SHOW_VECTORS = False # displays acceleration and velocity vectors
    menu = True

    STARS_AMOUNT = 50
    STARS = []
    for x in range(STARS_AMOUNT):
        STARS.append([(rm.randint(0, SCR_WIDTH), rm.randint(0, SCR_HEIGHT)), rm.randint(2, 3)])
    
    # list of universal constants
    gc = 0.5 # gravitational constant
    em = 1000 # earth's mass (kg) 5972370000000000000000000
    er = 40 # earth's radius (m) 63781000
    
    # QIV -> QI transformations
    def trect(coords):  # transform rectangle (4 inputs)
        return (coords[0]+coords[2], SCR_HEIGHT-coords[1], -1*coords[2], -1*coords[3])

    def tcirc(coords):  # transform circle (2 inputs)
        return (coords[0], SCR_HEIGHT-coords[1])

    def rect(coords):  # quickly draw a black rectangle
        pg.draw.rect(SCREEN, (0, 0, 0), trect(coords))

    # defines properties of all objects
    class Object():
        instances = []

        def __init__(self, x, y, xv, yv, xa, ya, m, c, e):
            # 'i' prefix = intial
            self.ix = x  # x position
            self.iy = y  # y position
            self.ixv = xv  # x velocity
            self.iyv = yv  # y velocity
            self.ixa = xa #x acceleration
            self.iya = ya #y accleration
            self.im = m  # mass
            self.ic = c  # color
            self.ie = -e # COR
            Object.instances.append(self)

        def reset(self):
            self.x = self.ix
            self.y = self.iy
            self.xv = self.ixv
            self.yv = self.iyv
            self.xa = self.ixa
            self.ya = self.iya
            self.m = self.im
            self.c = self.ic
            self.e = self.ie

        def update(self, dt):
            self.xv += self.xa * dt
            self.yv += self.ya * dt
            self.x += round(self.xv) * dt
            self.y += round(self.yv) * dt
            
            if SHOW_VECTORS:
                pg.draw.line(SCREEN,(255,100,0),tcirc((self.x,self.y)),tcirc((self.x+(self.xa*50),self.y+(self.ya*50))),3)                    
                pg.draw.line(SCREEN,(2,100,100),tcirc((self.x,self.y)),tcirc((self.x+(self.xv*20),self.y+(self.yv*20))),3)

        def reset_all():
            for instance in Object.instances:
                instance.reset()

    class SPhysics():  # Space physics

        def physics(self):
            for obj in Object.instances:
                if self.x != obj.x and self.y != obj.y:
                    
                    # calculates magnitude of acceleration vector
                    self.am = -(gc * obj.m) / sqrt((self.x-obj.x)**2 + (self.y-obj.y)**2)                                        
                    # calculates acceleration vector
                    if self.m < 30:
                        self.xa = self.am*((self.x-obj.x)/sqrt((self.x-obj.x)**2 + (self.y-obj.y)**2))
                        self.ya = self.am*((self.y-obj.y)/sqrt((self.x-obj.x)**2 + (self.y-obj.y)**2))
        
        def scl(self, x):
            return int((x*SCR_HEIGHT)/SPACE_HEIGHT)            
                         
    class EPhysics():  # Earth physics
        def physics(self):
            self.xv += round((rm.random()*2)-1, 2)
            self.ya = -(gc*em)/(er**2)
        
        def scl(self, x):
            return int((x*SCR_HEIGHT)/WLD_HEIGHT)

    class Sphere(Object):
        def __init__(self, x, y, xv, yv, xa, ya, m, c, e, r):
            self.r = r
            super().__init__(x, y, xv, yv, xa, ya, m, c, e)

        def update(self, dt):
            super().physics()
            super().update(dt)

            # object to object collisions
            for obj in Object.instances:
                
                # if the balls are intersecting
                if self.x != obj.x and self.y != obj.y and ceil(sqrt(((self.x-obj.x)**2 + (self.y-obj.y)**2))) <= (self.r + obj.r):
                    
                    # calculates distance between centers of balls
                    self.p = round(sqrt((((self.x-obj.x)**2) + ((self.y-obj.y)**2))), 5)

                    # calculates the coordinates of the furthest intersecting point for each ball
                    self.sintx, self.sinty = self.x + ((self.r * (obj.x - self.x))/self.p), self.y + ((self.r * (obj.y - self.y))/self.p)  # self intersection
                    self.ointx, self.ointy = obj.x + ((obj.r * (self.x - obj.x))/self.p), obj.y + ((obj.r * (self.y - obj.y))/self.p)  # obj intersection

                    # calculates the distance between the intersecting points and creates move values
                    self.h = round(sqrt(((self.sintx - self.ointx) ** 2) + ((self.sinty - self.ointy) ** 2)) / 2, 5)
                    self.movex, self.movey = ceil((self.h * (self.x-obj.x)) / self.p), ceil((self.h * (self.y-obj.y)) / self.p)

                    # moves the objects accordingly, resolving the collision
                    self.x += self.movex
                    obj.x -= self.movex
                    self.y += self.movey
                    obj.y -= self.movey
                    
                    self.xvo, self.yvo = self.xv, self.xv # saves original values
                    
                    self.colCOR = 0.9 #(self.e + obj.e) / 2 # collision coefficient of restitution
                    self.xv = ((self.colCOR * obj.m) * (obj.xv-self.xv) + (self.m * self.xv) + (obj.m * obj.xv)) / (self.m + obj.m)
                    self.yv = ((self.colCOR * obj.m) * (obj.yv-self.yv) + (self.m * self.yv) + (obj.m * obj.yv)) / (self.m + obj.m)
                    obj.xv = ((self.colCOR * self.m) * (self.xvo-obj.xv) + (self.m * self.xvo) + (obj.m * obj.xv)) / (self.m + obj.m)
                    obj.yv = ((self.colCOR * self.m) * (self.yvo-obj.yv) + (self.m * self.yvo) + (obj.m * obj.yv)) / (self.m + obj.m)
        
        def render(self):
            pg.draw.circle(SCREEN, self.c, tcirc((super().scl(self.x), super().scl(self.y))), super().scl(self.r))
    
    class Ball(Sphere, EPhysics):
        def update(self, dt):
            super().update(dt)
            
            # wall collisions
            if self.x <= self.r:
                self.x = self.r
                self.xv *= self.e
            elif self.x >= (WLD_WIDTH-self.r):
                self.x = WLD_WIDTH-self.r
                self.xv *= self.e

            # ground collisons
            if self.y <= self.r:
                self.y = self.r
                self.yv *= self.e
        
    class Satellite(Sphere, SPhysics):
        #self.yv = sqrt((gc*self.m)/self.r) - circular orbit? return to
        pass
    
    while menu:
        
        SCREEN.blit(FONT.render("Choose simulation", True, pg.Color('black')), trect((int((SCR_WIDTH/2)-(FONT.size("Choose simulation")[0]/2)),SCR_HEIGHT-80,0,0)))
        buttons = []
        for x in range(len(SIMS)):
            buttons.append(pg.draw.rect(SCREEN,(0,0,0),((SCR_WIDTH/2-75,SCR_HEIGHT-200-(x*50),150,30))))
            SCREEN.blit(FONTS.render(SIMS[x], True, (0,200,0)), (int((SCR_WIDTH/2)-(FONTS.size(SIMS[x])[0]/2)),SCR_HEIGHT-198-(x*50),150,30))
        keys = pg.key.get_pressed()
       
        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_q]:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                clicked = [c for c in buttons if c.collidepoint(pg.mouse.get_pos())]
                
                if len(clicked) == 1:
                    sel = int((clicked[0][1]-150)/50) #selected
                
                    if sel == 0:
                        #implement camera later
                        asteroid = Satellite(20, 200, 0, 1, 0, 0, 5, (61, 61, 41), 0.5, 3)
                        sun = Satellite(200, 200, 0, 0, 0, 0, 50, (255, 204, 0), 0.5, 10)
                        planet = Satellite(200, 350, 3, 0, 0, 0, 25, (255, 0, 0), 0.5, 5)
                    
                    if sel == 1:
                        ball_1 = Ball(100, 190, 0, 0, 0, 0, 10, (0, 255, 0), 0.7, 10)
                        ball_2 = Ball(150, 190, 0, 0, 0, 0, 5, (0, 0, 255), 0.8, 5)
                        ball_3 = Ball(50, 190, 0, 0, 0, 0, 3, (255, 0, 0), 0.9, 3)
                        ball_4 = Ball(190, 190, 0, 0, 0, 0, 13, (100, 50, 0), 0.6, 13)
                    
                    SIM = SIMS[sel]                    
                    menu = False
        
        pg.display.update()
    
    Object.reset_all()    
    elapsed = time.time()
   
    # main loop
    while True:
        SCREEN.fill((255, 255, 255))

        # enables quitting by pressing q or clicking red x
        keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_q]:
                pg.quit()
                sys.exit()

        if keys[pg.K_r]:
            Object.reset_all()

        if SIM == SIMS[0]:
            SCREEN.fill((0, 0, 0))
            for x in range(STARS_AMOUNT):
                pg.draw.circle(SCREEN, (255,255,255), STARS[x][0], STARS[x][1])

        if SIM == SIMS[1]:
            # builds Y-axis scale
            for x in range(TICK_MARKS):
                a = x*round(SCR_HEIGHT/TICK_MARKS)
                if x % 2 == 0:
                    pg.draw.rect(SCREEN, (240,240,240), trect([0, a, SCR_WIDTH, SCR_HEIGHT/TICK_MARKS]))
                rect((0, a, 5, 2))
                SCREEN.blit(FONTS.render(str(int((x*WLD_HEIGHT)/TICK_MARKS)) + UNIT, True, pg.Color('black')), trect((2, a+13, 10, a)))
        
        dt = (time.time() - elapsed) * 50
        elapsed = time.time()
        
        if keys[pg.K_s]:
            dt /= 50

        if keys[pg.K_d]:
            dt /= 100

        for instance in Object.instances:
            instance.update(dt)

        for instance in Object.instances:
            instance.render()

        # updates frame and resets
        pg.display.update()


engine()
