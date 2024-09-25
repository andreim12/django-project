import random
import sys
import pygame

# Inițializează pygame
pygame.init()

# Dimensiuni fereastră
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Culori
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Dimensiuni blocuri Snake
BLOCK_SIZE = 20

# FPS
FPS = 10
clock = pygame.time.Clock()

# Font pentru afișare scor
font = pygame.font.SysFont(None, 35)


def display_score(score):
    """Afișează scorul pe ecran."""
    value = font.render(f"Scor: {score}", True, WHITE)
    window.blit(value, [0, 0])


def game_over():
    """Funcție pentru ecranul de game over."""
    window.fill(BLACK)
    msg = font.render("Game Over! Apasă Q pentru a ieși sau R pentru a reporni.", True, RED)
    window.blit(msg, [WIDTH / 6, HEIGHT / 3])
    pygame.display.update()

    # Bucla de game over
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    main()


def main():
    # Poziția inițială a șarpelui
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]

    # Direcția șarpelui
    direction = 'RIGHT'
    change_to = direction

    # Poziția inițială a mâncării
    food_pos = [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
    food_spawn = True

    # Scorul inițial
    score = 0

    # Bucla principală a jocului
    while True:
        # Gestionarea evenimentelor
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        # Actualizarea direcției
        direction = change_to

        # Actualizarea poziției șarpelui
        if direction == 'UP':
            snake_pos[1] -= BLOCK_SIZE
        if direction == 'DOWN':
            snake_pos[1] += BLOCK_SIZE
        if direction == 'LEFT':
            snake_pos[0] -= BLOCK_SIZE
        if direction == 'RIGHT':
            snake_pos[0] += BLOCK_SIZE

        # Creșterea șarpelui la mâncare
        snake_body.insert(0, list(snake_pos))
        if (snake_pos[0] < food_pos[0] + BLOCK_SIZE and
            snake_pos[0] + BLOCK_SIZE > food_pos[0] and
            snake_pos[1] < food_pos[1] + BLOCK_SIZE and
            snake_pos[1] + BLOCK_SIZE > food_pos[1]):
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Reaparția mâncării
        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                        random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
        food_spawn = True

        # Fundalul jocului
        window.fill(BLACK)

        # Desenează șarpele
        for block in snake_body:
            pygame.draw.rect(window, GREEN, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

        # Desenează mâncarea
        pygame.draw.rect(window, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

        # Verifică coliziuni
        # Coliziune cu marginile ferestrei
        if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
            game_over()

        # Coliziune cu propriul corp
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()

        # Afișează scorul
        display_score(score)

        # Actualizează ecranul
        pygame.display.update()

        # Controlează viteza șarpelui
        clock.tick(FPS)


if __name__ == "__main__":
    main()
