import random
import pygame

def load(file):
    with open(file) as file:
        return [line[:5].upper() for line in file.readlines()]

GUESSING = load("Wordle/dict_english.txt")
ANSWERS = load("Wordle/dict_wordle.txt")
ANSWER = random.choice(ANSWERS)

WIDTH, HEIGHT, MARGIN, T_MARGIN, B_MARGIN, LR_MARGIN = 500, 600, 10, 30, 50, 50
GREY, GREEN, YELLOW, WHITE = (100, 100, 100), (80, 200, 70), (250, 200, 100), (255,255,255)

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption("Wordle")

SQ_SIZE = (WIDTH - 4 * MARGIN - 2 * LR_MARGIN) // 5
FONT = pygame.font.SysFont('sansbold', SQ_SIZE)

# Initialize game variables
INPUT = ""
GUESSES = []
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
GAME_OVER = False

# Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                if INPUT:
                    INPUT = INPUT[:-1]
            elif event.key == pygame.K_RETURN:
                if len(INPUT) == 5 and INPUT in GUESSING:
                    GUESSES.append(INPUT)
                    GAME_OVER = INPUT == ANSWER
                    INPUT = ""
            elif event.key == pygame.K_SPACE:
                GAME_OVER = False
                ANSWER = random.choice(ANSWERS)
                GUESSES = []
                INPUT = ""
            elif len(INPUT) < 5 and not GAME_OVER:
                INPUT = INPUT + event.unicode.upper()
            
    # Clear the screen
    screen.fill(WHITE)

    # Draw guesses
    y = T_MARGIN
    for i in range(6):
        x = LR_MARGIN
        for j in range(5):
            square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, GREY, square, width=2, border_radius=3)

            if i < len(GUESSES):
                color = GREEN if GUESSES[i][j] == ANSWER[j] else YELLOW if GUESSES[i][j] in ANSWER else GREY
                pygame.draw.rect(screen, color, square, border_radius=3)
                letter = FONT.render(GUESSES[i][j], False, (255, 255, 255))
                surface = letter.get_rect(center=(x + SQ_SIZE // 2, y + SQ_SIZE // 2))
                screen.blit(letter, surface)

            if i == len(GUESSES) and j < len(INPUT):
                letter = FONT.render(INPUT[j], False, GREY)
                surface = letter.get_rect(center=(x + SQ_SIZE // 2, y + SQ_SIZE // 2))
                screen.blit(letter, surface)

            x += SQ_SIZE + MARGIN
        y += SQ_SIZE + MARGIN

    # Draw the correct answer when the game is over
    if len(GUESSES) == 6 and GUESSES[5] != ANSWER:
        GAME_OVER = True
        letters = FONT.render(ANSWER, False, GREY)
        surface = letters.get_rect(center=(WIDTH // 2, HEIGHT - B_MARGIN // 2 - MARGIN))
        screen.blit(letters, surface)
    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()