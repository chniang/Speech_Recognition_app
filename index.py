# APPLICATION DE RECONNAISSENCE VOCALE AMELIOREE BASEE SUR (SPEECH-RECOGNITION)

# importation des bibliotheques
import streamlit as st
import speech_recognition as sr
import os
import datetime
import time

# definir une fonction de reconnaissence vocale
def transcribe_speech (recognizer, source, api_choice, language_code):
    
    """ecoute l'audio et utilise l'API specifiee pour la trasncription"""
    # ajustement au bruit ambiant
    try:
        # ecoute le bruit pandent 0.5 seconde pour ameliorer la qualite
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
    except Exception as e:
        st.error(f"Erreur lors de l'ajustement du bruit ambiant:{e}")
        return "Erreur d'initiation audio."
    
    st.info("Parlez maintenant...") # Correction: st.infos -> st.info
    
    try:
        # ecouter la parole
        audio_text = recognizer.listen(source)
    except sr.WaitTimeoutError: # Correction: st.WaitTimeoutError -> sr.WaitTimeoutError
        return "Aucune parole detectee.Veuillez reessayer"
    except Exception as e:
        st.error(f"Erreur lors de l'ecoute:{e}")
        return "Erreur lors de l'ecoute du microphone"
    
    st.info("Transcription en cours")
            
    try:
        # utiliser l'API de reconnaissence vocale choisie
        if api_choice == "Google Speech Recognition (Web)":
            text = recognizer.recognize_google(audio_text, language=language_code)
        elif api_choice == "Sphinx (Hors Ligne)":
            text = recognizer.recognize_sphinx(audio_text, language=language_code) # Correction: recognise_sphinx -> recognize_sphinx
        elif api_choice == "Microsoft Azure":
            st.warning("Cette API necessite la cle d'abonnement azure.")
            text = recognizer.recognize_azure(audio_text, language=language_code, key="VOTRE CLE AZURE") # Correction: lannguage -> language
        elif api_choice == "Wit.ai (Meta)":
            st.warning("Ctette API necessite la cle du developpeur de Wit.ai")
            text = recognizer.recognize_wit(audio_text, key="VOTRE CLE WIT_AI") # Correction: recognise_wit -> recognize_wit
        elif api_choice == "Autres API (Deepgram, AssemblyAI)":
            st.warning("Les API externes necessite des bibliotheques supplementaires.")
            text = recognizer.recognize_google(audio_text, language=language_code)
        else:
            text = "API non specifiee."
            
        return text
    # gestion des erreurs specifiees
    except sr.UnknownValueError:
        return "Desole l'API n'a pas compris ce que vous avez dit."
    except sr.RequestError as e: # Correction: suppression de l'exception précédente qui était en double
        return f"Erreur de service ({api_choice}). Verifiez votre connexion ou votre cle API: {e}" 
    except Exception as e:
        return f"Une erreur inattendue s'est produite:{e}" # Ajout de la dernière exception générique
    
# fonction pour sauvegarder le text transcrit
def save_transcription(text_to_save):
    # verifie si la transcription est valide avant de sauvegarder
    if text_to_save and text_to_save not in ["Desole l'API n'a pas compris ce que vous avez dit.", "Aucune parole detectee.Veuillez reessayer"]:
        save_dir = "transcriptions" # Correction de la majuscule "Transcriptions" -> "transcriptions" (meilleure pratique)
        os.makedirs(save_dir, exist_ok=True) # Correction: os.makdirs -> os.makedirs
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"transcription_{timestamp}.txt" # Correction de la majuscule "Transcription" -> "transcription"
        save_path = os.path.join(save_dir, file_name)
        
        
        try:
            with open(save_path,"w",encoding="utf-8") as f:
                f.write(f"Transcription({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
                f.write(f"API utilisee:{st.session_state.api_used}\n\n")
                f.write(text_to_save)
            st.sidebar.success(f"✅ Texte enregistré dans : {file_name}") # Correction: st.sidebar.succes -> st.sidebar.success
        except Exception as e:
            st.sidebar.error(f"Erreur lors de la sauvegarde : {e}")
    else:
        st.sidebar.warning("Rien de valide à enregistrer.")
        
# fonction principal
def main():
    st.title("Application de reconnaissence Vocale 🎙️")
    
    # --- EXPLICATION DU MODE D'UTILISATION (DEMANDÉ) ---
    st.subheader("📝 Mode d'Utilisation")
    st.markdown("""
    Pour utiliser cette application de reconnaissance vocale :

    ### 1. Configuration (Barre Latérale)
    * **Choisir la language parlee :** Sélectionnez la langue que vous allez utiliser (Français, Anglais, etc.) pour garantir la meilleure précision.
    * **Choisir l'API de reconnaissence :** Vous avez le choix entre plusieurs services. **Google Speech Recognition (Web)** est le plus recommandé pour la précision. Les autres (Azure, Wit.ai) nécessitent des clés d'abonnement externes.

    ### 2. Démarrer et Enregistrer
    * Cliquez sur **▶️ Démarrer l'enregistrement**. L'application attendra que vous parliez.
    * Parlez clairement dans votre microphone après avoir vu le message **"Parlez maintenant..."**.
    * Le texte transcrit s'affichera au bas de la page.

    ### 3. Contrôle et Sauvegarde
    * Le bouton **⏸️ Arrêter Provisoirement** est une simulation pour indiquer que vous ne parlez plus.
    * Cliquez sur **💾 Enregistrer la transcription** pour sauvegarder le texte dans un fichier `.txt` unique dans le dossier `transcriptions/` sur votre ordinateur.
    """)
    st.markdown("---")
    # --- FIN EXPLICATION ---

    
    # initialisation de l'etat de session
    if 'transcribed_text' not in st.session_state: # Correction: transcibed_text -> transcribed_text
        st.session_state.transcribed_text = ""
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False # controle letat denregistrement
    if 'api_used' not in st.session_state:
        st.session_state.api_used = "Google Speech Recognition (Web)" # Correction de l'étoile
        
        
    # barre laterale: configuration
    st.sidebar.title("⚙️ Configuration")
    # choix de la langue
    LANGUAGES = {
        "Français (France)": "fr-FR",
        "Anglais (États-Unis)": "en-US",
        "Espagnol": "es-ES",
        "Arabe": "ar-SA",
        "Autre...": ""
    }
    
    lang_choice = st.sidebar.selectbox("Choisir la language parlee", list(LANGUAGES.keys()))
    language_code = LANGUAGES[lang_choice] # Correction: langage_code -> language_code
    
    # choix de l'API de reconnaissence vocale
    API_CHOICES = [
        "Google Speech Recognition (Web)", 
        "Sphinx (Hors Ligne)", 
        "Microsoft Azure", 
        "Wit.ai (Meta)", 
        "Autres API (Deepgram, AssemblyAI)"
    ]
    
    api_choice = st.sidebar.selectbox("Choisir l'API de reconnaissence", API_CHOICES, help="Les APIs autres que Google et Sphinx nécessitent des clés d'abonnement.") # Correction: slectbox -> selectbox
    st.session_state.api_used = api_choice 
    # zone principale: controle
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Démarrer la reconnaissance
        if st.button("▶️ Démarrer l'enregistrement", type="primary", disabled=st.session_state.is_running):
            st.session_state.is_running = True
            r = sr.Recognizer()
            # Utilisation de st.spinner pour une meilleure UX pendant l'écoute
            with st.spinner(f"Écoute active en {lang_choice}..."):
                with sr.Microphone() as source:
                    text = transcribe_speech(r, source, api_choice, language_code)
                    st.session_state.transcribed_text = text
            st.session_state.is_running = False # Terminé
            st.rerun() # Rafraîchit l'affichage du résultat
            
    with col2:
        # Fonctionnalité Pause/Reprise (Simulée)
        if st.session_state.is_running:
            if st.button("⏸️ Arrêter Provisoirement"):
                st.session_state.is_running = False
                st.warning("Interruption demandée. Le flux audio va s'arrêter immédiatement.")
                # Le st.rerun dans col1 gère l'arrêt après la transcription
        else:
            # Bouton inactif quand rien ne tourne
            st.button("⏸️ Pause (Inactif)", disabled=True)
    
    with col3:
        # Sauvegarde du texte
        if st.button("💾 Enregistrer la transcription", disabled=(not st.session_state.transcribed_text or st.session_state.is_running)):
            save_transcription(st.session_state.transcribed_text)

    st.markdown("---")
    
    # Affichage de la transcription
    if st.session_state.transcribed_text:
        st.subheader("Transcription :")
        st.success(st.session_state.transcribed_text)
        st.markdown(f"*API utilisée pour la dernière transcription : **{st.session_state.api_used}***")
    elif not st.session_state.is_running:
        st.info("Prêt à commencer. Configurez les options à gauche et cliquez sur Démarrer.")

if __name__ == "__main__":
    main()