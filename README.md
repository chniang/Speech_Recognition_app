# 🎤 Speech Analysis & Feedback System

Système d'analyse NLP pour discours et prises de parole, avec génération automatique de feedback intelligent.

## 🌐 Démo en ligne

**Application déployée** : https://speechrecognitionapp-notgexojl2z4metcq9t6ud.streamlit.app/

## ✨ Fonctionnalités

- ✅ **Analyse de sentiment** optimisée pour le français avec dictionnaires personnalisés
- ✅ **Détection de clarté** basée sur la longueur des phrases
- ✅ **Analyse de structure** et détection des mots de transition
- ✅ **Détection de mots parasites** ("euh", "donc", "en fait", etc.)
- ✅ **Feedback automatisé** avec recommandations actionnables
- ✅ **Interface responsive** fonctionnelle sur mobile et desktop

## 🚀 Installation locale
```bash
git clone https://github.com/chniang/Speech_Recognition_app.git
cd Speech_Recognition_app
pip install -r requirements.txt
streamlit run app.py
```

## 💻 Technologies utilisées

- **Python 3.10+**
- **Streamlit** : Framework d'interface web
- **NLTK** : Natural Language Toolkit pour le traitement de texte
- **TextBlob** : Analyse de sentiment
- **Pandas** : Manipulation de données

## 📊 Métriques analysées

### Analyse textuelle
- Nombre de mots et phrases
- Richesse du vocabulaire
- Longueur moyenne des phrases

### Sentiment
- Détection du ton (positif/négatif/neutre)
- Score de polarité
- Niveau de subjectivité

### Qualité du discours
- Taux de mots de remplissage
- Clarté du message
- Présence de structure et transitions

## 🎯 Évolutions futures (Roadmap MVP Werekaan)

- 🎙️ **Module d'analyse vocale** : débit, pauses, intonation (Whisper + librosa)
- 🎥 **Module d'analyse gestuelle** : posture, gestes, expressions faciales (MediaPipe)
- 📊 **Système de scoring global** combinant texte + voix + gestuelle
- 📹 **Enregistrement vidéo intégré** dans l'interface
- 💾 **Base de données** pour suivi de progression des utilisateurs
- 📈 **Dashboard analytics** pour enseignants

## 👨‍💻 Auteur

**Cheikh Niang** - Data Scientist Junior  
Projet développé dans le cadre de la formation en Data Science et NLP appliqué.

## 📄 Licence

Projet open source pour usage éducatif et professionnel.
