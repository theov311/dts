#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fonctions pour sauvegarder et charger les parties
"""

import os
import pickle
import datetime
import glob

# Dossier de sauvegarde
SAVE_DIR = os.path.join(os.path.expanduser('~'), '.drive_to_survive', 'saves')

def ensure_save_dir():
    """Crée le dossier de sauvegarde s'il n'existe pas"""
    os.makedirs(SAVE_DIR, exist_ok=True)

def save_game(save_data, slot=None):
    """
    Sauvegarde une partie
    
    Args:
        save_data (dict): Données à sauvegarder
        slot (int, optional): Emplacement de sauvegarde (1-5). Si None, utilise l'auto-save.
    
    Returns:
        bool: True si la sauvegarde a réussi, False sinon
    """
    ensure_save_dir()
    
    try:
        # Nom du fichier de sauvegarde
        if slot is None:
            filename = "autosave.dat"
        else:
            filename = f"save_{slot}.dat"
        
        save_path = os.path.join(SAVE_DIR, filename)
        
        # Ajouter la date et l'heure de sauvegarde
        save_data['save_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Sauvegarder les données
        with open(save_path, 'wb') as f:
            pickle.dump(save_data, f)
        
        return True
    
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        return False

def load_game(slot=None):
    """
    Charge une partie sauvegardée
    
    Args:
        slot (int, optional): Emplacement de sauvegarde (1-5). Si None, utilise l'auto-save.
    
    Returns:
        dict: Données chargées ou None en cas d'erreur
    """
    ensure_save_dir()
    
    try:
        # Nom du fichier de sauvegarde
        if slot is None:
            filename = "autosave.dat"
        else:
            filename = f"save_{slot}.dat"
        
        save_path = os.path.join(SAVE_DIR, filename)
        
        # Vérifier si le fichier existe
        if not os.path.exists(save_path):
            return None
        
        # Charger les données
        with open(save_path, 'rb') as f:
            save_data = pickle.load(f)
        
        return save_data
    
    except Exception as e:
        print(f"Erreur lors du chargement: {e}")
        return None

def get_save_info(slot=None):
    """
    Récupère les informations d'une sauvegarde
    
    Args:
        slot (int, optional): Emplacement de sauvegarde (1-5). Si None, utilise l'auto-save.
    
    Returns:
        dict: Informations sur la sauvegarde ou None si elle n'existe pas
    """
    ensure_save_dir()
    
    try:
        # Nom du fichier de sauvegarde
        if slot is None:
            filename = "autosave.dat"
        else:
            filename = f"save_{slot}.dat"
        
        save_path = os.path.join(SAVE_DIR, filename)
        
        # Vérifier si le fichier existe
        if not os.path.exists(save_path):
            return None
        
        # Charger les données juste pour récupérer les infos
        with open(save_path, 'rb') as f:
            save_data = pickle.load(f)
        
        # Récupérer les informations essentielles
        player = save_data.get('player', {})
        career = save_data.get('career', {})
        
        return {
            'save_date': save_data.get('save_date', 'Date inconnue'),
            'player_name': player.name if player else 'Inconnu',
            'player_age': player.age if player else 0,
            'player_category': player.category if player else 'Inconnue',
            'player_team': player.team.name if player and player.team else 'Inconnue',
            'current_year': career.current_year if career else 0
        }
    
    except Exception as e:
        print(f"Erreur lors de la récupération des infos: {e}")
        return None

def list_saves():
    """
    Liste toutes les sauvegardes disponibles
    
    Returns:
        list: Liste des emplacements de sauvegarde avec leurs informations
    """
    ensure_save_dir()
    
    saves = []
    
    # Autosave
    autosave_info = get_save_info(None)
    if autosave_info:
        saves.append({
            'slot': 'auto',
            'info': autosave_info
        })
    
    # Sauvegardes manuelles
    for slot in range(1, 6):
        save_info = get_save_info(slot)
        if save_info:
            saves.append({
                'slot': slot,
                'info': save_info
            })
    
    return saves

def delete_save(slot=None):
    """
    Supprime une sauvegarde
    
    Args:
        slot (int, optional): Emplacement de sauvegarde (1-5). Si None, supprime l'auto-save.
    
    Returns:
        bool: True si la suppression a réussi, False sinon
    """
    ensure_save_dir()
    
    try:
        # Nom du fichier de sauvegarde
        if slot is None:
            filename = "autosave.dat"
        else:
            filename = f"save_{slot}.dat"
        
        save_path = os.path.join(SAVE_DIR, filename)
        
        # Vérifier si le fichier existe
        if not os.path.exists(save_path):
            return False
        
        # Supprimer le fichier
        os.remove(save_path)
        return True
    
    except Exception as e:
        print(f"Erreur lors de la suppression: {e}")
        return False