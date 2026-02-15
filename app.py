# coding: utf-8
# ============================================
# APPLICATION STREAMLIT : ANALYSE DE DISCOURS
# ============================================

import streamlit as st
from src.analyzer import SpeechAnalyzer
from src.feedback_generator import FeedbackGenerator
from nltk.tokenize import word_tokenize
import nltk

# Télécharger les ressources NLTK nécessaires
@st.cache_resource
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)

# Exécuter le téléchargement au démarrage
download_nltk_data()

# Configuration de la page
st.set_page_config(
    page_title="Analyse de Discours IA",
    page_icon="ðŸŽ¤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# En-tÃªte
st.title("ðŸŽ¤ Analyse de Discours IA")
st.markdown("**Analysez votre discours et obtenez un feedback automatisÃ© basÃ© sur l'IA**")
st.info("ðŸ’¡ Cette application utilise le NLP pour analyser la qualitÃ© de votre prise de parole.")

# Sidebar
with st.sidebar:
    st.header("Ã€ propos")
    st.markdown("""
    ### Ce systÃ¨me analyse :
    
    - âœ… **Sentiment** du discours
    - âœ… **ClartÃ©** du message
    - âœ… **Structure** et transitions
    - âœ… **Mots de remplissage**
    
    ---
    
    **DÃ©veloppÃ© par :** Cheikh Niang  
    **Projet :** NLP Speech Analysis
    """)
    
    st.subheader("Exemple de texte")
    st.code("""
Bonjour Ã  tous. Aujourd'hui, je vais vous 
parler de l'intelligence artificielle. 
PremiÃ¨rement, l'IA transforme notre sociÃ©tÃ©. 
Ensuite, nous verrons ses applications. 
Enfin, je partagerai mes recommandations.
    """, language="text")

# Zone de saisie
st.subheader("ðŸ“ Votre discours")

text_input = st.text_area(
    label="Entrez ou collez votre discours ici",
    height=200,
    placeholder="Exemple : Bonjour Ã  tous. Aujourd'hui, je vais vous parler de...",
    help="Tapez ou collez le texte de votre discours pour l'analyser",
    label_visibility="collapsed"
)

# Compteur de mots
if text_input:
    word_count = len(word_tokenize(text_input, language='french'))
    st.caption(f"ðŸ“Š {word_count} mots")

# Bouton d'analyse
analyze_button = st.button("ðŸ” Analyser mon discours", type="primary", use_container_width=True)

# Traitement
if analyze_button:
    if not text_input.strip():
        st.error("âš ï¸ Veuillez entrer un texte Ã  analyser")
    elif len(text_input.split()) < 10:
        st.warning("âš ï¸ Le texte est trop court (minimum 10 mots)")
    else:
        with st.spinner("Analyse en cours..."):
            analyzer = SpeechAnalyzer()
            feedback_gen = FeedbackGenerator()
            results = analyzer.analyze(text_input)
            feedback = feedback_gen.generate(results)
        
        st.success("âœ… Analyse terminÃ©e !")
        st.divider()
        
        # Score global
        st.subheader("ðŸ“Š Score Global")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            score = feedback['score_global']
            if score >= 7:
                delta_text = "Excellent"
            elif score >= 5:
                delta_text = "Bien"
            else:
                delta_text = "Ã€ amÃ©liorer"
            
            st.metric(label="Score", value=f"{score}/10", delta=delta_text)
        
        st.divider()
        
        # Feedback structurÃ©
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader("âœ… Points Forts")
            if feedback['points_forts']:
                for point in feedback['points_forts']:
                    st.success(point)
            else:
                st.info("Aucun point fort identifiÃ© pour le moment")
        
        with col_right:
            st.subheader("âš ï¸ Points Ã  AmÃ©liorer")
            if feedback['points_amelioration']:
                for point in feedback['points_amelioration']:
                    st.warning(point)
            else:
                st.success("Rien Ã  amÃ©liorer, excellent travail !")
        
        # Recommandations
        if feedback['recommandations']:
            st.divider()
            st.subheader("ðŸ’¡ Recommandations")
            for i, reco in enumerate(feedback['recommandations'], 1):
                st.info(f"**{i}.** {reco}")
        
        # DÃ©tails techniques
        st.divider()
        with st.expander("ðŸ“ˆ DÃ©tails de l'analyse (avancÃ©)"):
            st.markdown("### Statistiques")
            st.json(results['stats'])
            st.markdown("### Sentiment")
            st.json(results['sentiment'])
            st.markdown("### Mots de remplissage")
            st.json(results['fillers'])
            st.markdown("### ClartÃ©")
            st.json(results['clarity'])
            st.markdown("### Structure")
            st.json(results['structure'])

# Pied de page
st.divider()
st.caption("ðŸ“Œ DÃ©veloppÃ© par **Cheikh Niang** | Projet NLP Speech Analysis | PropulsÃ© par Python & Streamlit")