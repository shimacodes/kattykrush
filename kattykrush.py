import pygame
import sys
import random

pygame.init() # initialisation du module "pygame" 

fenetre = pygame.display.set_mode( (600,600) ) # Création d'une fenêtre graphique de taille 600x600 pixels
pygame.display.set_caption("Katty Krush!") # Définit le titre de la fenêtre

# Chargement des images:
#    On définit et affecte les variables qui contiendront les images des différents chats
i1w = pygame.image.load("cat heads\cat blanc.png")
i2t = pygame.image.load("cat heads\Head.png")
i3g = pygame.image.load("cat heads\merida.png")
i4b= pygame.image.load("cat heads\cat noir.png")
paw1= pygame.image.load("boosters\Paw.png")
paw2= pygame.image.load("boosters\sPaw.png")
pygame.display.set_icon(i4b)


# On définit le tableau de chats
def generate_initial_grid(rows, cols, num_cat_types):
    while True:
        grid = [[random.randint(0, num_cat_types - 1) for _ in range(cols)] for _ in range(rows)]
        if not has_initial_matches(grid):
            return grid

def has_initial_matches(grid):
    rows = len(grid)
    cols = len(grid[0])

    # On vérifie les lignes
    for r in range(rows):
        for c in range(cols - 2):
            if grid[r][c] == grid[r][c+1] == grid[r][c+2]:
                return True

    # On vérifie les colonnes
    for c in range(cols):
        for r in range(rows - 2):
            if grid[r][c] == grid[r+1][c] == grid[r+2][c]:
                return True

    return False
num_rows = 4
num_cols = 4
num_cat_types = 4
catn = generate_initial_grid(num_rows, num_cols, num_cat_types)
print("Initial grid:")
for row in catn:
    print(row)
arial24 = pygame.font.Font("space_invaders.ttf",20)
TITLE=pygame.font.Font("space_invaders.ttf",70)
score=0
print(catn)
PAW1=5
PAW2=6
selected_cat_grid_pos = None
scale_factor = 1.1
def gistudio():
    fenetre.fill((0, 0, 0))
    gst=TITLE.render(f"GI STUDTIOS", True, (255, 255, 255))
    fenetre.blit(gst,(200,200))
    pygame.time.wait(3000)
def theogcat():
    fenetre.fill((81, 151, 187))
    title=TITLE.render(f"KATTY KRUSH!", True, (255, 255, 255))
    fenetre.blit(title,(200,200))

# Fonction en charge de dessiner tous les éléments sur notre fenêtre graphique principale.
# Cette fonction sera appelée depuis notre boucle infinie
def dessiner():
    global fenetre, catn, score, selected_cat_pos, scale_factor, PAW1, PAW2 # Use selected_cat_pos
    fenetre.fill((81, 151, 187))
    for j in range(len(catn)):
        for i in range(len(catn[0])):
            pos_x = 43 + i * 150
            pos_y = 20 + j * 150

            image = None
            if catn[j][i] == 0:
                image = i1w
            elif catn[j][i] == 1:
                image = i2t
            elif catn[j][i] == 2:
                image = i3g
            elif catn[j][i] == 3:
                image = i4b
            elif catn[j][i] == PAW1:
                image=paw1
            elif catn[j][i] == PAW2:
                image=paw2
                if catn[j][i] == 0: image = i1w
                elif catn[j][i] == 1: image = i2t
                elif catn[j][i] == 2: image = i3g
                elif catn[j][i] == 3: image = i4b

            if image is not None:
                if selected_cat_pos == (j, i):
                    scaled_width = int(image.get_width() * scale_factor)
                    scaled_height = int(image.get_height() * scale_factor)
                    scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))
                    blit_x = pos_x - (scaled_width - image.get_width()) // 2
                    blit_y = pos_y - (scaled_height - image.get_height()) // 2
                    fenetre.blit(scaled_image, (blit_x, blit_y))
                else:
                    fenetre.blit(image, (pos_x, pos_y))

    score_text = arial24.render(f"Score: {score}", True, (255, 255, 255))
    fenetre.blit(score_text, (250, 570))
    pygame.display.flip() # Rafraichissement complet de la fenêtre avec les dernières opérations de dessin
#n
booster1_active = False
booster1_timer = 0

def pawboosters():
    global catn, score, booster1_active, booster1_timer

    if score >= 5 and not any( PAW1 in row for row in catn): # Check if score reached 5 and no Booster 1 is present
        print("Score reached 5! Deploying boosters...")
        rows = len(catn)
        cols = len(catn[0])
        num_boosters = random.randint(1, 3) # Deploy 1 to 3 boosters

        booster_placed_count = 0
        attempt = 0
        max_attempts = rows * cols * 2 # Avoid infinite loops

        while booster_placed_count < num_boosters and attempt < max_attempts:
            rand_row = random.randint(0, rows - 1)
            rand_col = random.randint(0, cols - 1)

            if catn[rand_row][rand_col] < PAW1: # Only replace regular cats
                catn[rand_row][rand_col] = PAW1
                booster_placed_count += 1
                print(f"Booster 1 placed at ({rand_row}, {rand_col})")
            attempt += 1

        score = 0 # Reset score after deploying boosters

    if booster1_active:
        booster1_timer -= 1
        if booster1_timer <= 0:
            booster1_active = False
            print("Booster 1 effect ended.")

def apply_score(points):
    global score, booster1_active
    if booster1_active:
        return points * 2
    return points
def find_matches(grid):
    rows = len(grid)
    cols = len(grid[0])
    matches = set()

# On a 6 autres situations possibles où la réunion fraternelle est possible. Allons-y!
    for r in range(rows):
        for c in range(cols - 2):
            if grid[r][c] is not None and grid[r][c] == grid[r][c+1] == grid[r][c+2]:
                match_type = grid[r][c]
                for i in range(3):
                    matches.add((r, c + i))
                for i in range(c + 3, cols):
                    if grid[r][i] == match_type:
                        matches.add((r, i))
                    else:
                        break
    for c in range(cols):
        for r in range(rows - 2):
            if grid[r][c] is not None and grid[r][c] == grid[r+1][c] == grid[r+2][c]:
                match_type = grid[r][c]
                for i in range(3):
                    matches.add((r + i, c))
                for i in range(r + 3, rows):
                    if grid[i][c] == match_type:
                        matches.add((i, c))
                    else:
                        break
    return matches
def handle_matches():
    global catn, score
    matched_coords = find_matches(catn)
    if matched_coords:
        score +=3
        print(f"Match found! Score: {score} + {3}")

        # Check for 4-in-a-row matches to potentially spawn Booster 2
        rows = len(catn)
        cols = len(catn[0])
        matched_sequences = set() # To avoid redundant checks

        # Check rows for 4+
        for r in range(rows):
            c = 0
            while c < cols - 3:
                if catn[r][c] is not None and catn[r][c] == catn[r][c+1] == catn[r][c+2] == catn[r][c+3]:
                    match_type = catn[r][c]
                    for i in range(4):
                        matched_sequences.add(((r, c + i), match_type))
                    c += 4
                else:
                    c += 1

        # Check columns for 4+
        for c in range(cols):
            r = 0
            while r < rows - 3:
                if catn[r][c] is not None and catn[r][c] == catn[r+1][c] == catn[r+2][c] == catn[r+3][c]:
                    match_type = catn[r][c]
                    for i in range(4):
                        matched_sequences.add(((r + i, c), match_type))
                    r += 4
                else:
                    r += 1

        # If a 4-match occurred, mark one of the matched cats for potential Booster 2
        if matched_sequences:
            (spawn_r, spawn_c), _ = random.choice(list(matched_sequences))
            if catn[spawn_r][spawn_c] < PAW1: # Ensure we don't overwrite other boosters
                catn[spawn_r][spawn_c] = PAW2
                print(f"A 4-match occurred! A potential Booster 2 spawned at ({spawn_r}, {spawn_c})")

        # Remove the matched cats and refill
        resolve_matches()
        return True
    return False

def handle_booster_activation(r, c):
    global catn, booster1_active, booster1_timer, score

    if catn[r][c] == PAW1:
        booster1_active = True
        booster1_timer = 30 * 50 # 30 seconds * frames per second
        print("Booster 1 activated! Score doubled for 30 seconds.")
        catn[r][c] = random.randint(0, 3) # Replace booster with a random cat
        return True
    elif catn[r][c] == PAW2:
        # Booster 2 activation happens on the next swap to create a match with this cat
        return False # Indicate it's not an immediate activation
    return False
# Fonction en charge de gérer les évènements clavier (ou souris), et notamment les échanges de chats
# Cette fonction sera appelée depuis notre boucle infinie
def gererClavierEtSouris():
    global continuer, catn, selected_cat_pos, booster1_active, score

    def check_match_swap(grid, r, c):
        rows = len(grid)
        cols = len(grid[0])
        cat_type = grid[r][c]
        if cat_type is None or cat_type >= PAW1:
            return None

        # Check horizontal
        count = 1
        for dc in [-1, 1]:
            for i in range(1, 3):
                cc = c + dc * i
                if 0 <= cc < cols and grid[r][cc] == cat_type:
                    count += 1
                else:
                    break
        if count >= 3:
            return cat_type

        # Check vertical
        count = 1
        for dr in [-1, 1]:
            for i in range(1, 3):
                rr = r + dr * i
                if 0 <= rr < rows and grid[rr][c] == cat_type:
                    count += 1
                else:
                    break
        if count >= 3:
            return cat_type
        return None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mous = pygame.mouse.get_pos()
            col = mous[0] // 150
            row = mous[1] // 150
            if 0 <= row < len(catn) and 0 <= col < len(catn[0]):
                selected_cat_pos = (row, col)
                print(f"Selected cat at grid: ({row}, {col})")
            else:
                selected_cat_pos = None

    keypress = pygame.key.get_pressed()
    if selected_cat_pos is not None:
        row_orig, col_orig = selected_cat_pos
        original_cat_type = catn[row_orig][col_orig]

        moves = {
            pygame.K_RIGHT: (0, 1),
            pygame.K_LEFT: (0, -1),
            pygame.K_DOWN: (1, 0),
            pygame.K_UP: (-1, 0)
        }

        for key, (dr, dc) in moves.items():
            if keypress[key]:
                row_target, col_target = row_orig + dr, col_orig + dc
                if 0 <= row_target < len(catn) and 0 <= col_target < len(catn[0]):
                    target_cell_value = catn[row_target][col_target]

                    # Attempt swap
                    temp_catn = [list(r) for r in catn]
                    temp_catn[row_orig][col_orig], temp_catn[row_target][col_target] = temp_catn[row_target][col_target], temp_catn[row_orig][col_orig]

                    # Check for match at the target position
                    matched_type = check_match_swap(temp_catn, row_target, col_target)
                    if matched_type is not None:
                        catn[row_orig][col_orig], catn[row_target][col_target] = catn[row_target][col_target], catn[row_orig][col_orig]
                        current_matches = find_matches(catn)
                        points = 3

                        if original_cat_type == PAW2:
                            print("Booster 2 activated! Score quadrupled for this match.")
                            score_to_add = apply_score(points * 4)

                        else:
                            score_to_add = apply_score(points)

                        score += score_to_add
                        print(f"DEBUG: Score updated by {score_to_add}. New score: {score}")

                        selected_cat_pos = None
                        while handle_matches():
                            pass
                        pawboosters()
                        return
                    elif handle_booster_activation(row_target, col_target):
                        selected_cat_pos = None
                        return

                    selected_cat_pos = None
# Intialise la position du chaton sélectionné

selected_cat_pos = None
def resolve_matches():
    global catn
    matches = find_matches(catn)
    if not matches:
        return False #Pas de réunion de sang..."better luck next time!" comme disent les anglais (sauf l'exclamation, l'enthousiasme c'est pas anglais, c'est connu...)

    # Te voilà ma soeur! Nous devons disparaître à présent...
    for r, c in matches:
        catn[r][c] = None

    rows = len(catn)
    cols = len(catn[0])
    num_cat_types = 4

    #...pour laisser la place à nos descendants!
    for c in range(cols):
        column = [catn[r][c] for r in range(rows) if catn[r][c] is not None]
        empty_count = rows - len(column)
        new_cats = [random.randint(0, num_cat_types - 1) for _ in range(empty_count)]
        new_column = new_cats + column
        for r in range(rows):
            catn[r][c] = new_column[r]

    return True 
def menu():
    global game_state, fenetre

    fenetre.fill((100, 100, 200)) # Blue-ish background for menu

    # Title "KATTY KRUSH!"
    title_text = TITLE.render("KATTY KRUSH!", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(600 // 2, 600 // 2 - 100)) # Slightly above middle
    fenetre.blit(title_text, title_rect)

    # Start Button
    start_button_width = 200
    start_button_height = 60
    start_button_x = (600 - start_button_width) // 2
    start_button_y = 600 // 2 + 50 # Below the title
    start_button_rect = pygame.Rect(start_button_x, start_button_y, start_button_width, start_button_height)

    pygame.draw.rect(fenetre, (0, 200, 0), start_button_rect, border_radius=10) # Green button
    start_text = arial24.render("Start Game", True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    fenetre.blit(start_text, start_text_rect)
# On crée une nouvelle horloge qui nous permettra de fixer la vitesse de rafraichissement de notre fenêtre
clock = pygame.time.Clock()
continuer=1
while continuer==1:
    menu()
    generate_initial_grid(num_rows,num_cols,num_cat_types)
    has_initial_matches(catn)
    dessiner()
    gererClavierEtSouris()
    pawboosters()
    apply_score(score)
    find_matches(catn)
    resolve_matches()
    clock.tick(50)
pygame.quit()
sys.exit()