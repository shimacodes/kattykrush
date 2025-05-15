import pygame
import sys
import random

pygame.init() # initialisation du module "pygame" 

fenetre = pygame.display.set_mode( (600,600) ) # Création d'une fenêtre graphique de taille 600x600 pixels
pygame.display.set_caption("Katty Krush!") # Définit le titre de la fenêtre


# Chargement des images:
#    On définit et affecte les variables qui contiendront les images des différents chats
i1w = pygame.image.load("cat blanc.png")
i2t = pygame.image.load("Head.png")
i3g = pygame.image.load("merida.png")
i4b= pygame.image.load("cat noir.png")


# On définit les variables qui contiendront les positions des différents éléments (vaisseau, alien, projectile)
# Chaque position est un couple de valeur '(x,y)'
catn = [[random.randint(0,3) for i in range(4)] for j in range(4)]
arial24 = pygame.font.SysFont("arial",24)
score=0

# Fonction en charge de dessiner tous les éléments sur notre fenêtre graphique.
# Cette fonction sera appelée depuis notre boucle infinie
def dessiner():
    global imageAlien, imageVaisseau, fenetre
    # On remplit complètement notre fenêtre avec la couleur noire: (0,0,0)
    # Ceci permet de 'nettoyer' notre fenêtre avant de la dessiner
    fenetre.fill( (0,0,0) )
    for i in catn:
        if i==0:
            fenetre.blit(i1w,(300,300))
        elif i==1:
            pass
        elif i==2:
            pass
        elif i==3:
            pass
    fenetre.blit(imageVaisseau, positionVaisseau) # On dessine l'image du vaisseau à sa position
    fenetre.blit(surfaceproj, (5,5))
    fenetre.blit(surfacescore, (500,5))
    pygame.display.flip() # Rafraichissement complet de la fenêtre avec les dernières opérations de dessin

