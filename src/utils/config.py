#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestion de la configuration du jeu
"""

import os
import json

# Configuration par défaut
DEFAULT_CONFIG = {
    'screen_width': 1024,
    'screen_height': 768,
    'fullscreen': False,
    'fps': 60,
    'sound_enabled': True,
    'sound_volume': 0.7,
    'music_enabled': True,
    'music_volume': 0.5,
    'difficulty': 'normal',  # 'easy', 'normal', 'hard'
    'language': 'fr',
    'first_run': True
}

# Chemin du fichier de configuration
CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.drive_to_survive', 'config.json')

def load_config():
    """
    Charge la configuration du jeu
    
    Returns:
        dict: Configuration du jeu
    """
    # Vérifier si le fichier de configuration existe
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # Fusionner avec la configuration par défaut pour les nouveaux paramètres
            merged_config = DEFAULT_CONFIG.copy()
            merged_config.update(config)
            return merged_config
        
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            # En cas d'erreur, utiliser la configuration par défaut
            return DEFAULT_CONFIG
    else:
        # Créer le fichier de configuration avec les valeurs par défaut
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    """
    Sauvegarde la configuration du jeu
    
    Args:
        config (dict): Configuration à sauvegarder
    
    Returns:
        bool: True si la sauvegarde a réussi, False sinon
    """
    try:
        # Créer le dossier si nécessaire
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        
        # Sauvegarder la configuration
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        
        return True
    
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la configuration: {e}")
        return False

def update_config(key, value):
    """
    Met à jour une valeur dans la configuration
    
    Args:
        key (str): Clé à mettre à jour
        value: Nouvelle valeur
    
    Returns:
        bool: True si la mise à jour a réussi, False sinon
    """
    config = load_config()
    config[key] = value
    return save_config(config)

def reset_config():
    """
    Réinitialise la configuration aux valeurs par défaut
    
    Returns:
        bool: True si la réinitialisation a réussi, False sinon
    """
    return save_config(DEFAULT_CONFIG)