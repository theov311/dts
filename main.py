#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Drive to Survive - Un jeu de carrière de Formule 1
Point d'entrée principal du jeu
"""

import sys
import os
import pygame
from src.game import Game
from src.utils.config import load_config

def main():
    """Fonction principale du jeu"""
    
    # Initialisation de pygame
    pygame.init()
    pygame.display.set_caption("Drive to Survive")
    
    # Chargement de la configuration
    config = load_config()
    
    # Création de la fenêtre du jeu
    screen = pygame.display.set_mode((config['screen_width'], config['screen_height']))
    
    # Initialisation du jeu
    game = Game(screen, config)
    
    # Boucle principale du jeu
    game.run()
    
    # Nettoyage à la fin du jeu
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()