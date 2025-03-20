#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Constantes utilisées dans le jeu
"""

# Catégories
CATEGORIES = {
    'f3': 'Formule 3',
    'f2': 'Formule 2',
    'f1': 'Formule 1'
}

# Nombre de courses par catégorie
RACES_COUNT = {
    'f3': 7,
    'f2': 12,
    'f1': 23
}

# Systèmes de points par catégorie
POINTS_SYSTEMS = {
    'f3': [25, 18, 15, 12, 10, 8, 6, 4, 2, 1],
    'f2': [25, 18, 15, 12, 10, 8, 6, 4, 2, 1],
    'f1': [25, 18, 15, 12, 10, 8, 6, 4, 2, 1, 0, 0, 0, 0, 0]
}

# Salaires de base par catégorie
BASE_SALARIES = {
    'f3': 50000,      # 50K€
    'f2': 200000,     # 200K€
    'f1': 1000000     # 1M€
}

# Budget des équipes par catégorie
TEAM_BUDGETS = {
    'f3': 1000000,    # 1M€
    'f2': 5000000,    # 5M€
    'f1': 150000000   # 150M€
}

# Prime de course par catégorie (position 1)
RACE_PRIZE_MONEY = {
    'f3': 5000,       # 5K€
    'f2': 15000,      # 15K€
    'f1': 100000      # 100K€
}

# Couleurs des équipes
TEAM_COLORS = {
    # Équipes F1
    "Scuderia Ferrari": ((180, 0, 0), (220, 30, 30)),
    "Mercedes-AMG Petronas": ((0, 180, 180), (30, 220, 220)),
    "Red Bull Racing": ((0, 0, 180), (30, 30, 220)),
    "BWT Alpine F1 Team": ((0, 0, 100), (30, 30, 150)),
    "McLaren F1 Team": ((255, 135, 0), (255, 165, 30)),
    
    # Équipes F2
    "Prema Racing": ((180, 0, 0), (220, 30, 30)),
    "ART Grand Prix": ((0, 180, 180), (30, 220, 220)),
    "Carlin": ((0, 0, 180), (30, 30, 220)),
    "Virtuosi Racing": ((0, 150, 0), (30, 180, 30)),
    "DAMS": ((255, 135, 0), (255, 165, 30)),
    
    # Équipes F3
    "Hitech Grand Prix": ((180, 0, 0), (220, 30, 30)),
    "MP Motorsport": ((0, 100, 150), (30, 130, 180)),
    "Campos Racing": ((0, 150, 0), (30, 180, 30))
}

# Niveaux de difficulté
DIFFICULTY_LEVELS = {
    'easy': {
        'ai_skill_factor': 0.8,     # Les IA sont 20% moins compétentes
        'skill_gain_factor': 1.5,   # Gains de compétences 50% plus rapides
        'prize_money_factor': 1.2   # 20% de gains supplémentaires
    },
    'normal': {
        'ai_skill_factor': 1.0,
        'skill_gain_factor': 1.0,
        'prize_money_factor': 1.0
    },
    'hard': {
        'ai_skill_factor': 1.2,     # Les IA sont 20% plus compétentes
        'skill_gain_factor': 0.8,   # Gains de compétences 20% plus lents
        'prize_money_factor': 0.9   # 10% de gains en moins
    }
}

# Compétences des pilotes
DRIVER_SKILLS = [
    'pace',              # Vitesse pure
    'overtaking',        # Capacité de dépassement
    'defending',         # Défense de position
    'consistency',       # Régularité
    'tire_management',   # Gestion des pneus
    'wet_driving',       # Pilotage sous la pluie
    'technical_feedback', # Feedback technique pour les réglages
    'starts'             # Départs
]

# Types d'événements de course
RACE_EVENT_TYPES = [
    'overtake_normal',   # Dépassement standard
    'overtake_risky',    # Dépassement risqué
    'defend_normal',     # Défense standard
    'defend_aggressive', # Défense agressive
    'push_pace',         # Pousser le rythme
    'conserve_tires',    # Préserver les pneus
    'fuel_saving',       # Économie de carburant
    'wet_overtake',      # Dépassement sous la pluie
    'risky_corner',      # Virage risqué
    'aggressive_curbs'   # Utilisation agressive des vibreurs
]

# Conditions météo
WEATHER_CONDITIONS = [
    'Sec',              # Temps sec
    'Pluie légère',     # Pluie légère
    'Pluie forte'       # Pluie forte
]

# Composés de pneus
TIRE_COMPOUNDS = [
    'soft',             # Pneus tendres
    'medium',           # Pneus médiums
    'hard',             # Pneus durs
    'wet'               # Pneus pluie
]

# Couleurs de l'interface
UI_COLORS = {
    'background': (30, 30, 50),
    'text': (255, 255, 255),
    'highlight': (255, 220, 50),
    'button': (50, 100, 180),
    'button_hover': (70, 130, 210),
    'warning': (220, 50, 50),
    'success': (50, 180, 50),
    'info': (50, 150, 220)
}