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
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# En-tête
st.title("🎤 Analyse de Discours IA")
st.markdown("**Analysez votre discours et obtenez un feedback automatisé basé sur l'IA**")
st.info("💡 Cette application utilise le NLP pour analyser la qualité de votre prise de parole.")

# Sidebar
with st.sidebar:
    st.header("À propos")
    st.markdown("""
    ### Ce système analyse :
    
    - ✅ **Sentiment** du discours
    - ✅ **Clarté** du message
    - ✅ **Structure** et transitions
    - ✅ **Mots de remplissage**
    
    ---
    
    **Développé par :** Cheikh Niang  
    **Projet :** NLP Speech Analysis
    """)
    
    st.subheader("Exemple de texte")
    st.code("""
Bonjour à tous. Aujourd'hui, je vais vous 
parler de l'intelligence artificielle. 
Premièrement, l'IA transforme notre société. 
Ensuite, nous verrons ses applications. 
Enfin, je partagerai mes recommandations.
    """, language="text")

# Zone de saisie
st.subheader("📝 Votre discours")

text_input = st.text_area(
    label="Entrez ou collez votre discours ici",
    height=200,
    placeholder="Exemple : Bonjour à tous. Aujourd'hui, je vais vous parler de...",
    help="Tapez ou collez le texte de votre discours pour l'analyser",
    label_visibility="collapsed"
)

# Compteur de mots
if text_input:
    word_count = len(word_tokenize(text_input, language='french'))
    st.caption(f"📊 {word_count} mots")

# Bouton d'analyse
analyze_button = st.button("🔍 Analyser mon discours", type="primary", use_container_width=True)

# Traitement
if analyze_button:
    if not text_input.strip():
        st.error("⚠️ Veuillez entrer un texte à analyser")
    elif len(text_input.split()) < 10:
        st.warning("⚠️ Le texte est trop court (minimum 10 mots)")
    else:
        with st.spinner("Analyse en cours..."):
            analyzer = SpeechAnalyzer()
            feedback_gen = FeedbackGenerator()
            results = analyzer.analyze(text_input)
            feedback = feedback_gen.generate(results)
        
        st.success("✅ Analyse terminée !")
        st.divider()
        
        # Score global
        st.subheader("📊 Score Global")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            score = feedback['score_global']
            if score >= 7:
                delta_text = "Excellent"
            elif score >= 5:
                delta_text = "Bien"
            else:
                delta_text = "À améliorer"
            
            st.metric(label="Score", value=f"{score}/10", delta=delta_text)
        
        st.divider()
        
        # Feedback structuré
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader("✅ Points Forts")
            if feedback['points_forts']:
                for point in feedback['points_forts']:
                    st.success(point)
            else:
                st.info("Aucun point fort identifié pour le moment")
        
        with col_right:
            st.subheader("⚠️ Points à Améliorer")
            if feedback['points_amelioration']:
                for point in feedback['points_amelioration']:
                    st.warning(point)
            else:
                st.success("Rien à améliorer, excellent travail !")
        
        # Recommandations
        if feedback['recommandations']:
            st.divider()
            st.subheader("💡 Recommandations")
            for i, reco in enumerate(feedback['recommandations'], 1):
                st.info(f"**{i}.** {reco}")
        
        # Détails techniques
        st.divider()
        with st.expander("📈 Détails de l'analyse (avancé)"):
            st.markdown("### Statistiques")
            st.json(results['stats'])
            st.markdown("### Sentiment")
            st.json(results['sentiment'])
            st.markdown("### Mots de remplissage")
            st.json(results['fillers'])
            st.markdown("### Clarté")
            st.json(results['clarity'])
            st.markdown("### Structure")
            st.json(results['structure'])

# Pied de page
st.divider()
st.caption("📌 Développé par **Cheikh Niang** | Projet NLP Speech Analysis | Propulsé par Python & Streamlit")