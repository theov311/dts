#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface utilisateur pendant une course
"""

import pygame
from pygame import font, draw, Rect, Surface
import random
from src.ui.main_menu import Button

class RaceUI:
    """Interface utilisateur pour une course"""
    
    def __init__(self, game, player, race):
        """
        Initialisation de l'interface de course
        
        Args:
            game: Instance principale du jeu
            player: Joueur
            race: Instance de la course
        """
        self.game = game
        self.player = player
        self.race = race
        
        # Dimensions de l'écran
        self.screen_width = game.screen.get_width()
        self.screen_height = game.screen.get_height()
        
        # Charger les polices
        font.init()
        self.title_font = font.SysFont('Arial', 36, bold=True)
        self.info_font = font.SysFont('Arial', 24)
        self.action_font = font.SysFont('Arial', 20)
        self.status_font = font.SysFont('Arial', 18)
        
        # Couleurs
        self.colors = {
            'background': (30, 30, 50),
            'text': (255, 255, 255),
            'highlight': (255, 220, 50),
            'button': (50, 100, 180),
            'button_hover': (70, 130, 210),
            'warning': (220, 50, 50),
            'success': (50, 180, 50),
            'info': (50, 150, 220)
        }
        
        # État de l'interface
        self.race_started = False
        self.race_finished = False
        self.current_actions = []
        self.selected_action = None
        self.action_result = None
        
        # Initialiser current_state avec des valeurs par défaut
        self.current_state = {
            'lap': 0,
            'total_laps': race.total_laps,
            'positions': {},
            'player_position': 0,
            'is_finished': False,
            'weather': race.weather,
            'time_gaps': {},      # Écarts de temps entre les pilotes
            'car_status': {       # État de la voiture du joueur
                'tire_wear': 0,
                'fuel_level': 100,
                'damage': 0
            }
        }
        
        # Horloge pour animations et timings
        self.clock = pygame.time.Clock()
        self.elapsed_time = 0
        
        # Boutons d'actions
        self.action_buttons = []
        
        # Bouton de retour
        self.back_button = Button(
            "RETOUR",
            self.screen_width // 2 - 50,  # Centré horizontalement
            self.screen_height - 100,     # En bas de l'écran
            120,
            50,
            action=self.return_to_career,
            bg_color=self.colors['warning'],
            hover_color=(250, 80, 80)
        )
        
        # Démarrer la course
        self.start_race()
    
    def return_to_career(self):
        """Retourne à l'interface de carrière"""
        print("Retour à la carrière")  # Débogage
        self.game.current_state = 1  # Retour à l'interface de carrière
    
    def start_race(self):
        """Démarrage de la course"""
        # Qualifier les pilotes
        quali_results = self.race.run_qualifying()
        
        # Initialiser la course
        self.current_state = self.race.start_race()
        
        # S'assurer que current_state a toutes les clés nécessaires
        if 'lap' not in self.current_state:
            self.current_state['lap'] = 1
        if 'total_laps' not in self.current_state:
            self.current_state['total_laps'] = self.race.total_laps
        if 'positions' not in self.current_state:
            self.current_state['positions'] = {}
        if 'player_position' not in self.current_state:
            self.current_state['player_position'] = 0
        if 'weather' not in self.current_state:
            self.current_state['weather'] = self.race.weather
        if 'is_finished' not in self.current_state:
            self.current_state['is_finished'] = False
        if 'time_gaps' not in self.current_state:
            self.current_state['time_gaps'] = {}
        if 'car_status' not in self.current_state:
            self.current_state['car_status'] = {
                'tire_wear': 0,
                'fuel_level': 100,
                'damage': 0
            }
        
        self.race_started = True
        self.race_finished = False
        
        # Générer les actions disponibles pour le joueur
        self.update_available_actions()
    
    def update_available_actions(self):
        """Met à jour les actions disponibles pour le joueur"""
        # Récupérer les actions disponibles de la course
        action_ids = self.race.get_available_actions('player')
        
        # Trouver les événements correspondants
        self.current_actions = []
        for action_id in action_ids:
            event = next((e for e in self.race.available_events if e.id == action_id), None)
            if event:
                self.current_actions.append(event)
        
        # Créer les boutons d'action
        self.create_action_buttons()
    
    def create_action_buttons(self):
        """Crée les boutons pour les actions disponibles"""
        self.action_buttons = []
        
        # Position et dimensions des boutons
        button_width = 250
        button_height = 40
        button_x = self.screen_width // 2 - button_width // 2
        button_y_start = self.screen_height - 180
        button_spacing = 10
        
        for i, action in enumerate(self.current_actions):
            button_y = button_y_start + (button_height + button_spacing) * i
            
            def create_action_handler(action_id):
                return lambda: self.handle_action(action_id)
            
            # Couleur du bouton selon le type d'action
            button_color = self.colors['button']
            hover_color = self.colors['button_hover']
            
            if action.id.startswith('overtake'):
                button_color = (200, 70, 50)  # Rouge pour les dépassements
                hover_color = (230, 100, 80)
            elif action.id.startswith('defend'):
                button_color = (50, 150, 50)  # Vert pour les défenses
                hover_color = (80, 180, 80)
            elif action.id == 'push_pace':
                button_color = (220, 150, 50)  # Orange pour pousser le rythme
                hover_color = (250, 180, 80)
            elif action.id == 'conserve_tires':
                button_color = (50, 150, 200)  # Bleu pour préserver les pneus
                hover_color = (80, 180, 230)
            
            # Créer le bouton
            button = Button(
                action.name,
                button_x,
                button_y,
                button_width,
                button_height,
                action=create_action_handler(action.id),
                bg_color=button_color,
                hover_color=hover_color
            )
            
            self.action_buttons.append(button)
    
    def handle_action(self, action_id):
        """
        Gère une action du joueur
        
        Args:
            action_id (str): ID de l'action choisie
        """
        if self.race_finished:
            return
        
        # Exécuter l'action
        self.action_result = self.race.execute_player_action(action_id)
        
        # Mise à jour de l'état de la voiture
        car_status = self.current_state.get('car_status', {})
        
        # Mise à jour de l'usure des pneus
        if 'tire_wear' in self.action_result:
            car_status['tire_wear'] = min(100, car_status.get('tire_wear', 0) + self.action_result['tire_wear'])
        
        # Mise à jour des dégâts
        if 'car_damage' in self.action_result:
            car_status['damage'] = min(100, car_status.get('damage', 0) + self.action_result['car_damage'])
        
        # Mise à jour du carburant (consommation de base par tour)
        car_status['fuel_level'] = max(0, car_status.get('fuel_level', 100) - 2)
        
        # Mettre à jour l'état
        self.current_state['car_status'] = car_status
        
        # Attendre un peu avant de passer au tour suivant
        pygame.time.delay(1000)  # 1 seconde
        
        # Avancer d'un tour
        self.current_state = self.race.advance_lap()
        
        # S'assurer que current_state a toutes les clés nécessaires
        if 'lap' not in self.current_state:
            self.current_state['lap'] = self.race.current_lap
        if 'total_laps' not in self.current_state:
            self.current_state['total_laps'] = self.race.total_laps
        if 'positions' not in self.current_state:
            self.current_state['positions'] = {}
        if 'player_position' not in self.current_state:
            self.current_state['player_position'] = 0
        if 'weather' not in self.current_state:
            self.current_state['weather'] = self.race.weather
        if 'is_finished' not in self.current_state:
            self.current_state['is_finished'] = False
        if 'time_gaps' not in self.current_state:
            self.current_state['time_gaps'] = {}
            
        # Conserver l'état de la voiture
        if 'car_status' not in self.current_state:
            self.current_state['car_status'] = car_status
        
        # Vérifier si la course est terminée
        if self.current_state.get('is_finished', False):
            self.race_finished = True
            # Afficher les résultats finaux
            self._show_race_results()
        else:
            # Mettre à jour les actions disponibles
            self.update_available_actions()
    
    def _show_race_results(self):
        """Affiche les résultats finaux de la course"""
        # Récupérer les résultats
        self.race_results = self.race.get_race_results()
        
        # Mettre à jour le joueur avec les résultats
        race_results_for_player = {
            'position': self.race_results['player_position'],
            'points': self.race_results['points'],
            'prize_money': self.race_results['prize_money'],
            'skill_improvements': self.race_results['skill_improvements']
        }
        
        # Mettre à jour les statistiques du joueur
        self.player.update_stats(race_results_for_player)
    
    def handle_event(self, event):
        """
        Gère les événements de l'interface
        
        Args:
            event (pygame.event.Event): Événement à gérer
        """
        # Touche Échap pour revenir au menu précédent si la course est terminée
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.race_finished:
            print("Retour à la carrière via touche Échap")
            self.game.current_state = 1  # Retour à l'interface de carrière
            return True
    
    # Gestion des boutons d'action
        for button in self.action_buttons:
            if button.handle_event(event):
                return True
    
    # Gestion du bouton retour si la course est terminée
        if self.race_finished and event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.rect.collidepoint(event.pos):
                print("Retour à la carrière via clic sur bouton")
                self.game.current_state = 1  # Retour à l'interface de carrière
                return True
    
        return False
    
    def update(self):
        """Met à jour l'état de l'interface"""
        self.elapsed_time += self.clock.tick(60)  # 60 FPS
    
    def draw_standings(self, surface):
        """
        Dessine le classement de la course
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Fond du classement
        standings_rect = Rect(20, 120, 300, 400)
        standings_surface = Surface((standings_rect.width, standings_rect.height), pygame.SRCALPHA)
        standings_surface.fill((0, 0, 0, 180))  # Fond semi-transparent
        
        # Titre du classement
        standings_title = self.info_font.render("CLASSEMENT", True, self.colors['highlight'])
        standings_surface.blit(standings_title, (10, 10))
        
        # Position actuelle du joueur
        player_pos = self.race.positions.get('player', 0)
        player_pos_text = self.info_font.render(f"Votre position: {player_pos}", True, self.colors['highlight'])
        standings_surface.blit(player_pos_text, (10, 40))
        
        # Afficher le classement
        positions = sorted(self.race.positions.items(), key=lambda x: x[1])
        
        y_offset = 80
        leader_id = positions[0][0] if positions else None
        
        for i, (driver_id, position) in enumerate(positions[:15]):  # Limiter aux 15 premiers
            driver_info = self.race.drivers[driver_id]
            driver_name = driver_info['name'] if driver_id != 'player' else f"{self.player.name} (Vous)"
            team_name = driver_info['team']
            
            # Couleur pour le joueur
            text_color = self.colors['highlight'] if driver_id == 'player' else self.colors['text']
            
            pos_text = self.status_font.render(f"{position}.", True, text_color)
            name_text = self.status_font.render(driver_name, True, text_color)
            
            # Afficher les écarts de temps
            time_gap = ""
            if driver_id != leader_id and i > 0:  # Pas le leader
                time_gap_value = self.current_state.get('time_gaps', {}).get(driver_id, 0)
                if time_gap_value > 0:
                    time_gap = f"+{time_gap_value:.1f}s"
            
            gap_text = self.status_font.render(time_gap, True, text_color)
            
            standings_surface.blit(pos_text, (15, y_offset))
            standings_surface.blit(name_text, (40, y_offset))
            standings_surface.blit(gap_text, (170, y_offset))
            
            team_text_y = y_offset + 20
            team_text = self.status_font.render(team_name, True, text_color)
            standings_surface.blit(team_text, (40, team_text_y))
            
            y_offset += 40
        
        surface.blit(standings_surface, standings_rect)
    
    def draw_race_info(self, surface):
        """
        Dessine les informations de course
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Fond des infos
        info_rect = Rect(self.screen_width - 320, 120, 300, 150)
        info_surface = Surface((info_rect.width, info_rect.height), pygame.SRCALPHA)
        info_surface.fill((0, 0, 0, 180))  # Fond semi-transparent
        
        # Titre de la course
        race_title = self.info_font.render(self.race.name, True, self.colors['highlight'])
        info_surface.blit(race_title, (10, 10))
        
        # Circuit
        circuit_text = self.status_font.render(f"Circuit: {self.race.circuit['name']}", True, self.colors['text'])
        info_surface.blit(circuit_text, (10, 40))
        
        # Tour actuel - Utiliser self.race.current_lap si la clé n'existe pas
        lap_text = self.status_font.render(
            f"Tour: {self.current_state.get('lap', self.race.current_lap)}/{self.race.total_laps}", 
            True, self.colors['text']
        )
        info_surface.blit(lap_text, (10, 65))
        
        # Conditions météo
        weather_condition = self.race.weather['condition']
        weather_text = self.status_font.render(f"Météo: {weather_condition}", True, self.colors['text'])
        info_surface.blit(weather_text, (10, 90))
        
        surface.blit(info_surface, info_rect)
    
    def draw_action_result(self, surface):
        """
        Dessine le résultat de la dernière action
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        if not self.action_result:
            return
        
        # Fond du résultat
        result_rect = Rect(self.screen_width - 320, 300, 300, 100)
        result_surface = Surface((result_rect.width, result_rect.height), pygame.SRCALPHA)
        
        # Couleur selon le résultat
        if self.action_result.get('success', False):
            result_surface.fill((0, 100, 0, 180))  # Vert semi-transparent
            result_title = self.info_font.render("RÉUSSITE!", True, self.colors['text'])
        else:
            result_surface.fill((100, 0, 0, 180))  # Rouge semi-transparent
            result_title = self.info_font.render("ÉCHEC!", True, self.colors['text'])
        
        result_surface.blit(result_title, (10, 10))
        
        # Message du résultat
        message = self.action_result.get('message', '')
        message_words = message.split()
        message_lines = []
        current_line = ""
        
        # Découper le message en lignes
        for word in message_words:
            test_line = current_line + " " + word if current_line else word
            if self.status_font.size(test_line)[0] <= result_rect.width - 20:
                current_line = test_line
            else:
                message_lines.append(current_line)
                current_line = word
        
        if current_line:
            message_lines.append(current_line)
        
        # Afficher les lignes du message
        for i, line in enumerate(message_lines):
            line_text = self.status_font.render(line, True, self.colors['text'])
            result_surface.blit(line_text, (10, 40 + i * 20))
        
        surface.blit(result_surface, result_rect)
    
    def draw_car_status(self, surface):
        """
        Dessine l'état de la voiture du joueur
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Fond de l'état de la voiture
        status_rect = Rect(self.screen_width - 320, 430, 300, 120)
        status_surface = Surface((status_rect.width, status_rect.height), pygame.SRCALPHA)
        status_surface.fill((0, 0, 0, 180))  # Fond semi-transparent
        
        # Titre
        status_title = self.status_font.render("ÉTAT DE LA VOITURE", True, self.colors['highlight'])
        status_surface.blit(status_title, (10, 10))
        
        # Récupérer l'état de la voiture
        car_status = self.current_state.get('car_status', {})
        damage_value = car_status.get('damage', 0)
        tire_wear_value = car_status.get('tire_wear', 0)
        fuel_level = car_status.get('fuel_level', 100)
        
        # Dégâts
        damage_color = (
            min(255, 50 + damage_value * 2),
            max(0, 200 - damage_value * 2),
            50
        )
        damage_text = self.status_font.render(f"Dégâts: {damage_value}%", True, damage_color)
        status_surface.blit(damage_text, (10, 40))
        
        # Usure des pneus
        tire_color = (
            min(255, 50 + tire_wear_value * 2),
            max(0, 200 - tire_wear_value * 2),
            50
        )
        tire_text = self.status_font.render(f"Usure pneus: {tire_wear_value}%", True, tire_color)
        status_surface.blit(tire_text, (10, 65))
        
        # Carburant
        fuel_color = (255, 255, 255)
        if fuel_level < 30:
            fuel_color = (255, 150, 0)  # Orange pour niveau bas
        if fuel_level < 10:
            fuel_color = (255, 0, 0)     # Rouge pour niveau critique
            
        fuel_text = self.status_font.render(f"Carburant: {fuel_level}%", True, fuel_color)
        status_surface.blit(fuel_text, (10, 90))
        
        surface.blit(status_surface, status_rect)
    
    def draw_race_results(self, surface):
        """
        Dessine les résultats finaux de la course
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        if not self.race_finished or not hasattr(self, 'race_results'):
            return
        
        # Fond semi-transparent sur tout l'écran
        overlay = Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        # Panneau de résultats
        results_width = 600
        results_height = 500
        results_x = self.screen_width // 2 - results_width // 2
        results_y = self.screen_height // 2 - results_height // 2
        
        results_surface = Surface((results_width, results_height), pygame.SRCALPHA)
        results_surface.fill((30, 30, 80, 255))
        draw.rect(results_surface, self.colors['highlight'], (0, 0, results_width, results_height), 2)
        
        # Titre
        title_text = self.title_font.render("RÉSULTATS DE COURSE", True, self.colors['highlight'])
        title_rect = title_text.get_rect(center=(results_width // 2, 40))
        results_surface.blit(title_text, title_rect)
        
        # Nom de la course
        race_name_text = self.info_font.render(self.race.name, True, self.colors['text'])
        race_name_rect = race_name_text.get_rect(center=(results_width // 2, 80))
        results_surface.blit(race_name_text, race_name_rect)
        
        # Position finale
        player_pos = self.race_results['player_position']
        position_color = self.colors['success'] if player_pos <= 3 else self.colors['text']
        position_text = self.title_font.render(f"Position finale: {player_pos}", True, position_color)
        position_rect = position_text.get_rect(center=(results_width // 2, 130))
        results_surface.blit(position_text, position_rect)
        
        # Points marqués
        points = self.race_results['points']
        points_text = self.info_font.render(f"Points marqués: {points}", True, self.colors['text'])
        points_rect = points_text.get_rect(center=(results_width // 2, 170))
        results_surface.blit(points_text, points_rect)
        
        # Prime d'argent
        prize_money = self.race_results['prize_money']
        money_text = self.info_font.render(f"Prime: {prize_money:,.0f} €", True, self.colors['text'])
        money_rect = money_text.get_rect(center=(results_width // 2, 200))
        results_surface.blit(money_text, money_rect)
        
        # Améliorations de compétence
        skill_improvements = self.race_results.get('skill_improvements', {})
        skill_text = self.info_font.render("Améliorations de compétence:", True, self.colors['highlight'])
        results_surface.blit(skill_text, (50, 240))
        
        y_offset = 270
        for skill, amount in skill_improvements.items():
            skill_name = {
                'overall': 'Niveau général',
                'pace': 'Rythme',
                'overtaking': 'Dépassement',
                'defending': 'Défense',
                'consistency': 'Régularité',
                'tire_management': 'Gestion des pneus',
                'wet_driving': 'Pilotage sous la pluie',
                'technical_feedback': 'Feedback technique',
                'starts': 'Départs'
            }.get(skill, skill)
            
            improvement_text = self.status_font.render(f"{skill_name}: +{amount:.2f}", True, self.colors['success'])
            results_surface.blit(improvement_text, (70, y_offset))
            y_offset += 25
        
        # Message de fin
        finish_message = "Appuyez sur RETOUR pour continuer"
        finish_text = self.status_font.render(finish_message, True, self.colors['text'])
        finish_rect = finish_text.get_rect(center=(results_width // 2, results_height - 40))
        results_surface.blit(finish_text, finish_rect)
        
        surface.blit(results_surface, (results_x, results_y))
    
    def render(self, surface):
        """
        Dessine l'interface de course sur une surface
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Fond de base
        surface.fill(self.colors['background'])
        
        # Dessiner la piste (simple fond abstrait)
        self._draw_track_background(surface)
        
        # Informations de course
        self.draw_race_info(surface)
        
        # Classement
        self.draw_standings(surface)
        
        # État de la voiture
        self.draw_car_status(surface)
        
        # Résultat de la dernière action
        self.draw_action_result(surface)
        
        # Boutons d'action
        if not self.race_finished:
            for button in self.action_buttons:
                button.draw(surface)
        
        # Bouton retour
        if self.race_finished:
            self.back_button.draw(surface)
        
        # Résultats de course
        if self.race_finished:
            self.draw_race_results(surface)
    
    def _draw_track_background(self, surface):
        """
        Dessine un fond abstrait représentant la piste
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        # Créer une surface pour la piste
        track_surface = Surface((self.screen_width, self.screen_height))
        
        # Couleur de fond selon la météo
        if self.race.weather['condition'] == 'Sec':
            track_color = (100, 100, 100)  # Gris pour piste sèche
        elif self.race.weather['condition'] == 'Pluie légère':
            track_color = (80, 80, 100)  # Gris-bleu pour pluie légère
        else:
            track_color = (60, 60, 80)  # Gris foncé pour pluie forte
        
        track_surface.fill(track_color)
        
        # Dessiner la ligne de course (courbe abstraite)
        points = [
            (0, self.screen_height // 2),
            (self.screen_width // 4, self.screen_height // 4),
            (self.screen_width // 2, self.screen_height // 3),
            (self.screen_width * 3 // 4, self.screen_height // 2),
            (self.screen_width, self.screen_height // 3)
        ]
        
        # Dessiner une ligne large pour la piste
        draw.lines(track_surface, (150, 150, 150), False, points, 60)
        
        # Ligne blanche au milieu
        draw.lines(track_surface, (255, 255, 255), False, points, 2)
        
        # Dessiner quelques marques de vibreurs
        for i in range(10):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            width = random.randint(20, 50)
            height = random.randint(5, 10)
            
            # Alterner rouge et blanc
            if i % 2 == 0:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            
            draw.rect(track_surface, color, (x, y, width, height))
        
        # Titre de la course
        title_text = self.title_font.render(self.race.name, True, self.colors['text'])
        track_surface.blit(title_text, (20, 20))
        
        # Ajouter un peu de transparence
        track_surface.set_alpha(100)
        
        # Dessiner sur la surface principale
        surface.blit(track_surface, (0, 0))