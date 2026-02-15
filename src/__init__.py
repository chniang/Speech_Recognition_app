# FICHIER DINITIATION DU PACKAGE SRC
#ce fichier transforme le dossier src en module python importable
#il permet decrire from src import SpeechAnalyzer au lieu de 
#from src.analyer import SpeechAnalyzer


"""Package SRC, Module d'analyse NLP pour discours et prise de parole
Ce package contient:
Analyzer: analyse NLP complete d'un discours
feedback_generator: generateur automatise d'un feedback
utils: fonctions utilitaires diverses
"""

__version__ = '1.0.0'
__author__ = 'Cheikh Niang'

#import pour simplifier l'utilisation du package
#cela permet d'importation depuis src

from .analyzer import SpeechAnalyzer
from .feedback_generator import FeedbackGenerator

#liste des objets exportes publiquement
#utiliser pas "from src import *"

__all__ = ['SpeechAnalyzer','FeedbackGenerator']

