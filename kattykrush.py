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
arial24 = pygame.font.SysFont("arial",24)
score=0
print(catn)

# Fonction en charge de dessiner tous les éléments sur notre fenêtre graphique principale.
# Cette fonction sera appelée depuis notre boucle infinie
def dessiner():
    global fenetre
    # On remplit complètement notre fenêtre un fond turquoise (parce que c'est GENIALLLL enft)
    # Ceci permet de 'nettoyer' notre fenêtre avant de la dessiner
    fenetre.fill( (132, 165, 157) )
    for j in range(len(catn)):
        for i in range(len(catn)):
            if catn[j][i] == 0:
                fenetre.blit(i1w,(25+i*150,25+j*150))
            if catn[j][i] == 1:
                fenetre.blit(i2t,(25+i*150,25+j*150))
            if catn[j][i] == 2:
                fenetre.blit(i3g,(25+i*150,25+j*150))
            if catn[j][i] == 3:
                fenetre.blit(i4b,(25+i*150,25+j*150))
    pygame.display.flip() # Rafraichissement complet de la fenêtre avec les dernières opérations de dessin

# Fonction en charge de gérer les évènements clavier (ou souris), et notamment les échanges de chats
# Cette fonction sera appelée depuis notre boucle infinie
def gererClavierEtSouris():
    global continuer, catn, selected_cat_pos
    def check_match(grid, r, c):
        rows = len(grid)
        cols = len(grid[0])
        cat_type = grid[r][c]
        if cat_type is None:
            return False

        # vérification horizontale
        count = 1
        for dc in [-1, 1]:
            for i in range(1, 3):
                cc = c + dc * i
                if 0 <= cc < cols and grid[r][cc] == cat_type:
                    count += 1
                else:
                    break
        if count >= 3:
            return True

        # Vérification verticale
        count = 1
        for dr in [-1, 1]:
            for i in range(1, 3):
                rr = r + dr * i
                if 0 <= rr < rows and grid[rr][c] == cat_type:
                    count += 1
                else:
                    break
        if count >= 3:
            return True
        return False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Clique gauche
            mous = pygame.mouse.get_pos()
            col = mous[0] // 150
            row = mous[1] // 150
            if 0 <= row < len(catn) and 0 <= col < len(catn[0]):
                selected_cat_pos = (row, col)
                print(f"mon petit chaton est à: {selected_cat_pos}")

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
                    # Test antérieur des échanges
                    temp_catn = [list(r) for r in catn]
                    temp_catn[row_orig][col_orig], temp_catn[row_target][col_target] = temp_catn[row_target][col_target], temp_catn[row_orig][col_orig]

                    # On vérifie si les chats ont des liens de parenté
                    if check_match(temp_catn, row_target, col_target):
                        print(f"Oh! notre chaton à peut-être trouver  {'right' if dc == 1 else 'left' if dc == -1 else 'down' if dr == 1 else 'up'}!")
                        catn[row_orig][col_orig], catn[row_target][col_target] = catn[row_target][col_target], catn[row_orig][col_orig]
                        selected_cat_pos = None
                        return

                    selected_cat_pos = None #On trouvera souvent cette variable qui permet de sortir de la boucle de vérification et de passer aux autres situations.
                if check_match(temp_catn, row_target, col_target):
                        print(f"Une fraternité trouvée {'à droite' if dc == 1 else 'à gauche' if dc == -1 else 'en bas' if dr == 1 else 'en haut'}!")
                        catn[row_orig][col_orig], catn[row_target][col_target] = catn[row_target][col_target], catn[row_orig][col_orig]
                        selected_cat_pos = None
                        # On rappelle la fonction antérieure pour pouvoir retirer les triplets une fois réunis pendant la partie
                        while resolve_matches():
                            pass
                        return

# Intialise la position du chaton sélectionné
selected_cat_pos = None
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
def resolve_matches():
    global catn
    matches = find_matches(catn)
    if not matches:
        return False #Pas de réunion de sang..."better luck next time!" comme disent les anglais (mais l'exclamation, l'enthousiasme c'est pas anglais c'est connu...)

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

# On crée une nouvelle horloge qui nous permettra de fixer la vitesse de rafraichissement de notre fenêtre
clock = pygame.time.Clock()
continuer=1
while continuer==1:
    generate_initial_grid(num_rows,num_cols,num_cat_types)
    has_initial_matches(catn)
    dessiner()
    gererClavierEtSouris()
    find_matches(catn)
    resolve_matches()
    clock.tick(50)
pygame.quit()
sys.exit()