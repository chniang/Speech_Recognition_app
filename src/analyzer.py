# coding: utf-8
# ============================================
# MODULE : ANALYSEUR DE DISCOURS NLP
# ============================================
# Auteur : Cheikh Niang
# Description : Analyse complète d'un discours avec techniques NLP

import re
from collections import Counter
from textblob import TextBlob
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Téléchargement des ressources NLTK si nécessaires
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Téléchargement des ressources NLTK en cours...")
    nltk.download('punkt')


class SpeechAnalyzer:
    """
    Classe principale pour l'analyse de discours.
    """
    
    def __init__(self):
        """
        Constructeur de la classe SpeechAnalyzer.
        """
        self.filler_words = [
            'euh', 'donc', 'en fait', 'genre', 'voilà',
            'du coup', 'quoi', 'hein', 'bon', 'bah',
            'enfin', 'en gros', 'disons'
        ]
    
    def analyze(self, text: str) -> dict:
        """
        Analyse complète d'un discours.
        """
        return {
            'stats': self._get_basic_stats(text),
            'sentiment': self._analyze_sentiment(text),
            'fillers': self._detect_fillers(text),
            'clarity': self._analyze_clarity(text),
            'structure': self._analyze_structure(text)
        }
    
    def _get_basic_stats(self, text: str) -> dict:
        """
        Calcule les statistiques de base du texte.
        """
        sentences = sent_tokenize(text, language='french')
        words = word_tokenize(text.lower(), language='french')
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        unique_words = len(set(words))
        vocabulary_richness = (unique_words / len(words) * 100) if words else 0
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_sentence_length': round(avg_sentence_length, 1),
            'unique_words': unique_words,
            'vocabulary_richness': round(vocabulary_richness, 1)
        }
    
    def _analyze_sentiment(self, text: str) -> dict:
        """
        Analyse le sentiment du texte en français.
        """
        mots_positifs = [
            'excellent', 'bon', 'bien', 'super', 'génial', 'parfait',
            'formidable', 'magnifique', 'merveilleux', 'fantastique',
            'réussi', 'positif', 'agréable', 'efficace', 'performant',
            'qualité', 'satisfait', 'heureux', 'content', 'enthousiaste'
        ]
        
        mots_negatifs = [
            'mauvais', 'mal', 'problème', 'échec', 'erreur', 'difficile',
            'négatif', 'désagréable', 'inefficace', 'médiocre',
            'insatisfait', 'malheureux', 'triste', 'inquiet', 'critique'
        ]
        
        words = word_tokenize(text.lower(), language='french')
        score_positif = sum(1 for word in words if word in mots_positifs)
        score_negatif = sum(1 for word in words if word in mots_negatifs)
        
        total_mots_sentiment = score_positif + score_negatif
        if total_mots_sentiment > 0:
            polarity = (score_positif - score_negatif) / total_mots_sentiment
        else:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
        
        if polarity > 0.2:
            sentiment = 'Positif'
        elif polarity < -0.2:
            sentiment = 'Négatif'
        else:
            sentiment = 'Neutre'
        
        subjectivity = total_mots_sentiment / len(words) if words else 0
        
        return {
            'sentiment': sentiment,
            'polarity_score': round(polarity, 2),
            'subjectivity': round(min(1.0, subjectivity * 5), 2)
        }
    
    def _detect_fillers(self, text: str) -> dict:
        """
        Détecte les mots de remplissage dans le discours.
        """
        text_lower = text.lower()
        fillers_found = {}
        total_fillers = 0
        
        for filler in self.filler_words:
            pattern = r'\b' + re.escape(filler) + r'\b'
            count = len(re.findall(pattern, text_lower))
            if count > 0:
                fillers_found[filler] = count
                total_fillers += count
        
        words = word_tokenize(text_lower, language='french')
        filler_rate = (total_fillers / len(words) * 100) if words else 0
        
        return {
            'total_fillers': total_fillers,
            'filler_details': fillers_found,
            'filler_rate_percent': round(filler_rate, 2)
        }
    
    def _analyze_clarity(self, text: str) -> dict:
        """
        Analyse la clarté du discours.
        """
        sentences = sent_tokenize(text, language='french')
        words = word_tokenize(text, language='french')
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        if avg_sentence_length < 15:
            clarity = 'Très clair'
            score = 9
        elif avg_sentence_length < 20:
            clarity = 'Clair'
            score = 7
        elif avg_sentence_length < 25:
            clarity = 'Moyennement clair'
            score = 5
        else:
            clarity = 'Complexe'
            score = 3
        
        return {
            'clarity_level': clarity,
            'clarity_score': score,
            'avg_sentence_length': round(avg_sentence_length, 1)
        }
    
    def _analyze_structure(self, text: str) -> dict:
        """
        Analyse la structure du discours.
        """
        sentences = sent_tokenize(text, language='french')
        
        transition_words = [
            'premièrement', 'deuxièmement', 'troisièmement',
            'ensuite', 'puis', 'après', 'avant',
            'enfin', 'finalement', 'en conclusion',
            'donc', 'ainsi', 'par conséquent',
            'cependant', 'néanmoins', 'toutefois',
            'en effet', 'de plus', 'également',
            'par ailleurs', 'd\'ailleurs'
        ]
        
        transitions_found = 0
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for transition in transition_words:
                if transition in sentence_lower:
                    transitions_found += 1
                    break
        
        structure_score = min(10, (transitions_found / len(sentences) * 20)) if sentences else 0
        
        return {
            'has_structure': transitions_found > 0,
            'transition_count': transitions_found,
            'structure_score': round(structure_score, 1)
        }


if __name__ == "__main__":
    exemple_discours = """
    Bonjour à tous. Aujourd'hui, je vais vous parler de l'intelligence artificielle.
    Premièrement, il faut comprendre que l'IA transforme notre société.
    Ensuite, nous verrons comment l'utiliser dans l'éducation.
    Enfin, je partagerai mes recommandations pour l'avenir.
    """
    
    analyzer = SpeechAnalyzer()
    resultats = analyzer.analyze(exemple_discours)
    
    print("=" * 50)
    print("RÉSULTATS DE L'ANALYSE")
    print("=" * 50)
    print(f"Nombre de mots: {resultats['stats']['word_count']}")
    print(f"Sentiment: {resultats['sentiment']['sentiment']}")
    print(f"Mots parasites: {resultats['fillers']['total_fillers']}")
    print(f"Clarté: {resultats['clarity']['clarity_level']}")
    print(f"Structure: {resultats['structure']['structure_score']}/10")