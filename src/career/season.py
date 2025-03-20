#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestion des saisons de course et des championnats
"""

import random
from src.racing.race import Race

class Season:
    """Classe représentant une saison de course"""
    
    def __init__(self, year, category, races_count, points_system, player, teams):
        """
        Initialisation d'une saison
        
        Args:
            year (int): Année de la saison
            category (str): Catégorie ('f3', 'f2', 'f1')
            races_count (int): Nombre de courses dans la saison
            points_system (list): Système de points pour les positions
            player (Player): Joueur/pilote
            teams (list): Liste des équipes participantes
        """
        self.year = year
        self.category = category
        self.races_count = races_count
        self.points_system = points_system
        self.player = player
        self.teams = teams
        
        # Génération des circuits pour la saison
        self.circuits = self._generate_circuits()
        
        # Liste des pilotes (joueur + IA)
        self.drivers = self._generate_drivers()
        
        # Classements
        self.driver_standings = {driver_id: 0 for driver_id in self.drivers}
        self.team_standings = {team.name: 0 for team in teams}
        
        # Programme des courses
        self.race_calendar = self._generate_race_calendar()
        
        # Index de la course actuelle
        self.current_race_index = 0
        
        # Historique des résultats
        self.race_results = []
    
    def _generate_circuits(self):
        """
        Génère la liste des circuits pour la saison
        
        Returns:
            list: Liste des circuits
        """
        # Liste des circuits possibles selon la catégorie
        f1_circuits = [
            {"name": "Circuit de Monaco", "country": "Monaco", "difficulty": 9},
            {"name": "Silverstone", "country": "Royaume-Uni", "difficulty": 7},
            {"name": "Spa-Francorchamps", "country": "Belgique", "difficulty": 8},
            {"name": "Monza", "country": "Italie", "difficulty": 6},
            {"name": "Suzuka", "country": "Japon", "difficulty": 8},
            {"name": "Circuit des Amériques", "country": "États-Unis", "difficulty": 7},
            {"name": "Circuit de Barcelone-Catalogne", "country": "Espagne", "difficulty": 6},
            {"name": "Red Bull Ring", "country": "Autriche", "difficulty": 5},
            {"name": "Hungaroring", "country": "Hongrie", "difficulty": 7},
            {"name": "Circuit Gilles-Villeneuve", "country": "Canada", "difficulty": 6},
            {"name": "Yas Marina", "country": "Émirats arabes unis", "difficulty": 5},
            {"name": "Bahrain International Circuit", "country": "Bahreïn", "difficulty": 5},
            {"name": "Circuit de Djeddah", "country": "Arabie Saoudite", "difficulty": 8},
            {"name": "Circuit International de Shanghai", "country": "Chine", "difficulty": 6},
            {"name": "Autodromo Jose Carlos Pace", "country": "Brésil", "difficulty": 7},
            {"name": "Circuit de Zandvoort", "country": "Pays-Bas", "difficulty": 7},
            {"name": "Albert Park", "country": "Australie", "difficulty": 6},
            {"name": "Circuit Paul Ricard", "country": "France", "difficulty": 5},
            {"name": "Baku City Circuit", "country": "Azerbaïdjan", "difficulty": 8},
            {"name": "Losail International Circuit", "country": "Qatar", "difficulty": 6},
            {"name": "Autodromo Enzo e Dino Ferrari", "country": "Italie", "difficulty": 7},
            {"name": "Circuit de Mexico", "country": "Mexique", "difficulty": 6},
            {"name": "Marina Bay Street Circuit", "country": "Singapour", "difficulty": 9}
        ]
        
        f2_f3_circuits = [circuit for circuit in f1_circuits if circuit["difficulty"] <= 8]
        
        # Sélection des circuits selon la catégorie
        if self.category == 'f1':
            # Pour la F1, on utilise 23 circuits (tous différents)
            selected_circuits = random.sample(f1_circuits, min(self.races_count, len(f1_circuits)))
        elif self.category == 'f2':
            # Pour la F2, on utilise 12 circuits
            selected_circuits = random.sample(f2_f3_circuits, min(self.races_count, len(f2_f3_circuits)))
        else:  # f3
            # Pour la F3, on utilise 7 circuits
            selected_circuits = random.sample(f2_f3_circuits, min(self.races_count, len(f2_f3_circuits)))
        
        return selected_circuits
    
    def _generate_drivers(self):
        """
        Génère la liste des pilotes pour la saison
        
        Returns:
            dict: Dictionnaire des pilotes (id: info)
        """
        # Nombre de pilotes selon la catégorie
        drivers_count = {
            'f1': 20,
            'f2': 22,
            'f3': 30
        }
        
        # Le joueur est toujours inclus
        drivers = {
            "player": {
                "name": self.player.name,
                "team": self.player.team.name,
                "skills": self.player.skills.overall,
                "is_player": True
            }
        }
        
        # Génération des pilotes IA
        first_names = ["Alex", "Daniel", "Carlos", "Lewis", "Max", "Charles", "Lando", "Pierre", "Esteban", 
                      "Lance", "Fernando", "Sebastian", "Mick", "Valtteri", "George", "Sergio", "Yuki", 
                      "Nicholas", "Zhou", "Kevin", "Jean", "Oscar", "Théo", "Jack", "Frederik", "Oliver"]
        
        last_names = ["Smith", "Johnson", "Brown", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", 
                      "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Martin", "Lee", "Thompson", 
                      "White", "Lopez", "Hill", "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen", 
                      "King", "Wright", "Scott", "Torres", "Nguyen", "Pourchaire", "Doohan", "Lawson"]
        
        # Attribuer les pilotes IA aux équipes
        team_names = [team.name for team in self.teams]
        drivers_per_team = {}
        
        for team_name in team_names:
            drivers_per_team[team_name] = 0
        
        # Nombre total de pilotes à générer
        ai_drivers_count = drivers_count[self.category] - 1  # -1 pour le joueur
        
        for i in range(ai_drivers_count):
            # Choisir un nom
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            name = f"{first_name} {last_name}"
            
            # Choisir une équipe qui n'a pas encore tous ses pilotes
            available_teams = [team for team in team_names 
                              if drivers_per_team[team] < 2 and team != self.player.team.name]
            
            # Si le joueur est le seul pilote de son équipe, aussi considérer son équipe
            if drivers_per_team[self.player.team.name] < 1:
                available_teams.append(self.player.team.name)
            
            if not available_teams:  # Toutes les équipes sont pleines
                break
            
            team_name = random.choice(available_teams)
            drivers_per_team[team_name] += 1
            
            # Générer un niveau de compétence
            # Plus d'équipes prestigieuses ont des pilotes plus forts
            team = next((t for t in self.teams if t.name == team_name), None)
            base_skill = 50
            if team:
                base_skill = team.performance
            
            # Ajouter un peu de variation
            skill = max(1, min(100, base_skill + random.randint(-15, 15)))
            
            # Ajouter le pilote
            driver_id = f"driver_{i+1}"
            drivers[driver_id] = {
                "name": name,
                "team": team_name,
                "skills": skill,
                "is_player": False
            }
        
        return drivers
    
    def _generate_race_calendar(self):
        """
        Génère le calendrier des courses pour la saison
        
        Returns:
            list: Calendrier des courses
        """
        calendar = []
        
        for i in range(self.races_count):
            circuit = self.circuits[i % len(self.circuits)]
            
            # Générer une date fictive
            month = 3 + (i * 9 // self.races_count)  # Répartir les courses de mars à novembre
            day = random.randint(1, 28)
            
            race = {
                "id": i + 1,
                "name": f"Grand Prix de {circuit['country']}",
                "circuit": circuit,
                "date": f"{day:02d}/{month:02d}/{self.year}",
                "completed": False,
                "race_obj": None
            }
            
            calendar.append(race)
        
        return calendar
    
    def get_next_race(self):
        """
        Récupère la prochaine course à disputer
        
        Returns:
            dict: Informations sur la prochaine course
        """
        if self.current_race_index < len(self.race_calendar):
            race_info = self.race_calendar[self.current_race_index]
            
            # Création de l'objet Race
            race_obj = Race(
                name=race_info["name"],
                circuit=race_info["circuit"],
                category=self.category,
                drivers=self.drivers,
                player=self.player
            )
            
            # Stocker l'objet Race dans le calendrier
            race_info["race_obj"] = race_obj
            
            return race_info
        else:
            return None  # Plus de courses dans la saison
    
    def complete_race(self, race_results):
        """
        Marque une course comme terminée et met à jour les classements
        
        Args:
            race_results (dict): Résultats de la course
        """
        race_info = self.race_calendar[self.current_race_index]
        race_info["completed"] = True
        
        # Mise à jour des points au championnat
        driver_positions = race_results.get("driver_positions", {})
        for driver_id, position in driver_positions.items():
            # Attribution des points
            points = 0
            if position <= len(self.points_system):
                points = self.points_system[position - 1]
            
            # Mise à jour du classement pilote
            self.driver_standings[driver_id] += points
            
            # Mise à jour du classement équipe
            team_name = self.drivers[driver_id]["team"]
            self.team_standings[team_name] += points
        
        # Enregistrement des résultats
        self.race_results.append(race_results)
        
        # Passage à la course suivante
        self.current_race_index += 1
    
    def get_current_standings(self):
        """
        Récupère les classements actuels
        
        Returns:
            dict: Classements pilotes et équipes
        """
        # Tri des classements
        sorted_drivers = sorted(self.driver_standings.items(), 
                               key=lambda x: x[1], reverse=True)
        sorted_teams = sorted(self.team_standings.items(), 
                             key=lambda x: x[1], reverse=True)
        
        # Trouver la position du joueur
        player_position = 1
        for i, (driver_id, _) in enumerate(sorted_drivers):
            if driver_id == "player":
                player_position = i + 1
                break
        
        # Trouver la position de l'équipe du joueur
        team_position = 1
        player_team = self.player.team.name
        for i, (team_name, _) in enumerate(sorted_teams):
            if team_name == player_team:
                team_position = i + 1
                break
        
        return {
            "driver_standings": sorted_drivers,
            "team_standings": sorted_teams,
            "player_position": player_position,
            "player_points": self.driver_standings["player"],
            "team_position": team_position,
            "team_points": self.team_standings[player_team],
            "races_completed": self.current_race_index,
            "total_races": self.races_count
        }
    
    def get_final_standings(self):
        """
        Récupère les classements finaux de la saison
        
        Returns:
            dict: Classements finaux
        """
        # Si toutes les courses ne sont pas terminées, compléter la saison avec des simulations
        while self.current_race_index < len(self.race_calendar):
            race_info = self.get_next_race()
            race_obj = race_info["race_obj"]
            
            # Simulation de la course (résultats aléatoires mais influencés par les niveaux)
            sim_results = race_obj.simulate_race()
            self.complete_race(sim_results)
        
        # Récupérer les classements finaux
        final_standings = self.get_current_standings()
        
        # Déterminer le champion
        champion_id = final_standings["driver_standings"][0][0]
        champion_name = self.drivers[champion_id]["name"]
        
        # Déterminer l'équipe championne
        team_champion = final_standings["team_standings"][0][0]
        
        final_standings["champion"] = champion_name
        final_standings["team_champion"] = team_champion
        
        return final_standings