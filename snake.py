import pygame 
import time
import random

pygame.init()  #initializes pygame

#define colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0) 
orange= (245, 134, 7)
blue = (0,0,255)
green = (0,255,0)
background = (200,200,200)

width, height = 480,480

game_display = pygame.display.set_mode((width,height)) #sets up window
pygame.display.set_caption("The Snake Game") #name of the window

clock = pygame.time.Clock()

snake_size = 20
snake_speed= 10

GRID_WIDTH = height / snake_size
GRID_HEIGHT = width / snake_size

message_font = pygame.font.SysFont('Impact',30)
score_font =  pygame.font.SysFont('Impact',20)

def print_score(score): #displays score on top left corner
    text = score_font.render("Score: " + str(score), True, orange)
    game_display.blit(text, [0,0])

def food_color(): #randomizes food color
            option = random.choice(['G','R', 'Y'])
            if option =='G':
                return (0,255,0)
            elif option =='Y':
                return (255,255,0)
            else:
                return (255,0,0)
    
def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(game_display, blue, [pixel[0],pixel[1], snake_size, snake_size])

def run_game():        
    game_over = False
    game_close = False
    x = width/2
    y = height/2
    COLOR = green #sets the first food to be green
    x_speed= 0
    y_speed= 0
    snake_pixels = []
    snake_length = 1
    food_x = random.randint(0, GRID_WIDTH -1) * snake_size
    food_y = random.randint(0, GRID_HEIGHT -1) * snake_size
    color_changed = False

    while not game_over:
        while game_close: #when game is over, menu shows up
            game_display.fill(black)
            game_over_message = message_font.render("GAME OVER!", True, red)
            game_display.blit(game_over_message, [width / 4+50, height / 3])
            game_over_message2 = message_font.render("Press 1 to Exit", True, white)
            game_display.blit(game_over_message2, [width/4+40,height/2])
            game_over_message3 = message_font.render("Press 2 to Restart", True, white)
            game_display.blit(game_over_message3, [width/4+20,height/4*3-25])
            
            print_score(snake_length - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: #When user press 1 game ends
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_2: #When user press 2 game restarts
                        run_game()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    
        for event in pygame.event.get(): #key bindings
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed = -snake_speed
                    y_speed = 0
                if event.key == pygame.K_RIGHT:
                    x_speed = snake_speed
                    y_speed = 0
                if event.key == pygame.K_UP:
                    x_speed = 0
                    y_speed = -snake_speed
                if event.key == pygame.K_DOWN:
                    x_speed = 0
                    y_speed = snake_speed
        if x>= width or x< 0 or y >= height or y<0: #if crushes into wall
            game_close = True
        x += x_speed
        y += y_speed
        
        game_display.fill(background)
         
        pygame.draw.rect(game_display, COLOR, [food_x, food_y,snake_size, snake_size]) #draws food
        
        #Makes red/yellow food turn into green
        if COLOR == red or COLOR == yellow: 
            if color_changed == False:
                old_time = pygame.time.get_ticks() #start time
                color_changed= True

            time_now = pygame.time.get_ticks() #current time
            if time_now>old_time+3000: #if 3 seconds passed
                color_changed = False
                pygame.draw.rect(game_display, green, [food_x, food_y, snake_size,snake_size])#green appears in place 
                COLOR = green
                
        snake_pixels.append([x,y])
        
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]  #delets the last pixel when the snake moves so it stays consistent
        for pixel in snake_pixels[:-1]: 
            if pixel == [x,y]:  #if the snake crushes into itself the game stops
                game_close = True
                
        draw_snake(snake_size,snake_pixels)
        print_score(snake_length-1)
        
        
        if x == food_x and y == food_y and COLOR ==green: #when snake eats green food
            food_x = random.randint(0, GRID_WIDTH -1) * snake_size  #generates coordinates for new food
            food_y = random.randint(0, GRID_HEIGHT -1) * snake_size
            COLOR = food_color()
            snake_length +=1 
        if x == food_x and y == food_y and COLOR == yellow: #when snake eats yellow food
            food_x = random.randint(0, GRID_WIDTH -1) * snake_size
            food_y = random.randint(0, GRID_HEIGHT -1) * snake_size
            COLOR = food_color()
            snake_length -=1 
            del snake_pixels[0]
            if snake_length <1: #if snake eats yellow when has only one block
                game_close = True 
                snake_length =1 
        if x == food_x and y == food_y and COLOR == red: #when red is eaten, game over
            game_close = True
        clock.tick(snake_speed+10)
        pygame.display.update()
    pygame.quit()
    quit()
run_game()