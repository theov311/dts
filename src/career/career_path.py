#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestion de la progression de carrière du pilote de F3 à F1
"""

from src.career.academy import create_all_academies
from src.career.season import Season

class CareerPath:
    """Classe gérant la progression de carrière du joueur"""
    
    def __init__(self, player):
        """
        Initialisation du chemin de carrière
        
        Args:
            player (Player): Joueur/pilote
        """
        self.player = player
        self.current_year = 2023  # Année de départ
        self.academies = create_all_academies()
        self.seasons = []  # Historique des saisons
        self.current_season = None
        
        # Configuration des catégories
        self.category_config = {
            'f3': {
                'races_per_season': 7,
                'promotion_threshold': 70,  # Niveau minimum pour être promu
                'points_system': [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
            },
            'f2': {
                'races_per_season': 12,
                'promotion_threshold': 80,
                'points_system': [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
            },
            'f1': {
                'races_per_season': 23,
                'points_system': [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
            }
        }
    
    def start_career(self, selected_academy):
        """
        Démarre la carrière avec l'académie sélectionnée
        
        Args:
            selected_academy: Académie choisie par le joueur
        """
        # Rejoindre l'académie sélectionnée
        self.player.join_academy(selected_academy)
        
        # Signer avec l'équipe F3 de l'académie
        f3_team = selected_academy.get_team_by_category('f3')
        if f3_team:
            contract = f3_team.get_contract_offer(self.player.reputation)
            self.player.sign_contract(f3_team, contract['years'], contract['value'])
        
        # Démarrer la première saison
        self.start_new_season()
    
    def start_new_season(self):
        """Démarre une nouvelle saison pour le joueur"""
        category = self.player.category
        races_count = self.category_config[category]['races_per_season']
        points_system = self.category_config[category]['points_system']
        
        # Création de la nouvelle saison
        self.current_season = Season(
            year=self.current_year,
            category=category,
            races_count=races_count,
            points_system=points_system,
            player=self.player,
            teams=self._get_category_teams(category)
        )
        
        # Ajouter la saison à l'historique
        self.seasons.append(self.current_season)
    
    def _get_category_teams(self, category):
        """
        Récupère toutes les équipes d'une catégorie donnée
        
        Args:
            category (str): Catégorie ('f3', 'f2', 'f1')
            
        Returns:
            list: Liste des équipes de la catégorie
        """
        teams = []
        for academy in self.academies:
            team = academy.get_team_by_category(category)
            if team:
                teams.append(team)
        return teams
    
    def end_season(self):
        """
        Termine la saison actuelle et gère la progression de carrière
        
        Returns:
            dict: Résultats de fin de saison
        """
        results = self.current_season.get_final_standings()
        player_position = results['player_position']
        player_points = results['player_points']
        
        # Mise à jour de l'année
        self.current_year += 1
        
        # Progression de carrière basée sur la performance
        promotion = self._check_promotion(player_position, player_points)
        
        # Si le contrat est terminé, proposer de nouveaux contrats
        new_contracts = []
        if self.player.contract_years <= 0:
            new_contracts = self._generate_contract_offers()
        
        # Résultats de fin de saison
        season_end_results = {
            'year': self.current_season.year,
            'category': self.current_season.category,
            'position': player_position,
            'points': player_points,
            'promotion_available': promotion,
            'new_contracts': new_contracts,
            'season_end': True
        }
        
        return season_end_results
    
    def _check_promotion(self, position, points):
        """
        Vérifie si le joueur peut être promu à la catégorie supérieure
        
        Args:
            position (int): Position au championnat
            points (float): Points marqués
            
        Returns:
            bool: True si une promotion est possible
        """
        category = self.player.category
        
        # Vérifier si nous sommes déjà en F1
        if category == 'f1':
            return False
        
        # Critères de promotion
        promotion_threshold = self.category_config[category]['promotion_threshold']
        
        # Promotion basée sur la position (top 3) et sur le niveau du pilote
        if position <= 3 and self.player.skills.overall >= promotion_threshold:
            return True
        
        return False
    
    def promote_player(self):
        """
        Promeut le joueur à la catégorie supérieure
        
        Returns:
            str: Nouvelle catégorie
        """
        current_category = self.player.category
        
        if current_category == 'f3':
            new_category = 'f2'
        elif current_category == 'f2':
            new_category = 'f1'
        else:
            return current_category  # Déjà en F1
        
        # Mise à jour de la catégorie du joueur
        self.player.promote_category(new_category)
        
        return new_category
    
    def _generate_contract_offers(self):
        """
        Génère des offres de contrat pour le joueur
        
        Returns:
            list: Liste d'offres de contrat
        """
        category = self.player.category
        offers = []
        
        # Offres de l'académie actuelle (si applicable)
        if self.player.academy:
            team = self.player.academy.get_team_by_category(category)
            if team:
                offers.append(team.get_contract_offer(self.player.reputation))
        
        # Offres d'autres académies basées sur la réputation du joueur
        for academy in self.academies:
            if academy != self.player.academy:
                # Plus haute est la réputation du joueur, plus il a de chances d'obtenir des offres
                chance = min(80, int(self.player.reputation / 2))
                
                # Simulation d'une chance d'obtenir une offre
                import random
                if random.randint(1, 100) <= chance:
                    team = academy.get_team_by_category(category)
                    if team:
                        offers.append(team.get_contract_offer(self.player.reputation))
        
        return offers
    
    def sign_new_contract(self, contract_offer):
        """
        Signe un nouveau contrat
        
        Args:
            contract_offer (dict): Offre de contrat
        """
        team = contract_offer['team']
        years = contract_offer['years']
        value = contract_offer['value']
        
        # Si le joueur change d'académie
        if team.parent_academy != self.player.academy:
            self.player.join_academy(team.parent_academy)
        
        # Signer le nouveau contrat
        self.player.sign_contract(team, years, value)