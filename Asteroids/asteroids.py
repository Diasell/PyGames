# -*- coding: utf-8 -*-
"""
Created on Jan 7, 2016

@author: taras
"""

import pygame
import math
import random


# colors:
white  = (255, 255, 255)
black  = (0, 0, 0)
red    = (255, 0, 0)
green  = (0, 155, 0)
blue   = (0, 0, 139)
l_blue = (0, 0, 255)

# globals for user interface
WIDTH    = 800
HEIGHT   = 600
FPS      = 60
score    = 0
lives    = 3
time     = 0
FRICTION = 0.02


game_exit = False
game_over = False
paused = False
MY_EVENT = pygame.USEREVENT
VOLUME_LEVEL = [0.1, 0.5, 0.9]

"""Initializing PyGame and gamescreen"""
pygame.init()
pygame.mixer.init()
game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

"""importing images"""
intro_image     = pygame.image.load('images/intro.jpg')
debris_image    = pygame.image.load("images/debris2_blue.png")
nebula_image    = pygame.image.load("images/nebula_blue.f2014.png")
splash_image    = pygame.image.load("images/splash.png")
ship_image1     = pygame.image.load("images/ship.png")
ship_image2     = pygame.image.load("images/ship_thr.png")
missile_image   = pygame.image.load("images/shot1.png")
asteroid_image  = pygame.image.load("images/asteroid_blue.png")
explosion_image = pygame.image.load("images/explosion_alpha.png")
button_image    = pygame.image.load("images/button1.png")
pbutton_image   = pygame.image.load("images/button_pressed1.png")
gameover_image  = pygame.image.load("images/gameover.jpg")
settings_image  = pygame.image.load("images/settings1.jpg")

""" importing Sounds"""
soundtrack        = pygame.mixer.Sound("sounds/soundtrack.ogg")
missile_sound     = pygame.mixer.Sound("sounds/missile.ogg")
ship_thrust_sound = pygame.mixer.Sound("sounds/thrust.ogg")
explosion_sound   = pygame.mixer.Sound("sounds/explosion.ogg")

""" Setting up the sound volume level"""
explosion_sound.set_volume(VOLUME_LEVEL[1])
missile_sound.set_volume(VOLUME_LEVEL[1])
soundtrack.set_volume(VOLUME_LEVEL[1])


""" Setting up fonts"""
smallfont  = pygame.font.SysFont("comicsansms", 25)
mediumfont = pygame.font.SysFont("comicsansms", 50)
bigfont    = pygame.font.SysFont("comicsansms", 80)


# helper functions to handle transformations
def angle_to_vector(ang):
    """
    :param ang its an angle in degrees in the regular right-oriented Descartes
    But in pyGame coordinates are left oriented plus cos and sin take arguments
    in radians that is why this convertation is needed
    """
    return [math.cos(math.radians(ang)), -math.sin(math.radians(ang))]


def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""

    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def rock_spawner():
    global asteroid
    if not game_over:
        rock_pos = [random.randrange(0, WIDTH - 90),
                    random.randrange(0, HEIGHT - 90)]
        rock_vel = [random.randrange(-4, 4),
                    random.randrange(-4, 4)]
        rock_angle = 1
        rock_angle_vel = random.randrange(-10, 10)
        if score > 1000:
            rock_vel[0] += score // 1000
            rock_vel[1] += score // 1000
        asteroid = Sprites(rock_pos,
                           rock_vel,
                           rock_angle,
                           rock_angle_vel,
                           asteroid_image,
                           90)
                    
        if len(ASTEROIDS_GROUP) < 20 and\
                        abs(asteroid.pos[0] - ship.pos[0]) > 150 and\
                        abs(asteroid.pos[1] - ship.pos[1]) > 150:
            ASTEROIDS_GROUP.add(asteroid)
        else:
            pass


def group_collide(group, other_object):

    s = set(group)
    collide = False
    for item in s:
        if item.collide(other_object):
            expl = Sprites(other_object.pos,
                           [0, 0], 0, 0, explosion_image, 128, True)
            EXPLOSIONS_GROUP.add(expl)
            explosion_sound.play()
            group.remove(item)         
            collide = True
    return collide


def group_to_group_collide(group1, group2):
    global count_collision
    g1 = set(group1)
    count_collision = 0
    for item in g1:
        if group_collide(group2, item):
            count_collision += 1
            group1.discard(item)
            group2.discard(item)
    return count_collision


def game_lives(lives):
    text = smallfont.render("Lives: " + str(lives), True, white)
    game_display.blit(text, [WIDTH - 125 ,0])


def game_score(score):
    text = smallfont.render("Score: " + str(score), True, white)
    game_display.blit(text, [25,0])
  

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = mediumfont.render(text, True, color)
    elif size == "big":
        textSurface = bigfont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size = 'small'):

    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (WIDTH/2), (HEIGHT/2) + y_displace
    game_display.blit(textSurf, textRect)

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small" ):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = ((buttonx+buttonwidth/2)), (buttony+(buttonheight/2))
    game_display.blit(text_surf, text_rect)
    
def button(text, x, y, width, height, in_active_img, active_img, text_color, action=None):
    global game_over, paused
    cur   = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+width >= cur[0] >= x and y+height>= cur[1] > y:
        game_display.blit(pbutton_image, (x, y))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "settings":
                game_settings()
            if action == "play":
                game_loop()
            if action == "resume":
                paused = False
            if action == "menu":
                game_intro()

    else:
        game_display.blit(button_image, (x, y))
    text_to_button(text, text_color, x, y, width, height)


class Ships:

    def __init__(self, pos, vel, angle, angle_vel, image1, image2=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = angle
        self.angle_vel = angle_vel
        self.image1 = image1
        self.image2 = image2
        self.image_length = 70
        self.thrust = False

    def draw(self, game_display):
        if self.thrust == False:
            image = rot_center(self.image1, self.angle)
            game_display.blit(image, self.pos)
        if self.thrust == True:
            image = rot_center(self.image2, self.angle)
            game_display.blit(image, self.pos)
    
    def shoot(self):
        global missile        
        missile_pos = [(self.get_pos_center()[0]),
                       self.get_pos_center()[1]]
        missile_vel = [self.vel[0] + (angle_to_vector(self.angle)[0] * 10),
                       self.vel[1] + (angle_to_vector(self.angle)[1] * 10)]
        missile =  Sprites(missile_pos, missile_vel, 0, 0, missile_image, 10, False)
        MISSILE_GROUP.add(missile)     
    
    def update(self):
        self.angle  += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        """ fricrion """
        self.vel[0] = self.vel[0] * (1- FRICTION)
        self.vel[1] = self.vel[1] * (1- FRICTION)

        """ direction: """
        if self.thrust:
            self.vel[0] += angle_to_vector(self.angle)[0] * 0.3
            self.vel[1] += angle_to_vector(self.angle)[1] * 0.3

        """ screen wrapping"""
        if self.pos[0]> WIDTH+80:
            self.pos[0] = -80
        if self.pos[0] < -80:
            self.pos[0]= WIDTH

        if self.pos[1]>HEIGHT+80:
            self.pos[1] = -80
        if self.pos[1]<-80:
            self.pos[1]=HEIGHT
    
    def get_pos_center(self):
        return [self.pos[0]+ self.image_length/2, self.pos[1]+self.image_length/2]
    
    def get_radius(self):
        return self.image_length/2
    
    def thrusters_on(self):
        self.thrust = True
        ship_thrust_sound.play()
        
    def thrusters_off(self):
        self.thrust = False
        ship_thrust_sound.stop()

    def increase_angle_vel(self):
        self.angle_vel += 5 # in degrees

    def decrease_angle_vel(self):
        self.angle_vel -= 5 # in degrees


class Sprites:
    
    def __init__(self, pos, vel, ang, ang_vel, image, image_length=None, animated=False):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_length = image_length
        self.age = 0
        self.animated = animated
        self.missile_life = 50
        self.ss_lenght = 1
        self.ex_speed = 0



    def get_pos_center(self):
        return [self.pos[0]+ self.image_length/2, self.pos[1]+self.image_length/2]

    def get_radius(self):
        return self.image_length/2
    
    def draw(self, game_display):
        global time
        if self.animated == False:
            image = rot_center(self.image, self.angle)
            game_display.blit(image, self.pos)
        if self.animated == True:
            """current_index = (self.age % self.lifespan) // 1
            current_expl_center = [self.image_center[0] + current_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_expl_center, self.image_size, self.pos ,self.image_size)"""
            game_display.blit(self.image, self.pos, (self.ex_speed*self.ss_lenght,0,128,128))
        
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        if self.pos[0]> WIDTH:
            self.pos[0] = -45
        if self.pos[0] < -45:
            self.pos[0]= WIDTH

        if self.pos[1]>HEIGHT:
            self.pos[1] = -45
        if self.pos[1]<-45:
            self.pos[1]=HEIGHT
        self.age += 1
        self.ex_speed += 128
        if self.age >= self.missile_life:
            MISSILE_GROUP.discard(self)
            EXPLOSIONS_GROUP.discard(self)

        
    def collide(self, other_object):
        if dist(self.get_pos_center(), other_object.get_pos_center()) <= (self.get_radius() + other_object.get_radius()):
            return True
        else:
            return False

def game_intro():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        game_display.blit(intro_image, (0, 0))
        button("Play", 100, 200, 200, 48, button_image, pbutton_image, white, "play")
        button("Settings", 100, 250, 200, 48, button_image, pbutton_image, white, "settings")
        button("Quit", 100, 300, 200, 48, button_image, pbutton_image, white, "quit")
        pygame.display.update()
        clock.tick(FPS)


def game_settings():
    game_set = True
    
    while game_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        game_display.blit(settings_image, (0,0))
        button("Menu", 300, 500, 200, 48, button_image, pbutton_image, white, "menu")
        pygame.display.update()
        clock.tick(FPS)

def pause():
    global paused
    
    paused = True
    message_to_screen("Paused", white, -100, size="big")
    message_to_screen("Hit ENTER to resume or Q to quit", white, 25)
    #button("Resume", 100, 200, 200, 48, button_image, pbutton_image, white, "resume")
    #button("Quit", 100, 300, 200, 48, button_image, pbutton_image, white, "quit")
    pygame.display.update()
    print "hello"
    
    while paused:
        ship.thrusters_off()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(FPS)


def gameover():
    global game_over, ASTEROIDS_GROUP, MISSILE_GROUP, EXPLOSIONS_GROUP

    game_over = True
    ASTEROIDS_GROUP = set([])
    MISSILE_GROUP = set([])
    EXPLOSIONS_GROUP = set([])
    game_display.blit(gameover_image, (0, 0))
    game_lives(lives)
    game_score(score)
    message_to_screen("Game Over", white, -100, size="big")
    button("Play again", 175, 400, 200, 48, pbutton_image, button_image, white, "play")
    button("Exit to Menu", 425, 400, 200, 48, pbutton_image, button_image, white, "menu")
    pygame.display.update()
    clock.tick(FPS)

 
def game_loop():
    global time, lives, score, game_over, ship, ASTEROIDS_GROUP, MISSILE_GROUP, EXPLOSIONS_GROUP, pause
    game_over = False
    game_exit = False
    score = 0
    lives = 3
    ASTEROIDS_GROUP = set([])
    MISSILE_GROUP = set([])
    EXPLOSIONS_GROUP = set([])
                
    ship = Ships([WIDTH/2, HEIGHT/2], [0, 0], 0, 0, ship_image1, ship_image2)
    #asteroid = Sprite([0,0], [1,1], 0, 5, asteroid_image, 90)
    pygame.time.set_timer(MY_EVENT, 500)
    soundtrack.play(-1)
   
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # quit the screen
                quit()
            if game_over == False:
                if event.type == MY_EVENT:
                    rock_spawner() # spamming asteroids each second
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ship.increase_angle_vel()
                if event.key == pygame.K_RIGHT:
                    ship.decrease_angle_vel()
                if event.key == pygame.K_UP:
                    ship.thrusters_on()  
                if event.key == pygame.K_SPACE:
                    ship.shoot()
                    missile_sound.play()
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_ESCAPE:
                    ship.thrusters_off()
                    soundtrack.stop()
                    game_intro()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    ship.decrease_angle_vel()
                if event.key == pygame.K_RIGHT:
                    ship.increase_angle_vel()
                if event.key == pygame.K_UP:
                    ship.thrusters_off()

        game_display.blit(nebula_image, (0, 0))
        
        """-Animated Background-"""  
        time += 1
        wtime = (time / 4) % WIDTH
        game_display.blit(debris_image, (wtime-WIDTH*1.25, 0))
        game_display.blit(debris_image, (wtime - WIDTH/2, 0))
        game_display.blit(debris_image, (wtime + WIDTH/2, 0))

        ship.draw(game_display)
        
        for rock in ASTEROIDS_GROUP:
            rock.draw(game_display)
            rock.update()
            
        x = set(MISSILE_GROUP)
        for item in x:
            item.draw(game_display)
            item.update()
            
        e = set(EXPLOSIONS_GROUP)
        for item in e:
            item.draw(game_display)
            # explosion_sound.play()
            item.update()
            
        if group_collide(ASTEROIDS_GROUP, ship):
            lives -= 1
        if group_to_group_collide(ASTEROIDS_GROUP, MISSILE_GROUP):
            score += 1
        if lives <= 0:
            ship.thrusters_off()
            soundtrack.stop()
            gameover()

        game_score(score)
        game_lives(lives)
    
        ship.update()
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit
    quit()

game_intro()

