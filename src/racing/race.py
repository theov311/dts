#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classe gérant une course individuelle et ses événements
"""

import random
from src.racing.event import RaceEvent

class Race:
    """Classe représentant une course de Formule"""
    
    def __init__(self, name, circuit, category, drivers, player):
        """
        Initialisation d'une course
        
        Args:
            name (str): Nom de la course
            circuit (dict): Informations sur le circuit
            category (str): Catégorie ('f3', 'f2', 'f1')
            drivers (dict): Dictionnaire des pilotes
            player (Player): Joueur/pilote
        """
        self.name = name
        self.circuit = circuit
        self.category = category
        self.drivers = drivers
        self.player = player
        
        # Définir le nombre total de tours selon la catégorie
        self.total_laps = {
            'f3': 15,
            'f2': 25,
            'f1': 50
        }.get(category, 20)
        
        # Grille de départ (sera définie après les qualifications)
        self.grid = []
        
        # Positions actuelles des pilotes (sera mise à jour pendant la course)
        self.positions = {}
        
        # État de la course
        self.current_lap = 0
        self.is_finished = False
        
        # Facteurs météo - Initialiser avant de générer les événements
        self.weather = self._generate_weather()
        
        # Temps de course cumulés pour calculer les écarts
        self.race_times = {driver_id: 0.0 for driver_id in self.drivers}
        
        # Événements de course disponibles
        self.available_events = self._generate_events()
        
        # Historique des événements
        self.event_history = []
        
        # Incidents de course
        self.incidents = []
        
        # Qualifications
        self.qualifying_results = {}
        
        # État de la voiture du joueur
        self.car_status = {
            'tire_wear': 0,
            'fuel_level': 100,
            'damage': 0
        }
    
    def _generate_events(self):
        """
        Génère les événements disponibles pour cette course
        
        Returns:
            list: Liste d'événements de course
        """
        # Événements de base toujours disponibles
        events = [
            RaceEvent("overtake_normal", "Dépassement standard", "Tentative de dépassement standard", 70),
            RaceEvent("overtake_risky", "Dépassement risqué", "Tentative de dépassement audacieuse", 50),
            RaceEvent("defend_normal", "Défense de position", "Défense de position standard", 75),
            RaceEvent("defend_aggressive", "Défense agressive", "Défense de position agressive", 60),
            RaceEvent("push_pace", "Pousser le rythme", "Augmentation du rythme pour gagner du temps", 80),
            RaceEvent("conserve_tires", "Préserver les pneus", "Conduite plus douce pour préserver les pneus", 90),
            RaceEvent("fuel_saving", "Économie de carburant", "Réduction de la consommation de carburant", 85)
        ]
        
        # Événements supplémentaires basés sur le circuit
        circuit_difficulty = self.circuit.get('difficulty', 5)
        
        if circuit_difficulty >= 7:
            events.append(RaceEvent("risky_corner", "Virage risqué", "Prise de risque dans un virage difficile", 60))
        
        if circuit_difficulty >= 8:
            events.append(RaceEvent("aggressive_curbs", "Utilisation agressive des vibreurs", "Passage agressif sur les vibreurs", 55))
        
        # Événements météo
        if self.weather.get('rain', 0) > 0:
            events.append(RaceEvent("wet_overtake", "Dépassement sous la pluie", "Tentative de dépassement sur piste mouillée", 50))
        
        return events
    
    def _generate_weather(self):
        """
        Génère les conditions météo pour la course
        
        Returns:
            dict: Conditions météo
        """
        # Probabilité de pluie (0-100)
        rain_chance = random.randint(0, 100)
        
        if rain_chance < 70:  # 70% de chance de temps sec
            return {
                'condition': 'Sec',
                'rain': 0,
                'temperature': random.randint(15, 35)  # Température en °C
            }
        elif rain_chance < 90:  # 20% de chance de pluie légère
            return {
                'condition': 'Pluie légère',
                'rain': random.randint(1, 3),  # Intensité de la pluie (1-10)
                'temperature': random.randint(10, 25)
            }
        else:  # 10% de chance de pluie forte
            return {
                'condition': 'Pluie forte',
                'rain': random.randint(4, 10),
                'temperature': random.randint(5, 20)
            }
    
    def _calculate_time_gaps(self):
        """
        Calcule les écarts de temps entre les pilotes
        
        Returns:
            dict: Écarts de temps
        """
        time_gaps = {}
        
        # Trouver le leader
        positions = sorted(self.positions.items(), key=lambda x: x[1])
        if not positions:
            return time_gaps
            
        leader_id = positions[0][0]
        leader_time = self.race_times[leader_id]
        
        # Calculer les écarts
        for driver_id, time in self.race_times.items():
            if driver_id != leader_id:
                time_gaps[driver_id] = time - leader_time
        
        return time_gaps
    
    def _update_race_times(self):
        """
        Met à jour les temps de course des pilotes
        """
        # Temps de base pour un tour (60-120 secondes selon la catégorie)
        base_lap_time = {
            'f3': 90.0,
            'f2': 80.0,
            'f1': 70.0
        }.get(self.category, 90.0)
        
        # Pour chaque pilote
        for driver_id in self.drivers:
            # Base du temps
            lap_time = base_lap_time
            
            # Facteurs influant sur le temps
            skill_factor = 1.0
            position_factor = 1.0
            car_factor = 1.0
            random_factor = random.uniform(0.98, 1.02)  # ±2% d'aléatoire
            
            if driver_id == 'player':
                # Facteur compétence du joueur
                skill_factor = max(0.8, min(1.2, 1.2 - (self.player.skills.overall / 100)))
                
                # Facteur position
                position = self.positions.get(driver_id, 0)
                position_factor = 1.0 + (position / 100)  # Trafic ralentit
                
                # Facteur voiture du joueur (état)
                tire_factor = 1.0 + (self.car_status.get('tire_wear', 0) / 200)  # Pneus usés = plus lent
                damage_factor = 1.0 + (self.car_status.get('damage', 0) / 150)   # Dégâts = plus lent
                car_factor = tire_factor * damage_factor
            else:
                # Facteur compétence IA
                driver_info = self.drivers[driver_id]
                skill_factor = max(0.8, min(1.2, 1.2 - (driver_info['skills'] / 100)))
                
                # Facteur position
                position = self.positions.get(driver_id, 0)
                position_factor = 1.0 + (position / 100)
            
            # Temps final du tour
            final_lap_time = lap_time * skill_factor * car_factor * position_factor * random_factor
            
            # Ajouter au temps total
            self.race_times[driver_id] += final_lap_time
    
    def run_qualifying(self):
        """
        Exécute la séance de qualifications
        
        Returns:
            dict: Résultats des qualifications
        """
        quali_times = {}
        
        # Pour chaque pilote, générer un temps de qualification
        for driver_id, driver_info in self.drivers.items():
            # Base de temps (en secondes) selon le circuit
            base_time = 60 + (self.circuit['difficulty'] * 2)
            
            # Facteur de compétence
            skill_factor = 1.0 - (driver_info['skills'] / 200)  # 0.5 à 0.95
            
            # Facteur équipe (voiture)
            team_name = driver_info['team']
            team = next((t for t in [self.player.team] if t.name == team_name), None)
            car_factor = 1.0
            if team:
                car_factor = 1.0 - (team.performance / 200)  # 0.5 à 0.95
            
            # Facteur aléatoire (erreurs, tours propres, etc.)
            random_factor = random.uniform(0.98, 1.02)
            
            # Facteur météo
            weather_factor = 1.0
            if self.weather['rain'] > 0:
                # La pluie amplifie les différences de compétence
                weather_skill = getattr(self.player.skills, 'wet_driving', 50) if driver_id == 'player' else random.randint(20, 90)
                weather_factor = 1.0 + ((10 - weather_skill / 10) * (self.weather['rain'] / 30))
            
            # Calcul du temps final
            lap_time = base_time * skill_factor * car_factor * random_factor * weather_factor
            
            # Pour le joueur, appliquer sa compétence réelle
            if driver_id == 'player':
                player_skill_factor = 1.0 - (self.player.skills.overall / 200)
                player_specific_skills = 1.0 - ((self.player.skills.pace + self.player.skills.consistency) / 400)
                lap_time = base_time * player_skill_factor * player_specific_skills * car_factor * random_factor * weather_factor
            
            # Enregistrer le temps
            quali_times[driver_id] = lap_time
        
        # Trier les temps
        sorted_times = sorted(quali_times.items(), key=lambda x: x[1])
        
        # Construire la grille de départ
        self.grid = [driver_id for driver_id, _ in sorted_times]
        self.qualifying_results = {driver_id: position + 1 for position, (driver_id, _) in enumerate(sorted_times)}
        
        return {
            'grid': self.grid,
            'times': dict(sorted_times),
            'player_position': self.qualifying_results.get('player', 0)
        }
    
    def start_race(self):
        """
        Démarre la course
        
        Returns:
            dict: État initial de la course
        """
        # Si les qualifications n'ont pas encore eu lieu
        if not self.grid:
            self.run_qualifying()
        
        # Initialiser les positions de départ
        self.positions = {driver_id: position + 1 for position, driver_id in enumerate(self.grid)}
        self.current_lap = 1
        
        # Réinitialiser les temps de course
        self.race_times = {driver_id: 0.0 for driver_id in self.drivers}
        
        # Réinitialiser l'état de la voiture
        self.car_status = {
            'tire_wear': 0,
            'fuel_level': 100,
            'damage': 0
        }
        
        # Calculer les écarts initiaux (tous à 0)
        time_gaps = self._calculate_time_gaps()
        
        return {
            'lap': self.current_lap,
            'total_laps': self.total_laps,
            'positions': self.positions,
            'player_position': self.positions.get('player', 0),
            'weather': self.weather,
            'time_gaps': time_gaps,
            'car_status': self.car_status
        }
    
    def get_available_actions(self, driver_id):
        """
        Récupère les actions disponibles pour un pilote
        
        Args:
            driver_id (str): ID du pilote
            
        Returns:
            list: Actions disponibles
        """
        # Filtrer les événements en fonction du contexte de course
        position = self.positions.get(driver_id, 0)
        actions = []
        
        # Actions de base toujours disponibles
        actions.append("push_pace")
        actions.append("conserve_tires")
        
        # Actions de dépassement (si le pilote n'est pas en tête)
        if position > 1:
            actions.extend(["overtake_normal", "overtake_risky"])
            
            # Dépassement sous la pluie si applicable
            if self.weather.get('rain', 0) > 0 and "wet_overtake" in [e.id for e in self.available_events]:
                actions.append("wet_overtake")
        
        # Actions de défense (si le pilote n'est pas dernier)
        if position < len(self.drivers):
            actions.extend(["defend_normal", "defend_aggressive"])
        
        # Actions spécifiques au circuit
        if "risky_corner" in [e.id for e in self.available_events]:
            actions.append("risky_corner")
        
        if "aggressive_curbs" in [e.id for e in self.available_events]:
            actions.append("aggressive_curbs")
        
        return actions
    
    def execute_player_action(self, action_id):
        """
        Exécute une action du joueur
        
        Args:
            action_id (str): ID de l'action à exécuter
            
        Returns:
            dict: Résultat de l'action
        """
        # Trouver l'événement correspondant
        event = next((e for e in self.available_events if e.id == action_id), None)
        
        if not event:
            return {
                'success': False,
                'message': "Action non disponible"
            }
        
        # Calculer les chances de réussite en fonction des compétences du joueur
        base_success_chance = event.success_chance
        player_skill = 0
        
        # Ajuster les chances en fonction de la compétence spécifique
        if action_id.startswith("overtake"):
            player_skill = self.player.skills.overtaking
        elif action_id.startswith("defend"):
            player_skill = self.player.skills.defending
        elif action_id == "push_pace":
            player_skill = self.player.skills.pace
        elif action_id == "conserve_tires":
            player_skill = self.player.skills.tire_management
        elif action_id == "wet_overtake":
            player_skill = self.player.skills.wet_driving
        else:
            player_skill = self.player.skills.overall
        
        # Ajuster les chances de réussite
        adjusted_chance = base_success_chance + (player_skill - 50) / 5
        adjusted_chance = max(10, min(95, adjusted_chance))  # Limiter entre 10% et 95%
        
        # Déterminer si l'action est réussie
        success = random.randint(1, 100) <= adjusted_chance
        
        result = {
            'action': action_id,
            'success': success,
            'position_before': self.positions.get('player', 0)
        }
        
        # Effets de l'action
        if success:
            # Actions réussies
            if action_id.startswith("overtake"):
                # Gagner une position
                self._update_position('player', -1)
                result['message'] = "Dépassement réussi!"
                
                # Amélioration de compétence
                result['skill_improvements'] = {
                    'overtaking': random.uniform(0.1, 0.3)
                }
                
                # Usure des pneus
                result['tire_wear'] = random.randint(2, 5)
            
            elif action_id.startswith("defend"):
                # Maintenir sa position
                result['message'] = "Défense réussie!"
                
                # Amélioration de compétence
                result['skill_improvements'] = {
                    'defending': random.uniform(0.1, 0.3)
                }
                
                # Usure des pneus
                result['tire_wear'] = random.randint(1, 3)
            
            elif action_id == "push_pace":
                # Chance de gagner une position ou creuser l'écart
                if random.random() < 0.4:  # 40% de chance de gagner une position
                    self._update_position('player', -1)
                    result['message'] = "Rythme augmenté, vous gagnez une position!"
                else:
                    result['message'] = "Rythme augmenté, vous creusez l'écart!"
                
                # Amélioration de compétence
                result['skill_improvements'] = {
                    'pace': random.uniform(0.1, 0.3)
                }
                
                # Augmentation de l'usure des pneus
                result['tire_wear'] = random.randint(3, 7)
            
            elif action_id == "conserve_tires":
                result['message'] = "Vous préservez vos pneus avec succès."
                
                # Amélioration de compétence
                result['skill_improvements'] = {
                    'tire_management': random.uniform(0.1, 0.3)
                }
                
                # Réduction de l'usure des pneus
                result['tire_wear'] = -random.randint(1, 3)  # Valeur négative pour réduire l'usure
            
            elif action_id == "wet_overtake":
                # Gain de position sur piste mouillée
                self._update_position('player', -1)
                result['message'] = "Dépassement sous la pluie réussi!"
                
                # Amélioration de compétence
                result['skill_improvements'] = {
                    'wet_driving': random.uniform(0.2, 0.5),
                    'overtaking': random.uniform(0.1, 0.2)
                }
                
                # Augmentation de l'usure des pneus
                result['tire_wear'] = random.randint(5, 10)
            
            elif action_id == "risky_corner":
                # Chance de gagner une position
                if random.random() < 0.6:  # 60% de chance de gagner une position
                    self._update_position('player', -1)
                    result['message'] = "Vous négociez parfaitement le virage difficile et gagnez une position!"
                else:
                    result['message'] = "Vous négociez bien le virage difficile."
                
                # Augmentation de l'usure des pneus
                result['tire_wear'] = random.randint(2, 5)
            
            elif action_id == "aggressive_curbs":
                # Chance de gagner du temps et une position
                if random.random() < 0.5:  # 50% de chance de gagner une position
                    self._update_position('player', -1)
                    result['message'] = "Passage agressif sur les vibreurs réussi, vous gagnez une position!"
                else:
                    result['message'] = "Passage agressif sur les vibreurs réussi."
                
                # Augmentation de l'usure des pneus et risque de dégâts
                result['tire_wear'] = random.randint(3, 8)
                if random.random() < 0.3:
                    result['car_damage'] = random.randint(1, 5)
        else:
            # Actions échouées
            if action_id.startswith("overtake"):
                if action_id == "overtake_risky" and random.random() < 0.3:
                    # Risque d'accident en cas d'échec de dépassement risqué
                    self._update_position('player', 3)  # Perte de positions importante
                    result['message'] = "Dépassement risqué raté! Vous perdez plusieurs positions!"
                    
                    # Risque de dégâts
                    if random.random() < 0.4:
                        result['car_damage'] = random.randint(10, 30)
                        result['message'] += " Votre voiture est endommagée."
                    
                    # Usure des pneus
                    result['tire_wear'] = random.randint(8, 15)
                else:
                    result['message'] = "Dépassement raté, vous restez derrière."
                    result['tire_wear'] = random.randint(3, 8)
            
            elif action_id.startswith("defend"):
                # Perte de position
                self._update_position('player', 1)
                result['message'] = "Défense échouée, vous perdez une position."
                result['tire_wear'] = random.randint(2, 6)
            
            elif action_id == "push_pace":
                # Risque d'usure des pneus
                result['message'] = "Vous poussez trop fort et usez vos pneus."
                result['tire_wear'] = random.randint(8, 15)
            
            elif action_id == "conserve_tires":
                # Perte de temps
                result['message'] = "Vous roulez trop lentement et perdez du temps."
                
                # Risque de perdre une position
                if random.random() < 0.3:  # 30% de chance de perdre une position
                    self._update_position('player', 1)
                    result['message'] += " Vous perdez une position."
                
                # Faible usure des pneus malgré l'échec
                result['tire_wear'] = random.randint(1, 3)
            
            elif action_id == "wet_overtake":
                # Échec de dépassement sous la pluie
                if random.random() < 0.4:  # 40% de chance d'accident
                    self._update_position('player', random.randint(2, 5))  # Perte de plusieurs positions
                    result['message'] = "Dépassement sous la pluie raté! Vous partez en aquaplaning et perdez plusieurs positions!"
                    
                    # Risque élevé de dégâts
                    if random.random() < 0.7:
                        result['car_damage'] = random.randint(15, 40)
                        result['message'] += " Votre voiture est sérieusement endommagée."
                    
                    # Usure élevée des pneus
                    result['tire_wear'] = random.randint(10, 20)
                else:
                    result['message'] = "Dépassement sous la pluie raté, vous restez dans le spray."
                    result['tire_wear'] = random.randint(5, 10)
            
            elif action_id == "risky_corner":
                # Échec dans un virage difficile
                self._update_position('player', random.randint(1, 2))
                result['message'] = "Vous ratez le virage difficile et perdez des positions!"
                
                # Risque de dégâts
                if random.random() < 0.5:
                    result['car_damage'] = random.randint(5, 20)
                    result['message'] += " Votre voiture est légèrement endommagée."
                
                # Usure des pneus
                result['tire_wear'] = random.randint(5, 12)
            
            elif action_id == "aggressive_curbs":
                # Échec avec les vibreurs
                if random.random() < 0.6:  # 60% de chance de dégâts
                    result['car_damage'] = random.randint(10, 25)
                    result['message'] = "Vous heurtez trop violemment les vibreurs et endommagez votre voiture!"
                else:
                    result['message'] = "Vous ne gagnez pas de temps avec les vibreurs."
                
                # Usure des pneus
                result['tire_wear'] = random.randint(5, 15)
        
        # Mettre à jour l'état de la voiture
        self.car_status['tire_wear'] = min(100, max(0, self.car_status['tire_wear'] + result.get('tire_wear', 0)))
        self.car_status['damage'] = min(100, self.car_status['damage'] + result.get('car_damage', 0))
        
        # Consommation de carburant (base par tour + extra selon l'action)
        fuel_consumption = 1.5  # Consommation de base
        if action_id == "push_pace":
            fuel_consumption += 1.0  # Plus de consommation en poussant
        elif action_id == "fuel_saving":
            fuel_consumption -= 0.8  # Moins de consommation en économisant
            
        self.car_status['fuel_level'] = max(0, self.car_status['fuel_level'] - fuel_consumption)
        
        # Mettre à jour la position après l'action
        result['position_after'] = self.positions.get('player', 0)
        
        # Enregistrer l'événement
        self.event_history.append({
            'lap': self.current_lap,
            'action': action_id,
            'success': success,
            'position_change': result['position_before'] - result['position_after']
        })
        
        return result
    
    def _update_position(self, driver_id, delta):
        """
        Met à jour la position d'un pilote
        
        Args:
            driver_id (str): ID du pilote
            delta (int): Changement de position (négatif pour gagner des places)
        """
        current_position = self.positions.get(driver_id, 0)
        new_position = max(1, min(len(self.drivers), current_position + delta))
        
        # Si la position ne change pas, rien à faire
        if new_position == current_position:
            return
        
        # Mettre à jour les positions des autres pilotes concernés
        if delta < 0:  # Gagner des positions
            for other_id, pos in self.positions.items():
                if other_id != driver_id and pos < current_position and pos >= new_position:
                    self.positions[other_id] = pos + 1
        else:  # Perdre des positions
            for other_id, pos in self.positions.items():
                if other_id != driver_id and pos > current_position and pos <= new_position:
                    self.positions[other_id] = pos - 1
        
        # Mettre à jour la position du pilote
        self.positions[driver_id] = new_position
    
    def advance_lap(self):
        """
        Avance d'un tour et simule les actions des IA
        
        Returns:
            dict: État de la course après le tour
        """
        # Mettre à jour les temps de course
        self._update_race_times()
        
        # Calculer les écarts de temps
        time_gaps = self._calculate_time_gaps()
        
        # Simuler les actions des IA
        self._simulate_ai_actions()
        
        # Passer au tour suivant
        self.current_lap += 1
        
        # Consommation de carburant de base pour le joueur
        base_fuel_consumption = 2.0
        self.car_status['fuel_level'] = max(0, self.car_status['fuel_level'] - base_fuel_consumption)
        
        # Usure de base des pneus
        base_tire_wear = random.randint(1, 3)
        self.car_status['tire_wear'] = min(100, self.car_status['tire_wear'] + base_tire_wear)
        
        # Vérifier si la course est terminée
        if self.current_lap > self.total_laps:
            self.is_finished = True
            return self.get_race_results()
        
        # État de la course
        return {
            'lap': self.current_lap,
            'total_laps': self.total_laps,
            'positions': self.positions,
            'player_position': self.positions.get('player', 0),
            'is_finished': self.is_finished,
            'time_gaps': time_gaps,
            'car_status': self.car_status,
            'weather': self.weather
        }
    
    def _simulate_ai_actions(self):
        """Simule les actions des pilotes IA pendant un tour"""
        # Pour chaque pilote IA, simuler une action
        for driver_id, driver_info in self.drivers.items():
            if driver_id == 'player':
                continue  # Sauter le joueur
            
            # Récupérer les actions disponibles
            available_actions = self.get_available_actions(driver_id)
            
            if not available_actions:
                continue
            
            # Choisir une action au hasard, pondérée par le niveau de compétence
            skill_level = driver_info['skills']
            
            # Les IA plus compétentes font des choix plus stratégiques
            if skill_level > 70:  # Pilotes très compétents
                # Favoriser les dépassements si en position de le faire
                if self.positions.get(driver_id, 0) > 1:
                    overtake_actions = [a for a in available_actions if a.startswith('overtake')]
                    if overtake_actions and random.random() < 0.7:  # 70% de chance de tenter un dépassement
                        action_id = random.choice(overtake_actions)
                    else:
                        action_id = random.choice(available_actions)
                else:
                    # Favoriser la défense si en tête
                    defend_actions = [a for a in available_actions if a.startswith('defend')]
                    if defend_actions and random.random() < 0.8:  # 80% de chance de défendre
                        action_id = random.choice(defend_actions)
                    else:
                        action_id = random.choice(available_actions)
            else:  # Pilotes moins compétents - plus aléatoire
                action_id = random.choice(available_actions)
            
            # Simuler l'action
            event = next((e for e in self.available_events if e.id == action_id), None)
            
            if not event:
                continue
            
            # Calculer les chances de réussite
            base_success_chance = event.success_chance
            adjusted_chance = base_success_chance + (skill_level - 50) / 5
            adjusted_chance = max(10, min(95, adjusted_chance))
            
            # Déterminer si l'action est réussie
            success = random.randint(1, 100) <= adjusted_chance
            
            # Appliquer les effets de l'action
            if success:
                if action_id.startswith("overtake"):
                    # Gagner une position
                    self._update_position(driver_id, -1)
                elif action_id.startswith("defend"):
                    # Rien à faire, juste défendre
                    pass
                elif action_id == "push_pace" and random.random() < 0.3:
                    # Chance de gagner une position
                    self._update_position(driver_id, -1)
            else:
                if action_id == "overtake_risky" and random.random() < 0.3:
                    # Perte de positions en cas d'échec de dépassement risqué
                    self._update_position(driver_id, random.randint(1, 3))
                elif action_id.startswith("defend"):
                    # Perte de position en cas d'échec de défense
                    self._update_position(driver_id, 1)
    
    def get_race_results(self):
        """
        Récupère les résultats finaux de la course
        
        Returns:
            dict: Résultats de la course
        """
        if not self.is_finished:
            # Si la course n'est pas terminée, la terminer
            while self.current_lap <= self.total_laps:
                self.advance_lap()
        
        # Calculer les écarts de temps finaux
        final_time_gaps = self._calculate_time_gaps()
        
        # Préparer les résultats
        results = {
            'name': self.name,
            'circuit': self.circuit['name'],
            'is_finished': True,
            'positions': self.positions,
            'qualifying': self.qualifying_results,
            'player_position': self.positions.get('player', 0),
            'player_qualifying': self.qualifying_results.get('player', 0),
            'events': self.event_history,
            'weather': self.weather,
            'time_gaps': final_time_gaps,
            'car_status': self.car_status
        }
        
        # Calculer les points pour le joueur
        player_position = results['player_position']
        points_system = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]  # Système de points F1 standard
        
        if player_position <= len(points_system):
            results['points'] = points_system[player_position - 1]
        else:
            results['points'] = 0
        
        # Calculer les gains de compétence
        skill_improvements = {}
        
        # Amélioration de base selon la performance
        if player_position <= 3:  # Podium
            skill_improvements['overall'] = random.uniform(0.5, 1.0)
        elif player_position <= 10:  # Points
            skill_improvements['overall'] = random.uniform(0.3, 0.6)
        else:  # Hors des points
            skill_improvements['overall'] = random.uniform(0.1, 0.3)
        
        # Ajout des améliorations spécifiques basées sur les événements
        for event in self.event_history:
            if event.get('success', False) and 'action' in event:
                action_id = event['action']
                
                if action_id.startswith("overtake"):
                    skill_improvements['overtaking'] = skill_improvements.get('overtaking', 0) + random.uniform(0.1, 0.3)
                elif action_id.startswith("defend"):
                    skill_improvements['defending'] = skill_improvements.get('defending', 0) + random.uniform(0.1, 0.3)
                elif action_id == "push_pace":
                    skill_improvements['pace'] = skill_improvements.get('pace', 0) + random.uniform(0.1, 0.3)
                elif action_id == "conserve_tires":
                    skill_improvements['tire_management'] = skill_improvements.get('tire_management', 0) + random.uniform(0.1, 0.3)
                elif action_id == "wet_overtake":
                    skill_improvements['wet_driving'] = skill_improvements.get('wet_driving', 0) + random.uniform(0.2, 0.5)
        
        results['skill_improvements'] = skill_improvements
        
        # Prime d'argent
        prize_money_base = {
            'f3': 5000,
            'f2': 15000,
            'f1': 100000
        }.get(self.category, 10000)
        
        if player_position <= 3:
            results['prize_money'] = prize_money_base * (4 - player_position)
        elif player_position <= 10:
            results['prize_money'] = prize_money_base / 2
        else:
            results['prize_money'] = prize_money_base / 10
        
        return results
    
    def simulate_race(self):
        """
        Simule la course entière sans interaction du joueur
        
        Returns:
            dict: Résultats de la course
        """
        # Simuler les qualifications si pas encore faites
        if not self.grid:
            self.run_qualifying()
            
        # Initialiser les positions
        self.positions = {driver_id: position + 1 for position, driver_id in enumerate(self.grid)}
        
        # Réinitialiser les temps de course
        self.race_times = {driver_id: 0.0 for driver_id in self.drivers}
        
        # Simuler tous les tours
        for lap in range(1, self.total_laps + 1):
            self.current_lap = lap
            
            # Mettre à jour les temps
            self._update_race_times()
            
            # Simuler les actions des IA
            self._simulate_ai_actions()
            
            # Simuler une action du joueur
            if 'player' in self.drivers:
                available_actions = self.get_available_actions('player')
                if available_actions:
                    action_id = random.choice(available_actions)
                    self.execute_player_action(action_id)
        
        self.is_finished = True
        return self.get_race_results()
                    