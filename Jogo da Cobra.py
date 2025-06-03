import pygame
import random
from pygame.locals import *

# Inicializa o Pygame
pygame.init()

# Configurações da tela (definidas ANTES de carregar imagens)
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 10  # Tamanho da grade
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cobra Esfomeada')

# Carrega o sprite sheet da cobra
try:
    sprite_sheet = pygame.image.load("A_pixel_art_sprite_sheet_of_a_snake_for_a_classic_.png").convert_alpha()
    print("Sprite sheet carregado com sucesso!", sprite_sheet.get_size())
except Exception as e:
    print("Erro ao carregar sprite sheet:", e)



def get_sprite(x, y, width=10, height=10):
    """Recorta e retorna uma parte específica do sprite sheet."""
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sprite_sheet, (0, 0), (x, y, width, height))
    return sprite

# Cores
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BROWN = (210, 180, 140)
WHITE = (255, 255, 255)

# Fonte
font = pygame.font.Font('freesansbold.ttf', 18)

# Direções
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

# Carregamento dos sprites individuais
head_up = get_sprite(0, 0)  # Coordenadas (ajustadas conforme o sprite)
head_down = get_sprite(10, 0)
head_left = get_sprite(20, 0)
head_right = get_sprite(30, 0)

body_horizontal = get_sprite(0, 10)
body_vertical = get_sprite(10, 10)

tail_up = get_sprite(0, 20)
tail_down = get_sprite(10, 20)
tail_left = get_sprite(20, 20)
tail_right = get_sprite(30, 20)

class SnakeGame:
    def __init__(self):
        self.running = True
        self.snake = [(200, 200), (210, 200), (220, 200)]
        self.direction = LEFT
        self.apple_pos = self.generate_apple()
        self.score = 0
        self.speed = 5
        self.clock = pygame.time.Clock()

    def generate_apple(self):
        """Gera uma nova posição para a maçã garantindo que não esteja na cobra."""
        while True:
            pos = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                   random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
            if pos not in self.snake:
                return pos

    def check_collision(self, pos1, pos2):
        """Verifica se duas posições são iguais."""
        return pos1 == pos2

    def handle_events(self):
        """Gerencia os eventos de entrada do jogador."""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

    def update(self):
        """Atualiza o estado do jogo."""
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        # Verifica colisão com as bordas
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            self.running = False

        # Verifica colisão com o próprio corpo
        if new_head in self.snake:
            self.running = False

        # Atualiza a posição da cobra
        self.snake.insert(0, new_head)

        # Verifica se comeu a maçã
        if self.check_collision(new_head, self.apple_pos):
            self.score += 5
            self.speed += 0.5
            self.apple_pos = self.generate_apple()
        else:
            self.snake.pop()  # Remove a cauda se não comeu

    def draw(self):
        # Desenha a cobra
        for i, pos in enumerate(self.snake):
            if i == 0:  # Cabeça da cobra
                if self.direction == UP:
                    screen.blit(head_up, pos)
                elif self.direction == DOWN:
                    screen.blit(head_down, pos)
                elif self.direction == LEFT:
                    screen.blit(head_left, pos)
                elif self.direction == RIGHT:
                    screen.blit(head_right, pos)
            elif i == len(self.snake) - 1:  # Cauda da cobra
                if self.snake[i - 1][0] > pos[0]:  # Vindo da direita
                    screen.blit(tail_right, pos)
                elif self.snake[i - 1][0] < pos[0]:  # Vindo da esquerda
                    screen.blit(tail_left, pos)
                elif self.snake[i - 1][1] > pos[1]:  # Vindo de baixo
                    screen.blit(tail_down, pos)
                elif self.snake[i - 1][1] < pos[1]:  # Vindo de cima
                    screen.blit(tail_up, pos)
            else:  # Corpo da cobra
                if self.snake[i - 1][0] == self.snake[i + 1][0]:  # Movimento vertical
                    screen.blit(body_vertical, pos)
                else:  # Movimento horizontal
                    screen.blit(body_horizontal, pos)

        # Exibe a pontuação
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (WIDTH - 120, 10))

        screen.fill(BROWN)  # Desenha a tela do jogo
        screen.blit(apple_img, self.apple_pos)   # Desenha a maçã
        pygame.display.update()
        pygame.time.wait(2000)

        pygame.display.update()

    def run(self):
        """Executa o loop principal do jogo."""
        while self.running:
            self.clock.tick(self.speed)
            self.handle_events()
            self.update()
            self.draw()

        self.game_over_screen()

    def game_over_screen(self):
        """Exibe a tela de Game Over."""
        while True:
            screen.fill(BROWN)
            game_over_font = pygame.font.Font('freesansbold.ttf', 50)
            game_over_text = game_over_font.render('Game Over', True, WHITE)
            score_text = font.render(f'Score: {self.score}', True, WHITE)

            screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50)))
            screen.blit(score_text, score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 20)))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:  # Reinicia o jogo
                        self.__init__()  # Reinicia os valores do jogo
                        self.run()
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        exit()

# Imagens
apple_img = pygame.image.load("apple.png")  # Carrega uma imagem de maçã
apple_img = pygame.transform.scale(apple_img, (10, 10))  # Ajusta o tamanho

#snake_skin = pygame.image.load("snake.png")  # Carrega a textura da cobra
#snake_skin = pygame.transform.scale(snake_skin, (10, 10))

# Inicia o jogo
if __name__ == "__main__":
    game = SnakeGame()
    game.run()




