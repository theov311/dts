#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface utilisateur pour la gestion de la carrière
"""

import pygame
from pygame import font, draw, Rect, Surface
from src.ui.main_menu import Button

class AcademySelection:
    """Interface de sélection d'académie"""
    
    def __init__(self, career_ui, academies):
        """
        Initialisation de l'interface de sélection d'académie
        
        Args:
            career_ui: Interface de carrière parente
            academies (list): Liste des académies disponibles
        """
        self.career_ui = career_ui
        self.academies = academies
        self.selected_academy = None
        
        # Créer les boutons pour chaque académie
        self.academy_buttons = []
        self._create_academy_buttons()
    
    def _create_academy_buttons(self):
        """Crée les boutons pour chaque académie"""
        screen_width = self.career_ui.screen_width
        button_width = 400
        button_height = 60
        button_x = screen_width // 2 - button_width // 2
        button_spacing = 20
        
        start_y = 200
        
        for i, academy in enumerate(self.academies):
            button_y = start_y + (button_height + button_spacing) * i
            
            def create_academy_handler(academy):
                return lambda: self.select_academy(academy)
            
            # Couleurs personnalisées pour chaque académie
            colors = {
                "Ferrari Driver Academy": ((180, 0, 0), (220, 30, 30)),
                "Mercedes Junior Team": ((0, 180, 180), (30, 220, 220)),
                "Red Bull Junior Team": ((0, 0, 180), (30, 30, 220)),
                "Alpine Academy": ((0, 0, 100), (30, 30, 150)),
                "McLaren Driver Development": ((255, 135, 0), (255, 165, 30))
            }
            
            bg_color = colors.get(academy.name, ((100, 100, 100), (150, 150, 150)))[0]
            hover_color = colors.get(academy.name, ((100, 100, 100), (150, 150, 150)))[1]
            
            # Créer le bouton
            button = Button(
                academy.name,
                button_x,
                button_y,
                button_width,
                button_height,
                action=create_academy_handler(academy),
                bg_color=bg_color,
                hover_color=hover_color
            )
            
            self.academy_buttons.append(button)
    
    def select_academy(self, academy):
        """
        Sélectionne une académie
        
        Args:
            academy: Académie sélectionnée
        """
        self.selected_academy = academy
        self.career_ui.start_career_with_academy(academy)
    
    def handle_event(self, event):
        """
        Gère les événements de l'interface
        
        Args:
            event (pygame.event.Event): Événement à gérer
        """
        for button in self.academy_buttons:
            if button.handle_event(event):
                return True
        return False
    
    def render(self, surface):
        """
        Dessine l'interface sur une surface
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Fond
        surface.fill((30, 30, 50))
        
        # Titre
        title_font = self.career_ui.title_font
        title_text = title_font.render("CHOISISSEZ VOTRE ACADÉMIE DE PILOTES", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.career_ui.screen_width // 2, 100))
        surface.blit(title_text, title_rect)
        
        # Description
        info_font = self.career_ui.info_font
        info_text = info_font.render("Votre académie sera votre point d'entrée dans le monde de la course", True, (220, 220, 220))
        info_rect = info_text.get_rect(center=(self.career_ui.screen_width // 2, 150))
        surface.blit(info_text, info_rect)
        
        # Boutons des académies
        for button in self.academy_buttons:
            button.draw(surface)


# Modifiez la méthode handle_event dans la classe CareerUI
def handle_event(self, event):
    """
    Gère les événements de l'interface
    
    Args:
        event (pygame.event.Event): Événement à gérer
    """
    if self.current_state == self.STATES['select_academy']:
        if self.academy_selection:
            self.academy_selection.handle_event(event)
    elif self.current_state == self.STATES['race_selection']:
        # Gérer le bouton retour
        if hasattr(self, 'back_button'):
            if self.back_button.handle_event(event):
                return True
        
        # Gérer les boutons de course
        for button in self.race_buttons:
            if button.handle_event(event):
                break
    elif self.current_state == self.STATES['season_overview']:
        # Gérer les boutons d'action
        for button in self.action_buttons:
            if button.handle_event(event):
                break
    elif self.current_state == self.STATES['end_season']:
        # Bouton continuer
        for button in self.action_buttons:
            if button.handle_event(event):
                break
    elif self.current_state == self.STATES['stats']:
        # Gérer le bouton retour si présent
        if hasattr(self, 'back_button'):
            if self.back_button.handle_event(event):
                return True

class CareerUI:
    """Interface principale de gestion de carrière"""
    
    def __init__(self, game, player, career):
        """
        Initialisation de l'interface de carrière
        
        Args:
            game: Instance principale du jeu
            player: Joueur
            career: Instance de la carrière
        """
        self.game = game
        self.player = player
        self.career = career
        
        # Dimensions de l'écran
        self.screen_width = game.screen.get_width()
        self.screen_height = game.screen.get_height()
        
        # Charger les polices
        font.init()
        self.title_font = font.SysFont('Arial', 36, bold=True)
        self.info_font = font.SysFont('Arial', 24)
        self.status_font = font.SysFont('Arial', 18)
        
        # Couleurs
        self.colors = {
            'background': (20, 20, 40),
            'text': (255, 255, 255),
            'highlight': (255, 220, 50),
            'button': (50, 100, 180),
            'button_hover': (70, 130, 210),
            'warning': (220, 50, 50),
            'success': (50, 180, 50),
            'info': (50, 150, 220)
        }
        
        # États possibles de l'interface
        self.STATES = {
            'select_academy': 0,
            'season_overview': 1,
            'race_selection': 2,
            'contract_negotiation': 3,
            'end_season': 4,
            'promotion': 5,
            'stats': 6
        }
        
        # État actuel
        self.current_state = self.STATES['select_academy']
        
        # Sous-interfaces
        self.academy_selection = None
        
        # Boutons d'action
        self.action_buttons = []
        
        # Boutons pour les courses
        self.race_buttons = []
        
        # Initialisation
        self._init_ui()
    
    def _init_ui(self):
        """Initialise l'interface"""
        # Si le joueur a déjà une académie, aller directement à la vue de saison
        if self.player.academy:
            self.current_state = self.STATES['season_overview']
            # Démarrer une nouvelle saison si nécessaire
            if not self.career.current_season:
                self.career.start_new_season()
        else:
            # Interface de sélection d'académie
            self.academy_selection = AcademySelection(self, self.career.academies)
    
    def start_career_with_academy(self, academy):
        """
        Démarre la carrière avec l'académie sélectionnée
        
        Args:
            academy: Académie sélectionnée
        """
        self.career.start_career(academy)
        self.current_state = self.STATES['season_overview']
        self._update_race_buttons()
    
    def _update_race_buttons(self):
        """Met à jour les boutons de course selon le calendrier actuel"""
        self.race_buttons = []
        
        if not self.career.current_season:
            return
        
        # Récupérer le calendrier des courses
        calendar = self.career.current_season.race_calendar
        
        # Position et dimensions des boutons
        button_width = 250
        button_height = 40
        button_x = self.screen_width // 2 - button_width // 2
        button_spacing = 15
        
        # Nombre maximum de boutons par colonne
        max_buttons_per_column = 8
        columns = (len(calendar) // max_buttons_per_column) + 1
        
        for i, race in enumerate(calendar):
            # Déterminer la colonne et la position
            column = i // max_buttons_per_column
            row = i % max_buttons_per_column
            
            column_width = button_width + 50
            start_x = button_x - (column_width * (columns - 1) // 2) + (column * column_width)
            button_y = 180 + (button_height + button_spacing) * row
            
            # Ne pas créer de bouton si la course est déjà terminée
            if race['completed']:
                continue
            
            def create_race_handler(race_index):
                return lambda: self.start_race(race_index)
            
            # Créer le bouton
            button = Button(
                f"{race['name']} - {race['date']}",
                start_x,
                button_y,
                button_width,
                button_height,
                action=create_race_handler(i),
                bg_color=self.colors['button'],
                hover_color=self.colors['button_hover']
            )
            
            self.race_buttons.append(button)
    
    def start_race(self, race_index):
        """
        Démarre une course
        
        Args:
            race_index (int): Index de la course dans le calendrier
        """
        # Récupérer la course
        race_info = self.career.current_season.get_next_race()
        
        if race_info and 'race_obj' in race_info:
            # Démarrer la course
            self.game.start_race(race_info['race_obj'])
    
    def handle_event(self, event):
        """
        Gère les événements de l'interface
        
        Args:
            event (pygame.event.Event): Événement à gérer
        """
        if self.current_state == self.STATES['select_academy']:
            self.academy_selection.handle_event(event)
        elif self.current_state == self.STATES['race_selection']:
            for button in self.race_buttons:
                if button.handle_event(event):
                    break
        elif self.current_state == self.STATES['season_overview']:
            # Gérer les boutons d'action
            for button in self.action_buttons:
                if button.handle_event(event):
                    break
        elif self.current_state == self.STATES['end_season']:
            # Bouton continuer
            for button in self.action_buttons:
                if button.handle_event(event):
                    break
    
    def update(self):
        """Met à jour l'état de l'interface"""
        # Mise à jour du calendrier des courses si besoin
        if self.current_state == self.STATES['race_selection'] and not self.race_buttons:
            self._update_race_buttons()
        
        # Vérifier si toutes les courses sont terminées
        if self.career.current_season and self.career.current_season.current_race_index >= len(self.career.current_season.race_calendar):
            # Terminer la saison
            self.current_state = self.STATES['end_season']
            self._show_season_results()
    
    def _show_season_results(self):
        """Affiche les résultats de fin de saison"""
        # Récupérer les résultats
        self.season_results = self.career.end_season()
        
        # Créer un bouton pour continuer
        button_width = 250
        button_height = 50
        button_x = self.screen_width // 2 - button_width // 2
        button_y = self.screen_height - 100
        
        # Vider les boutons existants
        self.action_buttons = []
        
        # Ajouter le bouton pour continuer
        continue_button = Button(
            "CONTINUER",
            button_x,
            button_y,
            button_width,
            button_height,
            action=self._handle_season_end,
            bg_color=self.colors['success'],
            hover_color=(80, 210, 80)
        )
        
        self.action_buttons.append(continue_button)
    
    def _handle_season_end(self):
        """Gère la fin de saison et la progression de carrière"""
        # Vérifier si une promotion est possible
        if self.season_results.get('promotion_available', False):
            self.current_state = self.STATES['promotion']
            self._show_promotion_screen()
        else:
            # Vérifier s'il y a des offres de contrat
            if self.player.contract_years <= 0 and self.season_results.get('new_contracts', []):
                self.current_state = self.STATES['contract_negotiation']
                self._show_contract_offers()
            else:
                # Nouvelle saison
                self.career.start_new_season()
                self.current_state = self.STATES['season_overview']
    
    def _show_promotion_screen(self):
        """Affiche l'écran de promotion"""
        # Vider les boutons existants
        self.action_buttons = []
        
        # Position et dimensions des boutons
        button_width = 300
        button_height = 60
        button_x = self.screen_width // 2 - button_width // 2
        button_spacing = 30
        
        # Bouton pour accepter la promotion
        promote_button = Button(
            "ACCEPTER LA PROMOTION",
            button_x,
            self.screen_height // 2,
            button_width,
            button_height,
            action=self._accept_promotion,
            bg_color=self.colors['success'],
            hover_color=(80, 210, 80)
        )
        
        # Bouton pour rester dans la catégorie actuelle
        stay_button = Button(
            "RESTER EN " + self.player.category.upper(),
            button_x,
            self.screen_height // 2 + button_height + button_spacing,
            button_width,
            button_height,
            action=self._decline_promotion,
            bg_color=self.colors['warning'],
            hover_color=(250, 80, 80)
        )
        
        self.action_buttons.append(promote_button)
        self.action_buttons.append(stay_button)
    
    def _accept_promotion(self):
        """Accepte la promotion à la catégorie supérieure"""
        # Promouvoir le joueur
        new_category = self.career.promote_player()
        
        # Vérifier les offres de contrat
        if self.player.contract_years <= 0 or self.player.team.category != new_category:
            self.current_state = self.STATES['contract_negotiation']
            self._show_contract_offers()
        else:
            # Nouvelle saison
            self.career.start_new_season()
            self.current_state = self.STATES['season_overview']
    
    def _decline_promotion(self):
        """Refuse la promotion et reste dans la catégorie actuelle"""
        # Vérifier s'il y a des offres de contrat
        if self.player.contract_years <= 0:
            self.current_state = self.STATES['contract_negotiation']
            self._show_contract_offers()
        else:
            # Nouvelle saison
            self.career.start_new_season()
            self.current_state = self.STATES['season_overview']
    
    def _show_contract_offers(self):
        """Affiche les offres de contrat disponibles"""
        # Récupérer les offres de contrat
        self.contract_offers = self.season_results.get('new_contracts', [])
        
        # Vider les boutons existants
        self.action_buttons = []
        
        # Position et dimensions des boutons
        button_width = 350
        button_height = 50
        button_x = self.screen_width // 2 - button_width // 2
        button_spacing = 20
        
        start_y = 250
        
        for i, offer in enumerate(self.contract_offers):
            team_name = offer['team'].name
            years = offer['years']
            value = offer['value']
            
            button_y = start_y + (button_height + button_spacing) * i
            
            def create_offer_handler(offer):
                return lambda: self._accept_contract(offer)
            
            # Couleur selon l'équipe
            team_colors = {
                "Scuderia Ferrari": ((180, 0, 0), (220, 30, 30)),
                "Mercedes-AMG Petronas": ((0, 180, 180), (30, 220, 220)),
                "Red Bull Racing": ((0, 0, 180), (30, 30, 220)),
                "BWT Alpine F1 Team": ((0, 0, 100), (30, 30, 150)),
                "McLaren F1 Team": ((255, 135, 0), (255, 165, 30))
            }
            
            bg_color = team_colors.get(team_name, (self.colors['button'], self.colors['button_hover']))[0]
            hover_color = team_colors.get(team_name, (self.colors['button'], self.colors['button_hover']))[1]
            
            # Créer le bouton
            button_text = f"{team_name} - {years} an(s) - {value:,.0f} €"
            button = Button(
                button_text,
                button_x,
                button_y,
                button_width,
                button_height,
                action=create_offer_handler(offer),
                bg_color=bg_color,
                hover_color=hover_color
            )
            
            self.action_buttons.append(button)
    
    def _accept_contract(self, offer):
        """
        Accepte une offre de contrat
        
        Args:
            offer (dict): Offre de contrat
        """
        # Signer le contrat
        self.career.sign_new_contract(offer)
        
        # Démarrer une nouvelle saison
        self.career.start_new_season()
        self.current_state = self.STATES['season_overview']
    
    def show_race_selection(self):
        """Affiche l'écran de sélection de course"""
        self.current_state = self.STATES['race_selection']
        self._update_race_buttons()
    
    def show_stats(self):
        """Affiche les statistiques du joueur"""
        self.current_state = self.STATES['stats']
    
    def show_standings(self):
        """Affiche les classements actuels"""
        # Rester dans l'aperçu de saison mais mettre à jour les classements
        pass
    
    def _create_action_buttons(self):
        """Crée les boutons d'action pour l'aperçu de saison"""
        # Vider les boutons existants
        self.action_buttons = []
        
        # Position et dimensions des boutons
        button_width = 250
        button_height = 50
        button_x = self.screen_width // 2 - button_width // 2
        button_spacing = 20
        
        start_y = self.screen_height - 250
        
        # Bouton pour les courses
        race_button = Button(
            "COURSES",
            button_x,
            start_y,
            button_width,
            button_height,
            action=self.show_race_selection,
            bg_color=self.colors['button'],
            hover_color=self.colors['button_hover']
        )
        
        # Bouton pour les stats
        stats_button = Button(
            "STATISTIQUES",
            button_x,
            start_y + button_height + button_spacing,
            button_width,
            button_height,
            action=self.show_stats,
            bg_color=self.colors['info'],
            hover_color=(80, 180, 250)
        )
        
        # Bouton pour les classements
        standings_button = Button(
            "CLASSEMENTS",
            button_x,
            start_y + (button_height + button_spacing) * 2,
            button_width,
            button_height,
            action=self.show_standings,
            bg_color=self.colors['success'],
            hover_color=(80, 210, 80)
        )
        
        self.action_buttons.append(race_button)
        self.action_buttons.append(stats_button)
        self.action_buttons.append(standings_button)
    
    def render(self, surface):
        """
        Dessine l'interface sur une surface
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Fond
        surface.fill(self.colors['background'])
        
        # Affichage selon l'état
        if self.current_state == self.STATES['select_academy']:
            self.academy_selection.render(surface)
        elif self.current_state == self.STATES['season_overview']:
            self._render_season_overview(surface)
        elif self.current_state == self.STATES['race_selection']:
            self._render_race_selection(surface)
        elif self.current_state == self.STATES['stats']:
            self._render_stats(surface)
        elif self.current_state == self.STATES['end_season']:
            self._render_season_results(surface)
        elif self.current_state == self.STATES['promotion']:
            self._render_promotion_screen(surface)
        elif self.current_state == self.STATES['contract_negotiation']:
            self._render_contract_offers(surface)
    
    def _render_season_overview(self, surface):
        """
        Dessine l'aperçu de la saison
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Titre
        title_text = self.title_font.render("APERÇU DE LA SAISON", True, self.colors['highlight'])
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        surface.blit(title_text, title_rect)
        
        # Informations sur le joueur
        player_rect = Rect(20, 100, 400, 200)
        player_surface = Surface((player_rect.width, player_rect.height), pygame.SRCALPHA)
        player_surface.fill((0, 0, 0, 180))  # Fond semi-transparent
        
        # Nom et âge
        name_text = self.info_font.render(f"{self.player.name}, {self.player.age} ans", True, self.colors['text'])
        player_surface.blit(name_text, (20, 20))
        
        # Catégorie
        category_names = {
            'f3': 'Formule 3',
            'f2': 'Formule 2',
            'f1': 'Formule 1'
        }
        category_text = self.info_font.render(f"Catégorie: {category_names.get(self.player.category, self.player.category)}", True, self.colors['text'])
        player_surface.blit(category_text, (20, 50))
        
        # Équipe
        team_name = self.player.team.name if self.player.team else "Aucune équipe"
        team_text = self.info_font.render(f"Équipe: {team_name}", True, self.colors['text'])
        player_surface.blit(team_text, (20, 80))
        
        # Académie
        academy_name = self.player.academy.name if self.player.academy else "Académie indépendante"
        academy_text = self.info_font.render(f"Académie: {academy_name}", True, self.colors['text'])
        player_surface.blit(academy_text, (20, 110))
        
        # Contrat
        contract_text = self.info_font.render(f"Contrat: {self.player.contract_years} an(s) restant(s)", True, self.colors['text'])
        player_surface.blit(contract_text, (20, 140))
        
        # Niveau global
        overall_text = self.info_font.render(f"Niveau global: {self.player.skills.overall:.1f}", True, self.colors['highlight'])
        player_surface.blit(overall_text, (20, 170))
        
        surface.blit(player_surface, player_rect)
        
        # Informations sur la saison
        if self.career.current_season:
            season_rect = Rect(self.screen_width - 420, 100, 400, 200)
            season_surface = Surface((season_rect.width, season_rect.height), pygame.SRCALPHA)
            season_surface.fill((0, 0, 0, 180))  # Fond semi-transparent
            
            # Année et catégorie
            season_text = self.info_font.render(f"Saison {self.career.current_season.year} - {category_names.get(self.career.current_season.category, self.career.current_season.category)}", True, self.colors['highlight'])
            season_surface.blit(season_text, (20, 20))
            
            # Progression
            races_completed = self.career.current_season.current_race_index
            total_races = len(self.career.current_season.race_calendar)
            progress_text = self.info_font.render(f"Progression: {races_completed}/{total_races} courses", True, self.colors['text'])
            season_surface.blit(progress_text, (20, 50))
            
            # Classements actuels
            standings = self.career.current_season.get_current_standings()
            position_text = self.info_font.render(f"Position actuelle: {standings['player_position']}", True, self.colors['text'])
            season_surface.blit(position_text, (20, 80))
            
            points_text = self.info_font.render(f"Points: {standings['player_points']}", True, self.colors['text'])
            season_surface.blit(points_text, (20, 110))
            
            team_position_text = self.info_font.render(f"Position équipe: {standings['team_position']}", True, self.colors['text'])
            season_surface.blit(team_position_text, (20, 140))
            
            # Prochaine course
            next_race = self.career.current_season.get_next_race()
            if next_race:
                next_race_text = self.info_font.render(f"Prochaine course: {next_race['name']}", True, self.colors['text'])
                season_surface.blit(next_race_text, (20, 170))
            
            surface.blit(season_surface, season_rect)
        
        # Création des boutons d'action si besoin
        if not self.action_buttons:
            self._create_action_buttons()
        
        # Affichage des boutons
        for button in self.action_buttons:
            button.draw(surface)
    
    def _render_race_selection(self, surface):
        """
        Dessine l'écran de sélection de course
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Titre
        title_text = self.title_font.render("SÉLECTION DE COURSE", True, self.colors['highlight'])
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        surface.blit(title_text, title_rect)
        
        # Sous-titre
        subtitle_text = self.info_font.render("Sélectionnez une course pour continuer", True, self.colors['text'])
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 100))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Affichage des boutons de course
        for button in self.race_buttons:
            button.draw(surface)
        
        # Bouton retour
        back_button = Button(
            "RETOUR",
            20,
            self.screen_height - 70,
            120,
            50,
            action=lambda: setattr(self, 'current_state', self.STATES['season_overview']),
            bg_color=self.colors['warning'],
            hover_color=(250, 80, 80)
        )
        
        back_button.draw(surface)
        # Stocker le bouton retour pour la gestion des événements
        self.back_button = back_button
    def _set_current_state(self, state):
        print(f"Changement d'état: {self.current_state} -> {state}")
        self.current_state = state

    def _render_stats(self, surface):
        """
        Dessine l'écran des statistiques
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Titre
        title_text = self.title_font.render("STATISTIQUES DU PILOTE", True, self.colors['highlight'])
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        surface.blit(title_text, title_rect)
        
        # Nom du pilote
        name_text = self.info_font.render(self.player.name, True, self.colors['text'])
        name_rect = name_text.get_rect(center=(self.screen_width // 2, 100))
        surface.blit(name_text, name_rect)
        
        # Compétences
        skills_rect = Rect(50, 150, 400, 300)
        skills_surface = Surface((skills_rect.width, skills_rect.height), pygame.SRCALPHA)
        skills_surface.fill((0, 0, 0, 180))  # Fond semi-transparent
        
        # Titre
        skills_title = self.info_font.render("COMPÉTENCES", True, self.colors['highlight'])
        skills_surface.blit(skills_title, (20, 20))
        
        # Liste des compétences
        skills = [
            ("Vitesse pure", self.player.skills.pace),
            ("Dépassement", self.player.skills.overtaking),
            ("Défense", self.player.skills.defending),
            ("Régularité", self.player.skills.consistency),
            ("Gestion des pneus", self.player.skills.tire_management),
            ("Pilotage sous la pluie", self.player.skills.wet_driving),
            ("Feedback technique", self.player.skills.technical_feedback),
            ("Départs", self.player.skills.starts),
            ("Niveau global", self.player.skills.overall)
        ]
        
        y_offset = 60
        for name, value in skills:
            # Texte de la compétence
            skill_text = self.status_font.render(name, True, self.colors['text'])
            skills_surface.blit(skill_text, (20, y_offset))
            
            # Valeur
            value_text = self.status_font.render(f"{value:.1f}", True, self.colors['highlight'])
            skills_surface.blit(value_text, (skills_rect.width - 70, y_offset))
            
            # Barre de progression
            bar_rect = Rect(150, y_offset + 7, 150, 10)
            draw.rect(skills_surface, (100, 100, 100), bar_rect)  # Fond de la barre
            
            # Remplissage selon la valeur
            fill_width = int(bar_rect.width * value / 100)
            fill_rect = Rect(bar_rect.left, bar_rect.top, fill_width, bar_rect.height)
            
            # Couleur selon la valeur
            if value >= 80:
                color = (50, 205, 50)  # Vert
            elif value >= 60:
                color = (220, 220, 0)  # Jaune
            elif value >= 40:
                color = (255, 165, 0)  # Orange
            else:
                color = (255, 0, 0)  # Rouge
            
            draw.rect(skills_surface, color, fill_rect)
            
            y_offset += 25
        
        surface.blit(skills_surface, skills_rect)
        
        # Statistiques de carrière
        stats_rect = Rect(self.screen_width - 450, 150, 400, 300)
        stats_surface = Surface((stats_rect.width, stats_rect.height), pygame.SRCALPHA)
        stats_surface.fill((0, 0, 0, 180))  # Fond semi-transparent
        
        # Titre
        stats_title = self.info_font.render("STATISTIQUES DE CARRIÈRE", True, self.colors['highlight'])
        stats_surface.blit(stats_title, (20, 20))
        
        # Liste des statistiques
        stats_items = [
            ("Courses disputées", self.player.stats.races),
            ("Victoires", self.player.stats.wins),
            ("Podiums", self.player.stats.podiums),
            ("Points", self.player.stats.points),
            ("Championnats", self.player.stats.championships),
            ("Meilleur résultat", f"{self.player.stats.best_finish}ème place"),
            ("", ""),
            ("F3 - Victoires", self.player.stats.f3_stats['wins']),
            ("F2 - Victoires", self.player.stats.f2_stats['wins']),
            ("F1 - Victoires", self.player.stats.f1_stats['wins'])
        ]
        
        y_offset = 60
        for name, value in stats_items:
            if name:  # Ignorer les lignes vides
                # Texte de la statistique
                stat_text = self.status_font.render(name, True, self.colors['text'])
                stats_surface.blit(stat_text, (20, y_offset))
                
                # Valeur
                value_text = self.status_font.render(str(value), True, self.colors['highlight'])
                stats_surface.blit(value_text, (stats_rect.width - 70, y_offset))
            
            y_offset += 25
        
        surface.blit(stats_surface, stats_rect)
        
        # Bouton retour
        back_button = Button(
            "RETOUR",
            20,
            self.screen_height - 70,
            120,
            50,
            action=lambda: setattr(self, 'current_state', self.STATES['season_overview']),
            bg_color=self.colors['warning'],
            hover_color=(250, 80, 80)
        )
        
        back_button.draw(surface)
    
    def _render_season_results(self, surface):
        """
        Dessine les résultats de fin de saison
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Titre
        title_text = self.title_font.render("FIN DE SAISON", True, self.colors['highlight'])
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        surface.blit(title_text, title_rect)
        
        # Panneau de résultats
        results_width = 600
        results_height = 400
        results_x = self.screen_width // 2 - results_width // 2
        results_y = 100
        
        results_surface = Surface((results_width, results_height), pygame.SRCALPHA)
        results_surface.fill((30, 30, 80, 255))
        draw.rect(results_surface, self.colors['highlight'], (0, 0, results_width, results_height), 2)
        
        # Année et catégorie
        category_names = {
            'f3': 'Formule 3',
            'f2': 'Formule 2',
            'f1': 'Formule 1'
        }
        category_name = category_names.get(self.season_results['category'], self.season_results['category'])
        season_text = self.info_font.render(f"Saison {self.season_results['year']} - {category_name}", True, self.colors['highlight'])
        season_rect = season_text.get_rect(center=(results_width // 2, 40))
        results_surface.blit(season_text, season_rect)
        
        # Position finale
        position = self.season_results['position']
        position_color = self.colors['success'] if position <= 3 else self.colors['text']
        position_text = self.title_font.render(f"Position finale: {position}", True, position_color)
        position_rect = position_text.get_rect(center=(results_width // 2, 100))
        results_surface.blit(position_text, position_rect)
        
        # Points
        points = self.season_results['points']
        points_text = self.info_font.render(f"Points marqués: {points}", True, self.colors['text'])
        points_rect = points_text.get_rect(center=(results_width // 2, 150))
        results_surface.blit(points_text, points_rect)
        
        # Champion
        champion = self.season_results.get('champion', "")
        if champion:
            champion_text = self.info_font.render(f"Champion: {champion}", True, self.colors['highlight'])
            champion_rect = champion_text.get_rect(center=(results_width // 2, 190))
            results_surface.blit(champion_text, champion_rect)
        
        # Équipe championne
        team_champion = self.season_results.get('team_champion', "")
        if team_champion:
            team_text = self.info_font.render(f"Équipe championne: {team_champion}", True, self.colors['highlight'])
            team_rect = team_text.get_rect(center=(results_width // 2, 230))
            results_surface.blit(team_text, team_rect)
        
        # Message de promotion
        if self.season_results.get('promotion_available', False):
            promo_text = self.info_font.render("Vous êtes éligible pour une promotion!", True, self.colors['success'])
            promo_rect = promo_text.get_rect(center=(results_width // 2, 280))
            results_surface.blit(promo_text, promo_rect)
        
        # Message de fin de contrat
        if self.player.contract_years <= 0:
            contract_text = self.info_font.render("Votre contrat est terminé. De nouvelles offres sont disponibles.", True, self.colors['warning'])
            contract_rect = contract_text.get_rect(center=(results_width // 2, 320))
            results_surface.blit(contract_text, contract_rect)
        
        surface.blit(results_surface, (results_x, results_y))
        
        # Affichage des boutons
        for button in self.action_buttons:
            button.draw(surface)
    
    def _render_promotion_screen(self, surface):
        """
        Dessine l'écran de promotion
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Titre
        title_text = self.title_font.render("PROMOTION DISPONIBLE", True, self.colors['highlight'])
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        surface.blit(title_text, title_rect)
        
        # Panneau d'information
        info_width = 600
        info_height = 300
        info_x = self.screen_width // 2 - info_width // 2
        info_y = 100
        
        info_surface = Surface((info_width, info_height), pygame.SRCALPHA)
        info_surface.fill((30, 30, 80, 255))
        draw.rect(info_surface, self.colors['highlight'], (0, 0, info_width, info_height), 2)
        
        # Message de promotion
        category_names = {
            'f3': 'Formule 3',
            'f2': 'Formule 2',
            'f1': 'Formule 1'
        }
        current_category = category_names.get(self.player.category, self.player.category)
        
        next_category = "Formule 1" if self.player.category == 'f2' else "Formule 2"
        
        message = f"Félicitations! Grâce à vos performances en {current_category}, vous avez la possibilité de monter en {next_category} pour la prochaine saison."
        
        # Afficher le message ligne par ligne
        message_words = message.split()
        message_lines = []
        current_line = ""
        
        for word in message_words:
            test_line = current_line + " " + word if current_line else word
            if self.info_font.size(test_line)[0] <= info_width - 40:
                current_line = test_line
            else:
                message_lines.append(current_line)
                current_line = word
        
        if current_line:
            message_lines.append(current_line)
        
        # Afficher les lignes du message
        for i, line in enumerate(message_lines):
            line_text = self.info_font.render(line, True, self.colors['text'])
            line_rect = line_text.get_rect(center=(info_width // 2, 60 + i * 30))
            info_surface.blit(line_text, line_rect)
        
        # Message de choix
        choice_text = self.info_font.render("Que voulez-vous faire?", True, self.colors['highlight'])
        choice_rect = choice_text.get_rect(center=(info_width // 2, info_height - 100))
        info_surface.blit(choice_text, choice_rect)
        
        surface.blit(info_surface, (info_x, info_y))
        
        # Affichage des boutons
        for button in self.action_buttons:
            button.draw(surface)
    
    def _render_contract_offers(self, surface):
        """
        Dessine l'écran des offres de contrat
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Titre
        title_text = self.title_font.render("OFFRES DE CONTRAT", True, self.colors['highlight'])
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        surface.blit(title_text, title_rect)
        
        # Sous-titre
        subtitle_text = self.info_font.render("Sélectionnez une offre pour continuer votre carrière", True, self.colors['text'])
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 100))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Panneau d'information
        info_width = 600
        info_height = 120
        info_x = self.screen_width // 2 - info_width // 2
        info_y = 150
        
        info_surface = Surface((info_width, info_height), pygame.SRCALPHA)
        info_surface.fill((30, 30, 80, 255))
        draw.rect(info_surface, self.colors['highlight'], (0, 0, info_width, info_height), 2)
        
        # Information sur le choix d'équipe
        info_lines = [
            "Les équipes de Formule 1 offrent les meilleures perspectives de carrière,",
            "mais la concurrence y est plus rude.",
            "Considérez également la performance de la voiture et les conditions du contrat."
        ]
        
        for i, line in enumerate(info_lines):
            line_text = self.status_font.render(line, True, self.colors['text'])
            line_rect = line_text.get_rect(center=(info_width // 2, 30 + i * 25))
            info_surface.blit(line_text, line_rect)
        
        surface.blit(info_surface, (info_x, info_y))
        
        # Affichage des boutons
        for button in self.action_buttons:
            button.draw(surface)