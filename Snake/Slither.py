'''
Created on Jan 5, 2016

@author: taras
'''
import pygame
import random

# colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 255)

display_width = 750
display_height = 450

FPS = 15
direction = 'right'
pygame.init()

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')

bg_image = pygame.image.load('images/game_bg.png')

icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

img = pygame.image.load('images/snake_head.png')
apple_img = pygame.image.load("images/apple.png")

pygame.display.update()

clock = pygame.time.Clock()

block_size = 20
apple_size = 40

smallfont = pygame.font.SysFont("comicsansms", 25)
mediumfont = pygame.font.SysFont("comicsansms", 50)
bigfont = pygame.font.SysFont("comicsansms", 80)


def pause():

    paused = True
    message_to_screen("Paused", black, -100, size="big")
    message_to_screen("Press C to continue or Q to quit", black, 25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)


def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - apple_size))
    randAppleY = round(random.randrange(0, display_height - apple_size))
    return randAppleX, randAppleY


def game_intro():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither",
                          green,
                          -100,
                          "big")
        message_to_screen("The objective of the game is to eat red apples",
                          black,
                          -30)
        message_to_screen("The more apples you eat the longer you get",
                          black,
                          10)
        message_to_screen("if you run into yourself or edges you die",
                          black,
                          50)
        message_to_screen("Press C to play, P to pause or Q to quit",
                          black,
                          180)

        pygame.display.update()
        clock.tick(5)


def snake(block_size, snake_list):

    if direction == 'right':
        head = pygame.transform.rotate(img, 270)
    if direction == 'left':
        head = pygame.transform.rotate(img, 90)
    if direction == 'up':
        head = img
    if direction == 'down':
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snake_list[-1][0],snake_list[-1][1]))
    for XnY in snake_list[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])


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
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf, textRect)

def gameLoop():
    global direction
    direction = "right"
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 10
    lead_y_change = 0

    snake_list = []
    snake_length = 1

    randAppleX, randAppleY = randAppleGen()

    while not gameExit:
        if gameOver == True:
            message_to_screen("Game Over", red, -50, size = "big")
            message_to_screen("Press C to play again or Q to quit", black , 50, size = "small")
            pygame.display.update()

        while gameOver == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = 'right'
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = 'down'
                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width-block_size or lead_x <= 0 or lead_y >= display_height-block_size or lead_y <= 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.blit(bg_image, (0,0))
        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, apple_size, apple_size])
        gameDisplay.blit(apple_img, (randAppleX, randAppleY))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snake_list.append(snakeHead)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for item in snake_list[:-1]:
            if item == snakeHead:
                gameOver = True
        snake(block_size, snake_list)

        if lead_x > randAppleX and lead_x < randAppleX + apple_size or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + apple_size:
            if lead_y > randAppleY and lead_y < randAppleY + apple_size:
                randAppleX, randAppleY = randAppleGen()
                snake_length += 1
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + apple_size:
                randAppleX, randAppleY = randAppleGen()
                snake_length += 1

        score(snake_length-1)
        pygame.display.update()
        clock.tick(FPS)
        
    pygame.quit()
    quit()

game_intro()
gameLoop()
