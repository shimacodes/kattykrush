import pygame
import random
import sys
import math

pygame.init()

# Les variables de départ
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4
SPACING = 20
NUM_CAT_TYPES = 4
CAT_SIZE = 75
TILE_SIZE = CAT_SIZE

# La jooolie grille de chatons
GRID_WIDTH = GRID_SIZE * TILE_SIZE + (GRID_SIZE - 1) * SPACING
GRID_HEIGHT = GRID_SIZE * TILE_SIZE + (GRID_SIZE - 1) * SPACING
GRID_X_OFFSET = (WIDTH - GRID_WIDTH) // 2
GRID_Y_OFFSET = (HEIGHT - GRID_HEIGHT) // 2

# Les variables pour le jeu en lui-même
cat_grid = [[random.randint(0, NUM_CAT_TYPES - 1) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
selected_cat_pos = None
score = 0
game_started = False
game_over = False
booster_pos = None
booster_active = False

# Les chats exotiques importés
cat_images = [pygame.transform.scale(pygame.image.load(path), (CAT_SIZE, CAT_SIZE)) for path in [
    "cat heads/cat blanc.png",
    "cat heads/cat noir.png",
    "cat heads/Head.png",
    "cat heads/merida.png"
]]
booster_image = pygame.transform.scale(pygame.image.load("boosters/Paw.png"), (CAT_SIZE, CAT_SIZE))

# Les variables du menu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Katty Krush")
font = pygame.font.Font("space_invaders.ttf", 30)
TITLE = pygame.font.Font("space_invaders.ttf", 50)
clock = pygame.time.Clock()
start_button = pygame.Rect(WIDTH // 2 - 75, 300, 150, 50)

#La grille de chatons est dessinée. 
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = GRID_X_OFFSET + col * (TILE_SIZE + SPACING)
            y = GRID_Y_OFFSET + row * (TILE_SIZE + SPACING)
            if booster_pos == (row, col):
                screen.blit(booster_image, (x, y))
            else:
                cat_type = cat_grid[row][col]
                if selected_cat_pos == (row, col):#Chaque chat a son moment de gloire.
                    time_ms = pygame.time.get_ticks()
                    scale_factor = 1.2 + 0.1 * math.sin(time_ms / 150)
                    scaled_size = int(CAT_SIZE * scale_factor)
                    offset = (scaled_size - CAT_SIZE) // 2
                    scaled_img = pygame.transform.smoothscale(cat_images[cat_type], (scaled_size, scaled_size))
                    screen.blit(scaled_img, (x - offset, y - offset))
                else:
                    screen.blit(cat_images[cat_type], (x, y))

def is_valid_swap(pos1, pos2):
    def makes_match():
        matched = set()
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 2):
                if cat_grid[r][c] == cat_grid[r][c + 1] == cat_grid[r][c + 2]:
                    matched.update({(r, c), (r, c + 1), (r, c + 2)})
        for c in range(GRID_SIZE):
            for r in range(GRID_SIZE - 2):
                if cat_grid[r][c] == cat_grid[r + 1][c] == cat_grid[r + 2][c]:
                    matched.update({(r, c), (r + 1, c), (r + 2, c)})
        return len(matched) > 0
    swap_cats(pos1, pos2)
    valid = makes_match()
    swap_cats(pos1, pos2)  # Revert
    return valid

def any_possible_matches():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if c + 1 < GRID_SIZE and is_valid_swap((r, c), (r, c + 1)):
                return True
            if r + 1 < GRID_SIZE and is_valid_swap((r, c), (r + 1, c)):
                return True
    return False

def swap_cats(pos1, pos2):
    global score, booster_pos, booster_active
    r1, c1 = pos1
    r2, c2 = pos2
    if booster_pos in [pos1, pos2]:
        score *= 4
        booster_pos = None
        booster_active = False
    else:
        cat_grid[r1][c1], cat_grid[r2][c2] = cat_grid[r2][c2], cat_grid[r1][c1]#votre méthode était plus logique monsieur, vous avez gagné le badge de "Neko-Sensei"

def handle_matches():
    global score, booster_pos, booster_active
    matched = set()
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 2):
            if cat_grid[r][c] == cat_grid[r][c + 1] == cat_grid[r][c + 2]:
                matched.update({(r, c), (r, c + 1), (r, c + 2)})
    for c in range(GRID_SIZE):
        for r in range(GRID_SIZE - 2):
            if cat_grid[r][c] == cat_grid[r + 1][c] == cat_grid[r + 2][c]:
                matched.update({(r, c), (r + 1, c), (r + 2, c)})
    for r, c in matched:
        cat_grid[r][c] = random.randint(0, NUM_CAT_TYPES - 1)
    score += len(matched)

    if score > 15 and not booster_active:
        while True:
            r = random.randint(0, GRID_SIZE - 1)
            c = random.randint(0, GRID_SIZE - 1)
            if (r, c) not in matched:
                booster_pos = (r, c)
                booster_active = True
                break

def handle_input():
    global selected_cat_pos, game_started, game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                if start_button.collidepoint(event.pos):
                    game_started = True
                    game_over = False
            elif not game_over:
                x, y = event.pos
                col = (x - GRID_X_OFFSET) // (TILE_SIZE + SPACING)
                row = (y - GRID_Y_OFFSET) // (TILE_SIZE + SPACING)
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    if selected_cat_pos:
                        r0, c0 = selected_cat_pos
                        if abs(r0 - row) + abs(c0 - col) == 1:
                            if is_valid_swap((r0, c0), (row, col)) or booster_pos in [(r0, c0), (row, col)]:
                                swap_cats((r0, c0), (row, col))
                            selected_cat_pos = None
                        else:
                            selected_cat_pos = (row, col)
                    else:
                        selected_cat_pos = (row, col)

def draw_game():
    screen.fill((73, 151, 208))
    draw_grid()
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, HEIGHT - 30))

def draw_menu():
    screen.fill((73, 151, 208))
    title = TITLE.render("KATTY KRUSH!", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
    pygame.draw.rect(screen, (200, 100, 100), start_button)
    start_text = font.render("START", True, (255, 255, 255))
    screen.blit(start_text, (start_button.x + 20, start_button.y + 10))

def draw_game_over():
    screen.fill((73, 151, 208))
    text = TITLE.render("Game Over!", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

# Main loop
while True:
    handle_input()
    if game_started:
        if not game_over:
            handle_matches()
            if not any_possible_matches():
                game_over = True
            draw_game()
        else:
            draw_game_over()
    else:
        draw_menu()
    pygame.display.flip()
    clock.tick(30)
