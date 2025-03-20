#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestion des événements pendant une course
"""

class RaceEvent:
    """Classe représentant un événement pendant une course"""
    
    def __init__(self, event_id, name, description, success_chance=50):
        """
        Initialisation d'un événement
        
        Args:
            event_id (str): Identifiant unique de l'événement
            name (str): Nom de l'événement
            description (str): Description de l'événement
            success_chance (int): Chance de réussite de base (0-100)
        """
        self.id = event_id
        self.name = name
        self.description = description
        self.success_chance = success_chance
    
    def get_success_chance(self, player_skill):
        """
        Calcule la chance de réussite en fonction du niveau du joueur
        
        Args:
            player_skill (float): Niveau de compétence du joueur
            
        Returns:
            float: Chance de réussite ajustée
        """
        # Ajuster la chance de réussite en fonction du niveau
        adjusted_chance = self.success_chance + (player_skill - 50) / 5
        
        # Limiter entre 10% et 95%
        return max(10, min(95, adjusted_chance))


class RaceActionResult:
    """Résultat d'une action pendant une course"""
    
    def __init__(self, event, success, position_change=0, message="", car_damage=0, tire_wear=0):
        """
        Initialisation d'un résultat d'action
        
        Args:
            event (RaceEvent): Événement concerné
            success (bool): Si l'action a réussi
            position_change (int): Changement de position (-1 = gain, +1 = perte)
            message (str): Message de résultat
            car_damage (int): Dégâts sur la voiture (0-100)
            tire_wear (int): Usure supplémentaire des pneus (0-100)
        """
        self.event = event
        self.success = success
        self.position_change = position_change
        self.message = message
        self.car_damage = car_damage
        self.tire_wear = tire_wear


# Événements de dépassement
OVERTAKE_NORMAL = RaceEvent(
    "overtake_normal",
    "Dépassement standard",
    "Tentative de dépassement standard avec un risque modéré",
    70
)

OVERTAKE_RISKY = RaceEvent(
    "overtake_risky",
    "Dépassement risqué",
    "Tentative de dépassement audacieuse avec un risque élevé",
    50
)

OVERTAKE_DRS = RaceEvent(
    "overtake_drs",
    "Dépassement avec DRS",
    "Utilisation du DRS pour faciliter un dépassement (F1 uniquement)",
    80
)

# Événements de défense
DEFEND_NORMAL = RaceEvent(
    "defend_normal",
    "Défense de position",
    "Défense standard de votre position",
    75
)

DEFEND_AGGRESSIVE = RaceEvent(
    "defend_aggressive",
    "Défense agressive",
    "Défense agressive de votre position, avec risque de pénalité",
    60
)

# Événements de conduite
PUSH_PACE = RaceEvent(
    "push_pace",
    "Pousser le rythme",
    "Augmenter votre rythme pour gagner du temps, au risque d'user les pneus",
    80
)

CONSERVE_TIRES = RaceEvent(
    "conserve_tires",
    "Préserver les pneus",
    "Conduire plus doucement pour préserver vos pneus",
    90
)

FUEL_SAVING = RaceEvent(
    "fuel_saving",
    "Économie de carburant",
    "Réduire la consommation de carburant",
    85
)

# Événements liés aux conditions
WET_DRIVING = RaceEvent(
    "wet_overtake",
    "Dépassement sous la pluie",
    "Tentative de dépassement sur piste mouillée",
    50
)

RISKY_CORNER = RaceEvent(
    "risky_corner",
    "Virage risqué",
    "Prise de risque dans un virage difficile",
    60
)

# Liste des événements standards
STANDARD_EVENTS = [
    OVERTAKE_NORMAL,
    OVERTAKE_RISKY,
    DEFEND_NORMAL,
    DEFEND_AGGRESSIVE,
    PUSH_PACE,
    CONSERVE_TIRES,
    FUEL_SAVING
]

# Fonction pour obtenir les événements disponibles
def get_available_events(category, weather, circuit_difficulty):
    """
    Récupère les événements disponibles selon le contexte
    
    Args:
        category (str): Catégorie ('f3', 'f2', 'f1')
        weather (dict): Conditions météo
        circuit_difficulty (int): Difficulté du circuit (1-10)
        
    Returns:
        list: Liste des événements disponibles
    """
    events = STANDARD_EVENTS.copy()
    
    # Événements spécifiques à la F1
    if category == 'f1':
        events.append(OVERTAKE_DRS)
    
    # Événements liés à la pluie
    if weather.get('rain', 0) > 0:
        events.append(WET_DRIVING)
    
    # Événements liés à la difficulté du circuit
    if circuit_difficulty >= 7:
        events.append(RISKY_CORNER)
    
    return events