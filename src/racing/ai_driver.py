#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestion du comportement des pilotes IA
"""

import random

class AIDriver:
    """Classe représentant un pilote IA"""
    
    def __init__(self, driver_id, name, team, skills):
        """
        Initialisation d'un pilote IA
        
        Args:
            driver_id (str): ID du pilote
            name (str): Nom du pilote
            team (str): Nom de l'équipe
            skills (float): Niveau de compétence global (0-100)
        """
        self.id = driver_id
        self.name = name
        self.team = team
        self.overall_skill = skills
        
        # Générer des compétences spécifiques
        self.skills = self._generate_skills()
        
        # État actuel en course
        self.position = 0
        self.tire_wear = 0
        self.car_damage = 0
        
        # Style de pilotage (influencant les décisions)
        self.aggression = random.randint(30, 100)  # 0-100
        self.consistency = random.randint(30, 100)  # 0-100
        self.wet_weather_skill = random.randint(30, 100)  # 0-100
        
        # Traits de personnalité (influencant le comportement)
        self.traits = self._generate_traits()
    
    def _generate_skills(self):
        """
        Génère les compétences spécifiques du pilote
        
        Returns:
            dict: Compétences spécifiques
        """
        # Base de compétence
        base = self.overall_skill
        
        # Variation autour de la base
        variation = 15
        
        skills = {
            'pace': max(1, min(100, base + random.randint(-variation, variation))),
            'overtaking': max(1, min(100, base + random.randint(-variation, variation))),
            'defending': max(1, min(100, base + random.randint(-variation, variation))),
            'consistency': max(1, min(100, base + random.randint(-variation, variation))),
            'tire_management': max(1, min(100, base + random.randint(-variation, variation))),
            'wet_driving': max(1, min(100, base + random.randint(-variation, variation))),
            'technical_feedback': max(1, min(100, base + random.randint(-variation, variation))),
            'starts': max(1, min(100, base + random.randint(-variation, variation)))
        }
        
        return skills
    
    def _generate_traits(self):
        """
        Génère les traits de personnalité du pilote
        
        Returns:
            dict: Traits de personnalité
        """
        traits = {
            'aggressive': random.random() > 0.5,         # Pilote agressif (plus de dépassements risqués)
            'cautious': random.random() > 0.7,           # Pilote prudent (moins d'erreurs)
            'tire_saver': random.random() > 0.6,         # Préserve les pneus
            'rain_master': random.random() > 0.8,        # Expert sous la pluie
            'good_starter': random.random() > 0.5,       # Bon au départ
            'pressure_sensitive': random.random() > 0.7,  # Sensible à la pression (fait des erreurs en tête/fin de course)
            'comeback_king': random.random() > 0.8       # Performant en remontée
        }
        
        return traits
    
    def decide_action(self, race_state, available_actions):
        """
        Décide de l'action à effectuer en fonction de l'état de la course
        
        Args:
            race_state (dict): État actuel de la course
            available_actions (list): Actions disponibles
            
        Returns:
            str: ID de l'action choisie
        """
        if not available_actions:
            return None
        
        # Récupérer la position actuelle
        position = race_state.get('positions', {}).get(self.id, 0)
        self.position = position
        
        # Récupérer le tour actuel et le nombre total de tours
        current_lap = race_state.get('lap', 1)
        total_laps = race_state.get('total_laps', 1)
        
        # Phase de la course
        race_progress = current_lap / total_laps
        is_early_race = race_progress < 0.3
        is_mid_race = 0.3 <= race_progress < 0.7
        is_late_race = race_progress >= 0.7
        
        # Conditions météo
        is_wet = race_state.get('weather', {}).get('rain', 0) > 0
        
        # Récupérer l'usure des pneus
        tire_wear = self.tire_wear
        
        # Stratégie de base
        action_weights = {}
        
        # Initialiser les poids pour toutes les actions disponibles
        for action in available_actions:
            action_weights[action] = 10  # Poids de base
        
        # Modifier les poids en fonction du contexte
        
        # Début de course: plus de dépassements, poussée du rythme
        if is_early_race:
            for action in action_weights:
                if action.startswith('overtake'):
                    action_weights[action] += 15
                if action == 'push_pace':
                    action_weights[action] += 10
        
        # Milieu de course: équilibrer entre attaque et conservation
        if is_mid_race:
            for action in action_weights:
                if action == 'push_pace':
                    action_weights[action] += 5
                if action == 'conserve_tires':
                    action_weights[action] += 5
        
        # Fin de course: plus agressif, moins de conservation
        if is_late_race:
            for action in action_weights:
                if action.startswith('overtake') or action.startswith('defend'):
                    action_weights[action] += 20
                if action == 'conserve_tires':
                    action_weights[action] -= 5
        
        # Pluie: privilégier les pilotes doués sur le mouillé
        if is_wet:
            wet_skill_factor = self.skills['wet_driving'] / 50  # 0.4 à 2.0
            for action in action_weights:
                if action == 'wet_overtake':
                    action_weights[action] += 15 * wet_skill_factor
                if action.startswith('overtake') and action != 'wet_overtake':
                    action_weights[action] -= 10
        
        # Usure des pneus: privilégier la conservation si usure importante
        if tire_wear > 50:
            for action in action_weights:
                if action == 'conserve_tires':
                    action_weights[action] += tire_wear / 5
                if action.startswith('overtake'):
                    action_weights[action] -= tire_wear / 10
        
        # Position: stratégie différente selon la position
        if position <= 3:  # Podium
            for action in action_weights:
                if action.startswith('defend'):
                    action_weights[action] += 15
        elif position <= 10:  # Points
            for action in action_weights:
                if action.startswith('overtake'):
                    action_weights[action] += 10
        else:  # Hors des points
            for action in action_weights:
                if action.startswith('overtake'):
                    action_weights[action] += 20
                if action == 'push_pace':
                    action_weights[action] += 15
        
        # Appliquer les traits de personnalité
        if self.traits.get('aggressive', False):
            for action in action_weights:
                if action in ['overtake_risky', 'push_pace', 'aggressive_curbs']:
                    action_weights[action] += 15
        
        if self.traits.get('cautious', False):
            for action in action_weights:
                if action in ['overtake_risky', 'aggressive_curbs']:
                    action_weights[action] -= 10
                if action in ['conserve_tires', 'defend_normal']:
                    action_weights[action] += 10
        
        if self.traits.get('tire_saver', False) and tire_wear > 30:
            for action in action_weights:
                if action == 'conserve_tires':
                    action_weights[action] += 20
        
        if self.traits.get('rain_master', False) and is_wet:
            for action in action_weights:
                if action == 'wet_overtake':
                    action_weights[action] += 25
        
        if self.traits.get('pressure_sensitive', False):
            if position <= 3 or is_late_race:
                for action in action_weights:
                    if action in ['overtake_risky', 'aggressive_curbs']:
                        action_weights[action] -= 15
        
        if self.traits.get('comeback_king', False) and position > 10:
            for action in action_weights:
                if action.startswith('overtake'):
                    action_weights[action] += 20
        
        # Ajuster les poids en fonction des compétences
        for action in action_weights:
            skill_factor = 1.0
            
            if action.startswith('overtake'):
                skill_factor = self.skills['overtaking'] / 50
            elif action.startswith('defend'):
                skill_factor = self.skills['defending'] / 50
            elif action == 'push_pace':
                skill_factor = self.skills['pace'] / 50
            elif action == 'conserve_tires':
                skill_factor = self.skills['tire_management'] / 50
            elif action == 'wet_overtake':
                skill_factor = self.skills['wet_driving'] / 50
            
            action_weights[action] *= skill_factor
        
        # Ajouter un peu d'aléatoire pour éviter le comportement déterministe
        for action in action_weights:
            action_weights[action] += random.randint(-5, 5)
            # Garantir un minimum de 1
            action_weights[action] = max(1, action_weights[action])
        
        # Sélectionner une action au hasard, pondérée par les poids
        total_weight = sum(action_weights.values())
        choice = random.uniform(0, total_weight)
        
        current_weight = 0
        for action, weight in action_weights.items():
            current_weight += weight
            if current_weight >= choice:
                return action
        
        # Par défaut, retourner une action aléatoire
        return random.choice(available_actions)
    
    def update_state(self, new_position, tire_wear_increase, damage_increase):
        """
        Met à jour l'état du pilote après une action
        
        Args:
            new_position (int): Nouvelle position
            tire_wear_increase (float): Augmentation de l'usure des pneus
            damage_increase (float): Augmentation des dégâts sur la voiture
        """
        self.position = new_position
        self.tire_wear += tire_wear_increase
        self.car_damage += damage_increase
    
    def reset_for_race(self):
        """Réinitialise l'état du pilote pour une nouvelle course"""
        self.position = 0
        self.tire_wear = 0
        self.car_damage = 0


class AIDriverManager:
    """Gestionnaire de pilotes IA pour une course"""
    
    def __init__(self, drivers_data):
        """
        Initialisation du gestionnaire
        
        Args:
            drivers_data (dict): Données des pilotes
        """
        self.ai_drivers = {}
        
        # Créer les pilotes IA
        for driver_id, data in drivers_data.items():
            if driver_id != 'player':  # Ignorer le joueur
                self.ai_drivers[driver_id] = AIDriver(
                    driver_id,
                    data['name'],
                    data['team'],
                    data['skills']
                )
    
    def simulate_ai_actions(self, race_state, available_actions_map):
        """
        Simule les actions des pilotes IA
        
        Args:
            race_state (dict): État actuel de la course
            available_actions_map (dict): Actions disponibles pour chaque pilote
            
        Returns:
            dict: Actions choisies par les pilotes IA
        """
        ai_actions = {}
        
        for driver_id, ai_driver in self.ai_drivers.items():
            available_actions = available_actions_map.get(driver_id, [])
            chosen_action = ai_driver.decide_action(race_state, available_actions)
            
            if chosen_action:
                ai_actions[driver_id] = chosen_action
        
        return ai_actions
    
    def update_ai_states(self, race_results):
        """
        Met à jour l'état des pilotes IA après une course
        
        Args:
            race_results (dict): Résultats de la course
        """
        positions = race_results.get('positions', {})
        
        for driver_id, ai_driver in self.ai_drivers.items():
            position = positions.get(driver_id, 0)
            
            # Estimer l'usure des pneus et les dégâts en fonction du style de pilotage
            tire_wear = 0
            damage = 0
            
            if ai_driver.traits.get('aggressive', False):
                tire_wear += 20 + random.randint(0, 10)
                damage += random.randint(0, 15)
            else:
                tire_wear += 10 + random.randint(0, 5)
                damage += random.randint(0, 5)
            
            # Les pilotes qui préservent les pneus ont moins d'usure
            if ai_driver.traits.get('tire_saver', False):
                tire_wear = max(0, tire_wear - random.randint(5, 15))
            
            # Mettre à jour l'état du pilote
            ai_driver.update_state(position, tire_wear, damage)
    
    def reset_for_race(self):
        """Réinitialise l'état de tous les pilotes IA pour une nouvelle course"""
        for ai_driver in self.ai_drivers.values():
            ai_driver.reset_for_race()