#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration pour créer un exécutable avec cx_Freeze
"""

import sys
import os
from cx_Freeze import setup, Executable

# Dépendances
build_exe_options = {
    "packages": ["pygame", "random", "os", "sys"],
    "excludes": [],
    "include_files": [
        ("assets", "assets"),  # Inclure les assets dans le build
    ]
}

# Target pour Windows (avec icône et ne pas montrer la console)
base = None
icon = None
if sys.platform == "win32":
    base = "Win32GUI"  # Utiliser cette base pour ne pas afficher la console sous Windows
    icon = "assets/images/icon.ico"  # Chemin de l'icône

# Target pour Mac
if sys.platform == "darwin":
    icon = "assets/images/icon.icns"  # Format d'icône pour macOS

# Configuration de l'exécutable
executables = [
    Executable(
        "main.py",  # Script principal
        base=base,
        target_name="DriveToSurvive",  # Nom du fichier exécutable
        icon=icon,  # Icône
        shortcut_name="Drive to Survive",  # Nom du raccourci
        shortcut_dir="DesktopFolder",  # Créer un raccourci sur le bureau
        copyright="Your Name"  # Copyright
    )
]

# Configuration du setup
setup(
    name="Drive to Survive",
    version="1.0.0",
    description="Jeu de carrière de Formule 1",
    options={"build_exe": build_exe_options},
    executables=executables,
    author="Your Name",
    author_email="your.email@example.com"
)

"""
Pour créer l'exécutable, exécutez:

Windows:
python setup.py build

macOS:
python setup.py bdist_mac

Linux:
python setup.py build
"""