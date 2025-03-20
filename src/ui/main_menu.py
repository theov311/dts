#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Menu principal du jeu
"""

import pygame
import os
from pygame import font, draw, Rect

# À mettre dans src/ui/main_menu.py
class Button:
    """Classe pour créer des boutons interactifs"""
    
    def __init__(self, text, x, y, width, height, action=None, bg_color=(100, 100, 100), hover_color=(150, 150, 150)):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def draw(self, surface):
        # Mise à jour de l'état de survol
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Fond du bouton
        pygame.draw.rect(surface, self.hover_color if self.is_hovered else self.bg_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (50, 50, 50), self.rect, 2, border_radius=10)  # Bordure
        
        # Texte du bouton
        button_font = pygame.font.SysFont('Arial', 24)
        text_surf = button_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        # Simplification : on ne vérifie que les clics
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    print(f"Bouton cliqué: {self.text}")
                    self.action()
                    return True
        return False

class MainMenu:
    """Classe pour le menu principal du jeu"""
    
    def __init__(self, game):
        """
        Initialise le menu principal
        
        Args:
            game: Instance principale du jeu
        """
        self.game = game
        self.screen_width = game.screen.get_width()
        self.screen_height = game.screen.get_height()
        
        # Charger les ressources
        self.load_resources()
        
        # Créer les boutons
        button_width = 250
        button_height = 60
        button_x = self.screen_width // 2 - button_width // 2
        button_spacing = 20
        
        start_y = self.screen_height // 2 - 50
        
        self.buttons = [
            Button("NOUVELLE CARRIÈRE", button_x, start_y, button_width, button_height, 
                  action=self.start_new_career, bg_color=(50, 100, 180), hover_color=(70, 130, 210)),
            Button("CHARGER PARTIE", button_x, start_y + button_height + button_spacing, button_width, button_height, 
                  action=self.load_game, bg_color=(50, 180, 100), hover_color=(70, 210, 130)),
            Button("OPTIONS", button_x, start_y + (button_height + button_spacing) * 2, button_width, button_height, 
                  action=self.show_options),
            Button("QUITTER", button_x, start_y + (button_height + button_spacing) * 3, button_width, button_height, 
                  action=self.game.quit_game, bg_color=(180, 50, 50), hover_color=(210, 70, 70))
        ]
    
    def load_resources(self):
        """Charge les ressources pour le menu"""
        # Charger les polices
        font.init()
        self.title_font = font.SysFont('Arial', 48, bold=True)
        self.subtitle_font = font.SysFont('Arial', 32)
        
        # Créer un arrière-plan en dégradé au lieu de charger une image
        self.background = pygame.Surface((self.screen_width, self.screen_height))
        
        # Créer un dégradé de haut en bas
        for y in range(self.screen_height):
            color_factor = y / self.screen_height
            r = int(10 + 20 * color_factor)
            g = int(10 + 50 * color_factor)
            b = int(50 + 70 * color_factor)
            pygame.draw.line(self.background, (r, g, b), (0, y), (self.screen_width, y))
    
    def update(self):
        """Met à jour l'état du menu"""
        pass
    
    def handle_event(self, event):
        """
        Gère les événements du menu
        
        Args:
            event (pygame.event.Event): Événement à gérer
        """
        for button in self.buttons:
            if button.handle_event(event):
                break
    
    def start_new_career(self):
        """Démarre une nouvelle carrière"""
        self.game.new_game()
    
    def load_game(self):
        """Charge une partie sauvegardée"""
        self.game.load_game()
    
    def show_options(self):
        """Affiche les options du jeu"""
        # À implémenter: affichage des options
        pass
    
    def render(self, surface):
        """
        Dessine le menu sur une surface
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Dessiner le fond
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill((30, 30, 80))  # Fond bleu foncé par défaut
        
        # Dessiner le titre
        title_surf = self.title_font.render("DRIVE TO SURVIVE", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, 100))
        surface.blit(title_surf, title_rect)
        
        # Dessiner le sous-titre
        subtitle_surf = self.subtitle_font.render("Carrière de Formule 1", True, (220, 220, 220))
        subtitle_rect = subtitle_surf.get_rect(center=(self.screen_width // 2, 150))
        surface.blit(subtitle_surf, subtitle_rect)
        
        # Dessiner les boutons
        for button in self.buttons:
            button.draw(surface)