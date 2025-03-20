#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestion des caractéristiques et dégâts des voitures
"""

class Car:
    """Classe représentant une voiture de course"""
    
    def __init__(self, category, team_performance=50):
        """
        Initialisation d'une voiture
        
        Args:
            category (str): Catégorie ('f3', 'f2', 'f1')
            team_performance (int): Performance de base de l'équipe (0-100)
        """
        self.category = category
        
        # Caractéristiques de base selon la catégorie
        base_stats = {
            'f3': {
                'top_speed': 250,  # km/h
                'acceleration': 60,
                'braking': 70,
                'cornering': 75,
                'reliability': 85,
                'fuel_efficiency': 80
            },
            'f2': {
                'top_speed': 280,  # km/h
                'acceleration': 70,
                'braking': 75,
                'cornering': 80,
                'reliability': 80,
                'fuel_efficiency': 75
            },
            'f1': {
                'top_speed': 330,  # km/h
                'acceleration': 95,
                'braking': 95,
                'cornering': 95,
                'reliability': 75,
                'fuel_efficiency': 70
            }
        }
        
        # Initialiser les caractéristiques avec les valeurs de base
        self.stats = base_stats.get(category, base_stats['f3']).copy()
        
        # Ajuster selon la performance de l'équipe
        self._adjust_for_team_performance(team_performance)
        
        # État actuel de la voiture
        self.damage = 0  # Dégâts (0-100)
        self.tire_wear = 0  # Usure des pneus (0-100)
        self.fuel_level = 100  # Niveau de carburant (0-100)
    
    def _adjust_for_team_performance(self, team_performance):
        """
        Ajuste les caractéristiques en fonction de la performance de l'équipe
        
        Args:
            team_performance (int): Performance de l'équipe (0-100)
        """
        # Facteur d'ajustement basé sur la performance de l'équipe
        factor = (team_performance - 50) / 100  # -0.5 à +0.5
        
        # Ajuster chaque caractéristique
        for key in self.stats:
            self.stats[key] = int(self.stats[key] * (1 + factor * 0.3))
    
    def take_damage(self, amount):
        """
        Applique des dégâts à la voiture
        
        Args:
            amount (int): Quantité de dégâts (0-100)
            
        Returns:
            dict: État de la voiture après les dégâts
        """
        self.damage = min(100, self.damage + amount)
        
        # Impact des dégâts sur les performances
        impact = {}
        
        if self.damage > 20:
            # Réduction des performances proportionnelle aux dégâts
            factor = self.damage / 100
            impact['top_speed'] = int(self.stats['top_speed'] * factor)
            impact['acceleration'] = int(self.stats['acceleration'] * factor * 0.5)
            impact['cornering'] = int(self.stats['cornering'] * factor * 0.7)
        
        # Risque de panne si dégâts importants
        reliability_impact = self.damage / 2
        impact['reliability'] = int(self.stats['reliability'] * (reliability_impact / 100))
        
        return {
            'damage': self.damage,
            'impact': impact,
            'critical': self.damage > 80  # Dégâts critiques
        }
    
    def update_tire_wear(self, amount):
        """
        Met à jour l'usure des pneus
        
        Args:
            amount (int): Quantité d'usure à ajouter (0-100)
            
        Returns:
            dict: État des pneus
        """
        self.tire_wear = min(100, max(0, self.tire_wear + amount))
        
        # Impact sur les performances
        impact = {}
        
        if self.tire_wear > 30:
            # Réduction des performances proportionnelle à l'usure
            factor = self.tire_wear / 200  # 0.15 à 0.5
            impact['cornering'] = int(self.stats['cornering'] * factor)
            impact['braking'] = int(self.stats['braking'] * factor * 0.7)
        
        # Risque accru de dérapages avec pneus usés
        grip_loss = self.tire_wear / 2
        
        return {
            'wear': self.tire_wear,
            'impact': impact,
            'critical': self.tire_wear > 90,  # Pneus critiques
            'grip_loss': grip_loss
        }
    
    def update_fuel(self, consumption):
        """
        Met à jour le niveau de carburant
        
        Args:
            consumption (float): Consommation de carburant (0-100)
            
        Returns:
            dict: État du carburant
        """
        self.fuel_level = max(0, self.fuel_level - consumption)
        
        # Impact sur les performances
        impact = {}
        
        # Voiture plus légère avec moins de carburant = plus rapide
        if self.fuel_level < 50:
            weight_factor = (50 - self.fuel_level) / 100  # 0 à 0.5
            impact['acceleration'] = int(self.stats['acceleration'] * weight_factor * 0.1)  # +10% max
            impact['top_speed'] = int(self.stats['top_speed'] * weight_factor * 0.05)  # +5% max
        
        return {
            'level': self.fuel_level,
            'impact': impact,
            'critical': self.fuel_level < 10  # Niveau critique
        }
    
    def get_performance(self):
        """
        Calcule les performances actuelles de la voiture
        
        Returns:
            dict: Performances actuelles
        """
        # Performances de base
        performance = self.stats.copy()
        
        # Impact des dégâts
        if self.damage > 0:
            damage_factor = self.damage / 100
            performance['top_speed'] -= int(performance['top_speed'] * damage_factor * 0.3)
            performance['acceleration'] -= int(performance['acceleration'] * damage_factor * 0.4)
            performance['cornering'] -= int(performance['cornering'] * damage_factor * 0.5)
            performance['reliability'] -= int(performance['reliability'] * damage_factor * 0.7)
        
        # Impact de l'usure des pneus
        if self.tire_wear > 0:
            tire_factor = self.tire_wear / 100
            performance['cornering'] -= int(performance['cornering'] * tire_factor * 0.6)
            performance['braking'] -= int(performance['braking'] * tire_factor * 0.5)
        
        # Impact du niveau de carburant
        if self.fuel_level < 100:
            # Moins de carburant = voiture plus légère
            fuel_factor = (100 - self.fuel_level) / 100
            performance['acceleration'] += int(performance['acceleration'] * fuel_factor * 0.15)
            performance['top_speed'] += int(performance['top_speed'] * fuel_factor * 0.05)
        
        return performance
    
    def reset_for_race(self):
        """Réinitialise l'état de la voiture pour une nouvelle course"""
        self.damage = 0
        self.tire_wear = 0
        self.fuel_level = 100
    
    def change_tires(self, compound="medium"):
        """
        Change les pneus de la voiture
        
        Args:
            compound (str): Type de pneus ('soft', 'medium', 'hard', 'wet')
            
        Returns:
            dict: Nouvelles caractéristiques des pneus
        """
        self.tire_wear = 0
        
        # Caractéristiques selon le type de pneus
        tire_stats = {
            'soft': {
                'grip': 90,
                'durability': 30,
                'optimal_temp': 'high'
            },
            'medium': {
                'grip': 75,
                'durability': 60,
                'optimal_temp': 'medium'
            },
            'hard': {
                'grip': 60,
                'durability': 90,
                'optimal_temp': 'low'
            },
            'wet': {
                'grip': 70,
                'durability': 50,
                'optimal_temp': 'low',
                'rain_performance': 95
            }
        }
        
        return tire_stats.get(compound, tire_stats['medium'])
    
    def repair(self, amount):
        """
        Répare la voiture
        
        Args:
            amount (int): Quantité de réparation (0-100)
            
        Returns:
            int: Niveau de dégâts restant
        """
        self.damage = max(0, self.damage - amount)
        return self.damage