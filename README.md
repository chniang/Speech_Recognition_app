

# 🎤 Application de Reconnaissance Vocale Avancée (Streamlit)

Ce projet est une application web interactive construite avec **Streamlit** et utilisant la bibliothèque **SpeechRecognition** pour offrir une solution de transcription vocale robuste et configurable.

L'objectif de cet exercice était d'améliorer les fonctionnalités de base pour offrir une expérience utilisateur supérieure et une flexibilité technique.

---

## 🚀 Fonctionnalités Clés

L'application intègre les améliorations suivantes :

* **Sélection d'API :** L'utilisateur peut choisir entre plusieurs moteurs de reconnaissance vocale, incluant **Google Speech Recognition (Web)**, **Sphinx (Hors Ligne)**, **Microsoft Azure**, et **Wit.ai (Meta)**.
* **Choix de la Langue :** Configuration explicite de la langue parlée (`fr-FR`, `en-US`, `es-ES`, etc.) pour améliorer la précision de la transcription.
* **Gestion des Erreurs Améliorée :** Des messages d'erreur spécifiques et significatifs sont affichés pour les problèmes de connexion (`RequestError`), l'audio incompris (`UnknownValueError`), ou l'absence de parole.
* **Sauvegarde des Transcriptions :** Un bouton permet d'enregistrer le texte transcrit dans un fichier `.txt` unique (horodaté) au sein d'un dossier `transcriptions/`.
* **Contrôle de l'Enregistrement :** Boutons **Démarrer** et **Arrêter Provisoirement** pour contrôler le flux d'écoute du microphone.

---

## ⚙️ Installation et Exécution

Suivez ces étapes pour installer et lancer l'application sur votre machine.

### Prérequis

* Python 3.8+
* Un microphone fonctionnel
* Le gestionnaire de paquets `pip`

### 1. Cloner le Dépôt

Ouvrez votre terminal et clonez le dépôt :

```bash
git clone [https://github.com/chniang/Speech_Recognition_app.git](https://github.com/chniang/Speech_Recognition_app.git)
cd Speech_Recognition_app
2. Créer et Activer l'Environnement Virtuel
Il est fortement recommandé d'utiliser un environnement virtuel :

Bash

# Créer l'environnement (si ce n'est pas déjà fait)
python -m venv .venv

# Activer l'environnement
# Sur Windows (PowerShell) :
.venv\Scripts\Activate
# Sur Linux/macOS :
source .venv/bin/activate
3. Installer les Dépendances
Installez les bibliothèques requises, y compris PyAudio pour l'accès au microphone :

Bash

pip install streamlit SpeechRecognition pyaudio
NOTE : Si l'installation de pyaudio échoue, consultez la documentation ou cherchez une version précompilée (.whl) spécifique à votre OS/version de Python.

4. Lancer l'Application
Exécutez l'application Streamlit :

Bash

streamlit run index.py
L'application s'ouvrira automatiquement dans votre navigateur par défaut (http://localhost:8501).

📖 Mode d'Emploi
Configuration : Utilisez la barre latérale (⚙️ Configuration) pour choisir la Langue que vous allez parler (ex: Français (France)) et l'API que vous souhaitez tester.

Démarrer : Cliquez sur ▶️ Démarrer l'enregistrement. Le message Parlez maintenant... apparaîtra.

Parler : Énoncez clairement votre texte. L'application ajustera le microphone au bruit ambiant avant d'écouter.

Résultat : La transcription s'affiche dans la zone principale.

Sauvegarder : Cliquez sur 💾 Enregistrer la transcription pour créer un fichier .txt horodaté dans le dossier local transcriptions/.

💡 Notes sur les APIs
Google Speech Recognition (Web) : Recommandé pour sa précision, nécessite une connexion Internet.

Sphinx (Hors Ligne) : Fonctionne sans Internet, mais la précision est souvent inférieure.

Azure et Wit.ai : Nécessitent des clés d'abonnement (clés non incluses dans le code). Si vous sélectionnez ces options sans fournir de clé valide, l'application affichera un message d'erreur de service.
