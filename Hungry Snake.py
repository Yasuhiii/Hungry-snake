import pygame, random
from pygame.locals import *

# Funções principais
def on_grid_random():  #create a random grid
    x = random.randint(0, 59)
    y = random.randint(0, 59)
    return (x * 10, y * 10)

def collision(c1, c2):  #verifies colision between the objects
    return c1[0] == c2[0] and c1[1] == c2[1]

#start the game
def initialize_game():
    snake = [(200, 200), (210, 200), (220, 200)]
    apple_pos = on_grid_random()
    return snake, apple_pos, LEFT, 0, initial_speed

#global variables
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

#difficulty option
difficulty = None
while difficulty not in ("easy", "medium", "hard"):
    difficulty = input("Escolha a dificuldade (easy/medium/hard): ").lower()

if difficulty == "easy":
    initial_speed = 5
    speed_increment = 0.5
elif difficulty == "medium":
    initial_speed = 7
    speed_increment = 1
elif difficulty == "hard":
    initial_speed = 9
    speed_increment = 1.5

#pygame's configuration
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cobra Esfomeada')
font = pygame.font.Font('freesansbold.ttf', 18)

#start the states of the game
snake, apple_pos, my_direction, score, speed = initialize_game()
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((0, 128, 0))  #snake's color - green

apple = pygame.Surface((10, 10))
apple.fill((255, 0, 0))  # apple's color - red

game_over = False
clock = pygame.time.Clock()

#main loop
while not game_over:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_UP and my_direction != DOWN:
                my_direction = UP
            if event.key == K_DOWN and my_direction != UP:
                my_direction = DOWN
            if event.key == K_LEFT and my_direction != RIGHT:
                my_direction = LEFT
            if event.key == K_RIGHT and my_direction != LEFT:
                my_direction = RIGHT

    #verifies colision to the apple
    if collision(snake[0], apple_pos):
        apple_pos = on_grid_random()
        snake.append((0, 0))
        score += 5
        speed += speed_increment

    #verifies colision to the edge
    if snake[0][0] >= width or snake[0][1] >= height or snake[0][0] < 0 or snake[0][1] < 0:
        game_over = True

    #verifies colision from snake's body
    if snake[0] in snake[1:]:
        game_over = True

    if game_over:
        break

    #move the snake's body
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = snake[i - 1]

    #move the snake's head
    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])

    #update the screen
    screen.fill((210, 180, 140))
    screen.blit(apple, apple_pos)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (width - 120, 10))

    for pos in snake:
        screen.blit(snake_skin, pos)

    pygame.display.update()

#game over screen
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                snake, apple_pos, my_direction, score, speed = initialize_game()
                game_over = False
                break
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()

    screen.fill((210, 180, 140))
    game_over_font = pygame.font.Font('freesansbold.ttf', 75)
    game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
    game_over_rect = game_over_screen.get_rect(center=(width / 2, height / 2 - 50))
    screen.blit(game_over_screen, game_over_rect)

    score_font = font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_font.get_rect(center=(width / 2, height / 2 + 20))
    screen.blit(score_font, score_rect)

    pygame.display.update()
