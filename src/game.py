#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classe principale du jeu qui gère les états du jeu et les transitions
"""

import pygame
from src.ui.main_menu import MainMenu
from src.ui.race_ui import RaceUI
from src.ui.career_ui import CareerUI
from src.player import Player
from src.career.career_path import CareerPath
from src.utils.save_load import save_game, load_game

class GameState:
    """Énumération des différents états du jeu"""
    MAIN_MENU = 0
    CAREER = 1
    RACE = 2
    RESULTS = 3
    QUIT = 4

class Game:
    """Classe principale du jeu qui gère les états et la boucle de jeu"""
    
    def __init__(self, screen, config):
        """
        Initialisation du jeu
        
        Args:
            screen (pygame.Surface): Surface d'affichage du jeu
            config (dict): Configuration du jeu
        """
        self.screen = screen
        self.config = config
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = GameState.MAIN_MENU
        
        # Composants du jeu
        self.player = None
        self.career = None
        
        # Interfaces utilisateur
        self.main_menu = MainMenu(self)
        self.race_ui = None
        self.career_ui = None
        
        # Chargement des ressources
        self.load_resources()
    
    def load_resources(self):
        """Chargement des ressources (images, sons, etc.)"""
        # À implémenter: chargement des ressources
        pass
    
    def new_game(self):
        """Démarrer une nouvelle partie"""
        self.player = Player("Nouveau Pilote", 16)  # Âge par défaut: 16 ans
        self.career = CareerPath(self.player)
        self.career_ui = CareerUI(self, self.player, self.career)
        self.current_state = GameState.CAREER
    
    def load_game(self):
        """Charger une partie sauvegardée"""
        loaded_data = load_game()
        if loaded_data:
            self.player = loaded_data.get('player')
            self.career = loaded_data.get('career')
            self.career_ui = CareerUI(self, self.player, self.career)
            self.current_state = GameState.CAREER
        else:
            # Échec du chargement, retour au menu principal
            self.current_state = GameState.MAIN_MENU
    
    def start_race(self, race):
        """
        Démarrer une course
        
        Args:
            race: Objet race à démarrer
        """
        self.race_ui = RaceUI(self, self.player, race)
        self.current_state = GameState.RACE
    
    def end_race(self, results):
        """
        Terminer une course
        
        Args:
            results: Résultats de la course
        """
        # Mise à jour des statistiques du joueur
        self.player.update_stats(results)
        
        # Retour à l'interface de carrière
        self.current_state = GameState.CAREER
    
    def save_game(self):
        """Sauvegarder la partie en cours"""
        save_data = {
            'player': self.player,
            'career': self.career
        }
        save_game(save_data)
    
    def quit_game(self):
        """Quitter le jeu"""
        self.running = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
        
        # Touche Échap pour retourner à l'écran précédent
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.current_state == GameState.RACE and hasattr(self.race_ui, 'race_finished') and self.race_ui.race_finished:
                    print("Retour à la carrière via touche Échap (dans Game)")
                    self.current_state = GameState.CAREER
                    continue
        
        # Délégation des événements à l'interface active
            if self.current_state == GameState.MAIN_MENU:
                self.main_menu.handle_event(event)
            elif self.current_state == GameState.CAREER:
                self.career_ui.handle_event(event)
            elif self.current_state == GameState.RACE:
                self.race_ui.handle_event(event)
    
    def update(self):
        """Mise à jour de l'état du jeu"""
        if self.current_state == GameState.MAIN_MENU:
            self.main_menu.update()
        elif self.current_state == GameState.CAREER:
            self.career_ui.update()
        elif self.current_state == GameState.RACE:
            self.race_ui.update()
    
    def render(self):
        """Rendu graphique du jeu"""
        self.screen.fill((0, 0, 0))  # Fond noir
        
        if self.current_state == GameState.MAIN_MENU:
            self.main_menu.render(self.screen)
        elif self.current_state == GameState.CAREER:
            self.career_ui.render(self.screen)
        elif self.current_state == GameState.RACE:
            self.race_ui.render(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.config['fps'])