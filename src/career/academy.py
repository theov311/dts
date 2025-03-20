#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestion des académies de pilotes (Ferrari, Mercedes, Red Bull, Alpine, McLaren)
"""

class Team:
    """Classe représentant une équipe de course"""
    
    def __init__(self, name, category, parent_academy=None, performance=50):
        """
        Initialisation d'une équipe
        
        Args:
            name (str): Nom de l'équipe
            category (str): Catégorie ('f3', 'f2', 'f1')
            parent_academy: Académie parente (peut être None)
            performance (int): Performance de base de l'équipe (0-100)
        """
        self.name = name
        self.category = category
        self.parent_academy = parent_academy
        self.performance = performance  # Performance de base de l'équipe
        self.reputation = 50  # Réputation initiale
        self.budget = self._calculate_budget()
        self.car_development = 50  # Niveau de développement de la voiture
        
        # Statistiques d'équipe
        self.stats = {
            'races': 0,
            'wins': 0,
            'podiums': 0,
            'points': 0,
            'championships': 0
        }
    
    def _calculate_budget(self):
        """Calcule le budget de l'équipe basé sur la catégorie et la réputation"""
        base_budget = {
            'f3': 1000000,
            'f2': 5000000,
            'f1': 150000000
        }
        
        # Le budget est influencé par la réputation
        reputation_factor = self.reputation / 50  # 1.0 pour la réputation moyenne
        return base_budget[self.category] * reputation_factor
    
    def get_contract_offer(self, player_reputation):
        """
        Génère une offre de contrat basée sur la réputation du joueur
        
        Args:
            player_reputation (float): Réputation du joueur
            
        Returns:
            dict: Détails du contrat (années, valeur)
        """
        base_value = {
            'f3': 50000,
            'f2': 200000,
            'f1': 1000000
        }
        
        # La valeur du contrat est influencée par la réputation du joueur
        rep_factor = player_reputation / 50  # 1.0 pour la réputation moyenne
        value = base_value[self.category] * rep_factor
        
        # Durée du contrat (généralement 1-3 ans)
        years = min(3, max(1, int(player_reputation / 30)))
        
        return {
            'team': self,
            'years': years,
            'value': value
        }
    
    def update_stats(self, race_results):
        """
        Mise à jour des statistiques d'équipe après une course
        
        Args:
            race_results: Résultats de la course
        """
        self.stats['races'] += 1
        self.stats['points'] += race_results.get('team_points', 0)
        
        if race_results.get('team_position') == 1:
            self.stats['wins'] += 1
            self.stats['podiums'] += 1
        elif race_results.get('team_position') <= 3:
            self.stats['podiums'] += 1
            
        # Mise à jour de la réputation
        position = race_results.get('team_position')
        if position <= 3:
            self.reputation = min(100, self.reputation + 1)
        elif position >= 8:
            self.reputation = max(0, self.reputation - 1)


class DriverAcademy:
    """Classe représentant une académie de pilotes"""
    
    def __init__(self, name, prestige, teams=None):
        """
        Initialisation d'une académie
        
        Args:
            name (str): Nom de l'académie
            prestige (int): Prestige de l'académie (0-100)
            teams (list): Liste d'équipes affiliées
        """
        self.name = name
        self.prestige = prestige
        self.teams = teams or []
        
        # Bonus d'académie pour les pilotes
        self.skill_bonuses = self._generate_skill_bonuses()
    
    def _generate_skill_bonuses(self):
        """
        Génère des bonus de compétences spécifiques à l'académie
        
        Returns:
            dict: Bonus de compétences
        """
        # Chaque académie a ses forces et faiblesses
        bonuses = {
            'pace': 0,
            'overtaking': 0,
            'defending': 0,
            'consistency': 0,
            'tire_management': 0,
            'wet_driving': 0,
            'technical_feedback': 0,
            'starts': 0
        }
        
        # Attribution de bonus en fonction du nom de l'académie
        if "Ferrari" in self.name:
            bonuses['pace'] = 5
            bonuses['technical_feedback'] = 3
        elif "Mercedes" in self.name:
            bonuses['consistency'] = 5
            bonuses['tire_management'] = 3
        elif "Red Bull" in self.name:
            bonuses['overtaking'] = 5
            bonuses['wet_driving'] = 3
        elif "Alpine" in self.name:
            bonuses['defending'] = 4
            bonuses['consistency'] = 4
        elif "McLaren" in self.name:
            bonuses['pace'] = 3
            bonuses['starts'] = 5
        
        return bonuses
    
    def get_team_by_category(self, category):
        """
        Récupère une équipe de cette académie par catégorie
        
        Args:
            category (str): Catégorie ('f3', 'f2', 'f1')
            
        Returns:
            Team: Équipe correspondante ou None
        """
        for team in self.teams:
            if team.category == category:
                return team
        return None
    
    def add_team(self, team):
        """
        Ajoute une équipe à l'académie
        
        Args:
            team (Team): Équipe à ajouter
        """
        team.parent_academy = self
        self.teams.append(team)


def create_all_academies():
    """
    Crée toutes les académies avec leurs équipes
    
    Returns:
        list: Liste de toutes les académies
    """
    # Ferrari Driver Academy
    ferrari_academy = DriverAcademy("Ferrari Driver Academy", 90)
    ferrari_academy.add_team(Team("Prema Racing", "f3", ferrari_academy, 75))
    ferrari_academy.add_team(Team("Prema Racing", "f2", ferrari_academy, 80))
    ferrari_academy.add_team(Team("Scuderia Ferrari", "f1", ferrari_academy, 85))
    
    # Mercedes Junior Team
    mercedes_academy = DriverAcademy("Mercedes Junior Team", 85)
    mercedes_academy.add_team(Team("ART Grand Prix", "f3", mercedes_academy, 70))
    mercedes_academy.add_team(Team("ART Grand Prix", "f2", mercedes_academy, 75))
    mercedes_academy.add_team(Team("Mercedes-AMG Petronas", "f1", mercedes_academy, 90))
    
    # Red Bull Junior Team
    redbull_academy = DriverAcademy("Red Bull Junior Team", 80)
    redbull_academy.add_team(Team("Hitech Grand Prix", "f3", redbull_academy, 65))
    redbull_academy.add_team(Team("Carlin", "f2", redbull_academy, 70))
    redbull_academy.add_team(Team("Red Bull Racing", "f1", redbull_academy, 88))
    
    # Alpine Academy
    alpine_academy = DriverAcademy("Alpine Academy", 75)
    alpine_academy.add_team(Team("MP Motorsport", "f3", alpine_academy, 60))
    alpine_academy.add_team(Team("Virtuosi Racing", "f2", alpine_academy, 65))
    alpine_academy.add_team(Team("BWT Alpine F1 Team", "f1", alpine_academy, 75))
    
    # McLaren Driver Development
    mclaren_academy = DriverAcademy("McLaren Driver Development", 78)
    mclaren_academy.add_team(Team("Campos Racing", "f3", mclaren_academy, 62))
    mclaren_academy.add_team(Team("DAMS", "f2", mclaren_academy, 68))
    mclaren_academy.add_team(Team("McLaren F1 Team", "f1", mclaren_academy, 82))
    
    return [ferrari_academy, mercedes_academy, redbull_academy, alpine_academy, mclaren_academy]