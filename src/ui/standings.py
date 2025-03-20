#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface de classements et statistiques
"""

import pygame
from pygame import font, draw, Rect, Surface

class StandingsUI:
    """Interface des classements et statistiques"""
    
    def __init__(self, screen_width, screen_height, season):
        """
        Initialisation de l'interface de classements
        
        Args:
            screen_width (int): Largeur de l'écran
            screen_height (int): Hauteur de l'écran
            season: Saison actuelle
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.season = season
        
        # Charger les polices
        font.init()
        self.title_font = font.SysFont('Arial', 36, bold=True)
        self.subtitle_font = font.SysFont('Arial', 24)
        self.entry_font = font.SysFont('Arial', 18)
        
        # Couleurs
        self.colors = {
            'background': (30, 30, 50),
            'text': (255, 255, 255),
            'highlight': (255, 220, 50),
            'panel': (40, 40, 60, 200),
            'header': (60, 60, 80),
            'row_even': (50, 50, 70, 200),
            'row_odd': (40, 40, 60, 200),
            'player': (255, 220, 50, 200)
        }
        
        # État de l'interface
        self.view_mode = 'drivers'  # 'drivers' ou 'teams'
        
        # Obtenir les classements actuels
        self.standings = self.season.get_current_standings()
    
    def update(self, season=None):
        """
        Met à jour les classements
        
        Args:
            season: Nouvelle saison (si changée)
        """
        if season:
            self.season = season
        
        # Mettre à jour les classements
        self.standings = self.season.get_current_standings()
    
    def toggle_view(self):
        """Bascule entre les classements pilotes et équipes"""
        self.view_mode = 'teams' if self.view_mode == 'drivers' else 'drivers'
    
    def render(self, surface):
        """
        Dessine l'interface sur une surface
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Fond
        surface.fill(self.colors['background'])
        
        # Titre
        if self.view_mode == 'drivers':
            title_text = self.title_font.render("CLASSEMENT DES PILOTES", True, self.colors['highlight'])
        else:
            title_text = self.title_font.render("CLASSEMENT DES ÉQUIPES", True, self.colors['highlight'])
        
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        surface.blit(title_text, title_rect)
        
        # Informations sur la saison
        season_text = self.subtitle_font.render(
            f"Saison {self.season.year} - Courses: {self.standings['races_completed']}/{self.standings['total_races']}",
            True, self.colors['text']
        )
        season_rect = season_text.get_rect(center=(self.screen_width // 2, 90))
        surface.blit(season_text, season_rect)
        
        # Afficher le classement approprié
        if self.view_mode == 'drivers':
            self._render_driver_standings(surface)
        else:
            self._render_team_standings(surface)
        
        # Bouton pour basculer la vue
        toggle_rect = Rect(self.screen_width - 150, 40, 130, 40)
        draw.rect(surface, (60, 60, 100), toggle_rect, border_radius=5)
        draw.rect(surface, (100, 100, 150), toggle_rect, 2, border_radius=5)
        
        toggle_text = self.entry_font.render("BASCULER", True, self.colors['text'])
        toggle_text_rect = toggle_text.get_rect(center=toggle_rect.center)
        surface.blit(toggle_text, toggle_text_rect)
    
    def _render_driver_standings(self, surface):
        """
        Dessine le classement des pilotes
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Tableau de classement
        table_width = 800
        table_height = 500
        table_x = self.screen_width // 2 - table_width // 2
        table_y = 150
        
        # En-tête du tableau
        header_height = 40
        header_rect = Rect(table_x, table_y, table_width, header_height)
        draw.rect(surface, self.colors['header'], header_rect)
        
        # Colonnes
        col_widths = [60, 300, 280, 160]  # Pos, Pilote, Équipe, Points
        col_x = [table_x]
        for i in range(len(col_widths) - 1):
            col_x.append(col_x[i] + col_widths[i])
        
        # Titres des colonnes
        headers = ["Pos", "Pilote", "Équipe", "Points"]
        for i, header in enumerate(headers):
            header_text = self.subtitle_font.render(header, True, self.colors['text'])
            header_rect = header_text.get_rect(midleft=(col_x[i] + 20, table_y + header_height // 2))
            surface.blit(header_text, header_rect)
        
        # Lignes du tableau (classement)
        row_height = 30
        drivers_standings = self.standings['driver_standings']
        
        for i, (driver_id, points) in enumerate(drivers_standings):
            row_y = table_y + header_height + i * row_height
            
            # Alterner les couleurs de ligne
            row_color = self.colors['row_even'] if i % 2 == 0 else self.colors['row_odd']
            
            # Surbrillance pour le joueur
            if driver_id == 'player':
                row_color = self.colors['player']
            
            row_rect = Rect(table_x, row_y, table_width, row_height)
            draw.rect(surface, row_color, row_rect)
            
            # Position
            pos_text = self.entry_font.render(str(i + 1), True, self.colors['text'])
            pos_rect = pos_text.get_rect(midleft=(col_x[0] + 20, row_y + row_height // 2))
            surface.blit(pos_text, pos_rect)
            
            # Nom du pilote
            driver_info = self.season.drivers.get(driver_id, {})
            driver_name = driver_info.get('name', 'Inconnu')
            if driver_id == 'player':
                driver_name += " (Vous)"
            
            driver_text = self.entry_font.render(driver_name, True, self.colors['text'])
            driver_rect = driver_text.get_rect(midleft=(col_x[1] + 20, row_y + row_height // 2))
            surface.blit(driver_text, driver_rect)
            
            # Équipe
            team_name = driver_info.get('team', 'Inconnue')
            team_text = self.entry_font.render(team_name, True, self.colors['text'])
            team_rect = team_text.get_rect(midleft=(col_x[2] + 20, row_y + row_height // 2))
            surface.blit(team_text, team_rect)
            
            # Points
            points_text = self.entry_font.render(f"{points:.1f}", True, self.colors['text'])
            points_rect = points_text.get_rect(midleft=(col_x[3] + 20, row_y + row_height // 2))
            surface.blit(points_text, points_rect)
    
    def _render_team_standings(self, surface):
        """
        Dessine le classement des équipes
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Tableau de classement
        table_width = 600
        table_height = 500
        table_x = self.screen_width // 2 - table_width // 2
        table_y = 150
        
        # En-tête du tableau
        header_height = 40
        header_rect = Rect(table_x, table_y, table_width, header_height)
        draw.rect(surface, self.colors['header'], header_rect)
        
        # Colonnes
        col_widths = [60, 380, 160]  # Pos, Équipe, Points
        col_x = [table_x]
        for i in range(len(col_widths) - 1):
            col_x.append(col_x[i] + col_widths[i])
        
        # Titres des colonnes
        headers = ["Pos", "Équipe", "Points"]
        for i, header in enumerate(headers):
            header_text = self.subtitle_font.render(header, True, self.colors['text'])
            header_rect = header_text.get_rect(midleft=(col_x[i] + 20, table_y + header_height // 2))
            surface.blit(header_text, header_rect)
        
        # Lignes du tableau (classement)
        row_height = 30
        team_standings = self.standings['team_standings']
        player_team = self.season.drivers['player']['team']
        
        for i, (team_name, points) in enumerate(team_standings):
            row_y = table_y + header_height + i * row_height
            
            # Alterner les couleurs de ligne
            row_color = self.colors['row_even'] if i % 2 == 0 else self.colors['row_odd']
            
            # Surbrillance pour l'équipe du joueur
            if team_name == player_team:
                row_color = self.colors['player']
            
            row_rect = Rect(table_x, row_y, table_width, row_height)
            draw.rect(surface, row_color, row_rect)
            
            # Position
            pos_text = self.entry_font.render(str(i + 1), True, self.colors['text'])
            pos_rect = pos_text.get_rect(midleft=(col_x[0] + 20, row_y + row_height // 2))
            surface.blit(pos_text, pos_rect)
            
            # Nom de l'équipe
            team_text = self.entry_font.render(team_name, True, self.colors['text'])
            team_rect = team_text.get_rect(midleft=(col_x[1] + 20, row_y + row_height // 2))
            surface.blit(team_text, team_rect)
            
            # Points
            points_text = self.entry_font.render(f"{points:.1f}", True, self.colors['text'])
            points_rect = points_text.get_rect(midleft=(col_x[2] + 20, row_y + row_height // 2))
            surface.blit(points_text, points_rect)
    
    def handle_event(self, event):
        """
        Gère les événements de l'interface
        
        Args:
            event (pygame.event.Event): Événement à gérer
            
        Returns:
            bool: True si l'événement a été traité
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Clic sur le bouton de basculement
            toggle_rect = Rect(self.screen_width - 150, 40, 130, 40)
            if toggle_rect.collidepoint(event.pos):
                self.toggle_view()
                return True
        
        return False