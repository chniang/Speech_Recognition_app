#FONCTIONS UTILITAIRES
#ce module contient des fonctions helpers reutilisables
#dans plusieurs parties du projet

import re 
from typing import List, Dict


def clean_text(text:str) -> str:
    """nettoi un texte en supprimant les caracteres parasites
    cette fonction:
    supprime les espaces multiples
    supprime les retours a la ligne excessifs
    retire les caracteres speciaux unitules
    
    argument:texte (le texte a nettoyer)
    retourne:str (le texte nettoye)
    
    exemple:
    >>>clean_text("bonjour tout le monde \n\n\n!")
    
    "bonjour tout le monde !"
    """
    #remplacer les espaces multiples par un seul espace
    text = re.sub(r'\s+',' ',text)
    #supprimer les espaces en debut et fin
    text = text.strip()
    return text

def format_pourcentage(value:float) -> str:
    """formate un nombre en pourcentage avec deux decimales
    argument:value(valeur a formater)
    retourne:str(pourcentage formate)
    """
    return f"{value*100:.2f}%"

def truncate_text(text:str, max_length:int=100) -> str:
    """
    tronque un texte a une longueur maxiamle
    si le text est plus long que max_length, il est coupe
    et "..." est ajoute a la fin
    
    argument:text(le texte a tronquer)
    max_length(longueur maximale, par defaut 100)
    retourne: str(le texte tronquer si necessaire)
    """
    
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
def calculate_vocabulary_richness(total_words:int,unique_words:int) -> float:
    """
    calcule la richesse du vocabulaire
    
    la richese du vocabulaire est le ratio entre le nombre de mots
    unique et le nombre de mots totales. Plus ce vocabulaire est eleve, 
    plus le vocabulaire est varie
    
    argument:total_words(nombre total de mots)
    unique_words(nombre de mots uniques)
    
    retourne:float(ratio de richesse (entre 0 et 1))
    
    EXEMPLE:
    >>>calculate_vocabulary_richness(100,50)
    0.5
    """
    
    if total_words == 0:
        return 0.0
    return unique_words/total_words
