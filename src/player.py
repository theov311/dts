#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classe qui représente le joueur/pilote avec ses caractéristiques et statistiques
"""

class DriverSkills:
    """Compétences du pilote"""
    
    def __init__(self):
        # Compétences principales (0-100)
        self.pace = 20  # Vitesse pure
        self.overtaking = 20  # Capacité de dépassement
        self.defending = 20  # Défense de position
        self.consistency = 20  # Régularité
        self.tire_management = 20  # Gestion des pneus
        self.wet_driving = 20  # Pilotage sous la pluie
        self.technical_feedback = 20  # Feedback technique pour les réglages
        self.starts = 20  # Départs
        
        # Niveau global (calculé à partir des compétences)
        self.calculate_overall()
    
    def calculate_overall(self):
        """Calcule le niveau global du pilote"""
        skills = [
            self.pace, self.overtaking, self.defending, 
            self.consistency, self.tire_management, 
            self.wet_driving, self.technical_feedback, self.starts
        ]
        self.overall = sum(skills) / len(skills)
        return self.overall
    
    def improve_skill(self, skill_name, amount):
        """
        Améliore une compétence spécifique
        
        Args:
            skill_name (str): Nom de la compétence à améliorer
            amount (float): Montant de l'amélioration
        """
        if hasattr(self, skill_name):
            current = getattr(self, skill_name)
            setattr(self, skill_name, min(100, current + amount))
            self.calculate_overall()


class DriverStats:
    """Statistiques de carrière du pilote"""
    
    def __init__(self):
        # Statistiques globales
        self.races = 0
        self.wins = 0
        self.podiums = 0
        self.points = 0
        self.championships = 0
        self.best_finish = 0
        
        # Statistiques par catégorie
        self.f3_stats = {'races': 0, 'wins': 0, 'podiums': 0, 'points': 0, 'championships': 0}
        self.f2_stats = {'races': 0, 'wins': 0, 'podiums': 0, 'points': 0, 'championships': 0}
        self.f1_stats = {'races': 0, 'wins': 0, 'podiums': 0, 'points': 0, 'championships': 0}
    
    def update(self, category, position, points):
        """
        Mise à jour des statistiques après une course
        
        Args:
            category (str): Catégorie ('f3', 'f2', 'f1')
            position (int): Position d'arrivée
            points (float): Points marqués
        """
        # Mise à jour des stats globales
        self.races += 1
        self.points += points
        
        if position == 1:
            self.wins += 1
            self.podiums += 1
        elif position <= 3:
            self.podiums += 1
        
        if position < self.best_finish or self.best_finish == 0:
            self.best_finish = position
        
        # Mise à jour des stats par catégorie
        cat_stats = getattr(self, f"{category}_stats")
        cat_stats['races'] += 1
        cat_stats['points'] += points
        
        if position == 1:
            cat_stats['wins'] += 1
            cat_stats['podiums'] += 1
        elif position <= 3:
            cat_stats['podiums'] += 1


class Player:
    """Classe représentant le joueur/pilote"""
    
    def __init__(self, name, age):
        """
        Initialisation du joueur
        
        Args:
            name (str): Nom du pilote
            age (int): Âge du pilote
        """
        self.name = name
        self.age = age
        self.reputation = 0  # Réputation dans le monde de la course (0-100)
        self.money = 0  # Argent gagné
        self.academy = None  # Académie de pilote (Ferrari, Mercedes, etc.)
        self.team = None  # Équipe actuelle
        self.category = "f3"  # Catégorie actuelle (f3, f2, f1)
        
        # Compétences et statistiques
        self.skills = DriverSkills()
        self.stats = DriverStats()
        
        # Progression de carrière
        self.contract_years = 0  # Années restantes de contrat
        self.contract_value = 0  # Valeur du contrat
    
    def join_academy(self, academy):
        """
        Rejoint une académie de pilotes
        
        Args:
            academy: Académie à rejoindre
        """
        self.academy = academy
        self.reputation += 5  # Augmentation de la réputation
    
    def sign_contract(self, team, years, value):
        """
        Signe un contrat avec une équipe
        
        Args:
            team: Équipe avec laquelle signer
            years (int): Durée du contrat en années
            value (float): Valeur du contrat
        """
        self.team = team
        self.contract_years = years
        self.contract_value = value
        self.money += value / years  # Premier paiement
    
    def promote_category(self, new_category):
        """
        Promotion vers une catégorie supérieure
        
        Args:
            new_category (str): Nouvelle catégorie ('f3', 'f2', 'f1')
        """
        self.category = new_category
        self.reputation += 10  # Augmentation de la réputation
    
    def update_stats(self, race_results):
        """
        Mise à jour des statistiques après une course
        
        Args:
            race_results: Résultats de la course
        """
        position = race_results.get('position')
        points = race_results.get('points')
        skill_improvements = race_results.get('skill_improvements', {})
        
        # Mise à jour des statistiques
        self.stats.update(self.category, position, points)
        
        # Mise à jour des compétences
        for skill, amount in skill_improvements.items():
            self.skills.improve_skill(skill, amount)
        
        # Mise à jour de la réputation
        if position <= 3:
            self.reputation += 2
        elif position <= 10:
            self.reputation += 1
        
        # Mise à jour de l'argent (bonus de course)
        self.money += race_results.get('prize_money', 0)
        
        # Une année de plus
        if race_results.get('season_end', False):
            self.age += 1
            self.contract_years -= 1  # Une année de moins de contrat