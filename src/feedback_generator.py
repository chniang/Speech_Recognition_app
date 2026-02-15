# MODULE : GÉNÉRATEUR DE FEEDBACK AUTOMATISÉ
# Ce module transforme les résultats d'analyse NLP
# en feedback structuré et actionnable pour l'utilisateur.
# Le feedback comprend :
#   - Score global sur 10
#   - Points forts identifiés
#   - Points à améliorer
#   - Recommandations concrètes

class FeedbackGenerator:
    """
    Classe qui génère un feedback structuré à partir des résultats d'analyse.
    
    Le feedback est orienté "coaching" : il est constructif, spécifique,
    et donne des actions concrètes pour s'améliorer.
    """
    
    def generate(self, analysis_results: dict) -> dict:
        """
        Génère un feedback complet à partir des résultats d'analyse.
        
        Arguments:
            analysis_results : Dictionnaire retourné par SpeechAnalyzer.analyze()
            
        Retourne:
            dict : Feedback structuré contenant :
                - score_global : Note sur 10
                - points_forts : Liste des aspects positifs
                - points_amelioration : Liste des aspects à améliorer
                - recommandations : Conseils concrets et actionnables
        """
        # Initialiser la structure du feedback
        feedback = {
            'score_global': self._calculate_global_score(analysis_results),
            'points_forts': [],
            'points_amelioration': [],
            'recommandations': []
        }
        
        # Analyser chaque aspect du discours
        # Chaque méthode remplit les listes du feedback
        self._feedback_stats(analysis_results['stats'], feedback)
        self._feedback_sentiment(analysis_results['sentiment'], feedback)
        self._feedback_fillers(analysis_results['fillers'], feedback)
        self._feedback_clarity(analysis_results['clarity'], feedback)
        self._feedback_structure(analysis_results['structure'], feedback)
        
        return feedback
    
    def _calculate_global_score(self, results: dict) -> float:
        """
        Calcule le score global sur 10 basé sur tous les critères.
        
        La formule pondère différents aspects :
        - Clarté : 40% (le plus important)
        - Structure : 40% (très important aussi)
        - Absence de mots parasites : 20%
        
        Arguments:
            results : Résultats complets de l'analyse
            
        Retourne:
            float : Score sur 10
        """
        # Récupérer les scores individuels
        clarity_score = results['clarity']['clarity_score']
        structure_score = results['structure']['structure_score']
        
        # Calculer la pénalité pour les mots parasites
        # Plus il y a de mots parasites, plus la pénalité est forte
        # On limite la pénalité à 3 points maximum
        filler_penalty = min(3, results['fillers']['filler_rate_percent'] / 2)
        
        # Calculer le score global avec pondération
        # 40% clarté + 40% structure + 20% absence de parasites
        score = (
            clarity_score * 0.4 + 
            structure_score * 0.4 + 
            (10 - filler_penalty) * 0.2
        )
        
        # S'assurer que le score reste entre 0 et 10
        # min() garantit qu'on ne dépasse pas 10
        # max() garantit qu'on ne descend pas sous 0
        return round(min(10, max(0, score)), 1)
    
    def _feedback_stats(self, stats: dict, feedback: dict):
        """
        Génère le feedback sur les statistiques de base.
        
        Évalue principalement la longueur du discours.
        """
        word_count = stats['word_count']
        
        # Évaluer la longueur
        # Pour un discours standard, 100-500 mots est une bonne longueur
        if 100 <= word_count <= 500:
            feedback['points_forts'].append(
                f"Longueur appropriée ({word_count} mots)"
            )
        elif word_count < 100:
            feedback['points_amelioration'].append(
                f"Discours un peu court ({word_count} mots)"
            )
            feedback['recommandations'].append(
                "Développez davantage vos arguments avec des exemples concrets"
            )
        else:
            feedback['points_amelioration'].append(
                f"Discours un peu long ({word_count} mots)"
            )
            feedback['recommandations'].append(
                "Concentrez-vous sur l'essentiel, soyez plus concis"
            )
    
    def _feedback_sentiment(self, sentiment: dict, feedback: dict):
        """
        Génère le feedback sur le sentiment du discours.
        """
        # Un ton positif est généralement apprécié
        if sentiment['sentiment'] == 'Positif':
            feedback['points_forts'].append(
                "Ton positif et engageant"
            )
        elif sentiment['sentiment'] == 'Négatif':
            feedback['points_amelioration'].append(
                "Ton un peu négatif"
            )
            feedback['recommandations'].append(
                "Essayez d'adopter un ton plus positif et constructif"
            )
    
    def _feedback_fillers(self, fillers: dict, feedback: dict):
        """
        Génère le feedback sur les mots de remplissage.
        
        Les mots parasites sont un indicateur important de la qualité
        de la préparation et de la maîtrise du sujet.
        """
        filler_rate = fillers['filler_rate_percent']
        
        # Seuils d'évaluation
        if filler_rate < 2:
            feedback['points_forts'].append(
                "Très peu de mots de remplissage"
            )
        elif filler_rate > 5:
            feedback['points_amelioration'].append(
                f"Trop de mots de remplissage ({filler_rate}%)"
            )
            
            # Identifier les mots les plus fréquents
            if fillers['filler_details']:
                most_common = max(fillers['filler_details'], 
                                key=fillers['filler_details'].get)
                feedback['recommandations'].append(
                    f"Vous utilisez beaucoup '{most_common}'. "
                    "Faites des pauses silencieuses à la place."
                )
    
    def _feedback_clarity(self, clarity: dict, feedback: dict):
        """
        Génère le feedback sur la clarté du discours.
        """
        if clarity['clarity_score'] >= 7:
            feedback['points_forts'].append(
                f"Message clair ({clarity['clarity_level']})"
            )
        else:
            feedback['points_amelioration'].append(
                f"Clarté à améliorer ({clarity['clarity_level']})"
            )
            feedback['recommandations'].append(
                "Utilisez des phrases plus courtes et simples (15-20 mots maximum)"
            )
    
    def _feedback_structure(self, structure: dict, feedback: dict):
        """
        Génère le feedback sur la structure du discours.
        """
        if structure['has_structure']:
            feedback['points_forts'].append(
                f"Bonne structure avec {structure['transition_count']} transitions"
            )
        else:
            feedback['points_amelioration'].append(
                "Structure peu visible"
            )
            feedback['recommandations'].append(
                "Ajoutez des mots de transition : 'Premièrement...', "
                "'Ensuite...', 'Enfin...'"
            )