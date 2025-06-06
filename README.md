# 🎯 Projet d'Analyse de Marché - Services Web sur COMEUP

## 📋 Vue d'ensemble du projet

Ce projet consiste en une **analyse complète du marché des services de développement web** sur la plateforme française COMEUP. À travers une approche data-driven, nous avons collecté, nettoyé et analysé les données de **50 services de création de sites vitrines** pour identifier les tendances du marché et les opportunités business.

## 🛠️ Stack technique

- **Langage :** Python 🐍
- **Environnement :** Jupyter Notebook
- **Librairies principales :**
  - `pandas` - Manipulation et analyse des données
  - `matplotlib` & `seaborn` - Visualisations
  - `BeautifulSoup` - Web scraping (mentionné dans les objectifs)
  - `numpy` - Calculs numériques

## 📊 Données collectées

### Sources
- **Plateforme :** COMEUP.com (marketplace français de freelances)
- **Catégorie :** Services de création de sites vitrines
- **Volume :** 50 services analysés

### Variables analysées
- 👤 **Vendor_Name** : Nom du prestataire
- 📝 **Service_Description** : Description du service
- 💰 **Price** : Prix en livres sterling (£)
- ⭐ **Rating** : Note moyenne (sur 5)
- 📊 **Number_of_Ratings** : Nombre d'évaluations
- 🏷️ **Category** : Catégorie du service
- 🔧 **Techno_List** : Technologies utilisées
- 🎯 **Techno_Main** : Technologie principale
- 🔢 **Techno_Count** : Nombre de technologies
- ✅ **Is_Multi_Tech** : Service multi-technologies (booléen)

## 🎨 Visualisations créées

### 1. Analyse des prix
- Distribution des prix par catégorie
- Prix moyens vs médians
- Analyse de la dispersion des tarifs

### 2. Analyse technologique
- Top des technologies les plus utilisées
- Répartition mono vs multi-technologies
- Corrélation entre nombre de technologies et prix

### 3. Analyse qualité-prix
- Scatter plot Rating vs Prix
- Matrice de corrélation des variables numériques
- Analyse des vendors les plus performants

### 4. Dashboard de synthèse
- Métriques clés du marché
- Tendances par catégorie
- Vue d'ensemble du positionnement concurrentiel

## 📈 Insights principaux

### Technologies dominantes
- **WordPress** : Technologie la plus populaire
- **Divi** et **Elementor** : Page builders très demandés
- **NextJS**, **Wix**, **Webflow** : Technologies modernes émergentes

### Structure des prix
- Prix moyen observé : ~328£
- Grande variabilité selon les technologies
- Corrélation positive entre expertise technique et tarification

### Positionnement marché
- Services mono-technologie vs multi-technologies
- Impact du nombre d'évaluations sur la crédibilité
- Segmentation par catégories (Website Development, Web Design, SEO, etc.)

## 📁 Structure du projet

```
COMEUP/
├── data/
│   ├── raw/                    # Données brutes scrapées
│   └── processed/              # Données nettoyées (CSV final)
├── notebook/
│   ├── data/preprocessing/     # Nettoyage des données
│   └── visualization/          # Analyses et visualisations
├── README.md                   # Documentation projet
└── vizu.ipynb                  # Notebook principal d'analyse
```

## 🔄 Pipeline de données

1. **Extraction** : Scraping des données COMEUP
2. **Transformation** : Nettoyage et structuration (technologies, prix, catégories)
3. **Analyse** : Statistiques descriptives et visualisations
4. **Insights** : Identification des patterns et opportunités

## 💡 Applications business

Ce projet fournit une **base de données market intelligence** pour :
- 🎯 Définir une stratégie de pricing compétitive
- 🔧 Choisir les technologies à mettre en avant
- 📊 Identifier les niches sous-exploitées
- 👥 Comprendre les attentes clients du marché français

## 🚀 Évolutions possibles

- Expansion vers d'autres catégories de services
- Analyse temporelle (évolution des prix dans le temps)
- Intégration d'APIs pour automatiser la collecte
- Machine Learning pour prédiction de prix optimal

---

**Auteur :** Andrin'Ny Aina Razafinjato  
**Contact :** aina.razafinjato29@gmail.com  
**GitHub :** [AinaRazafinjato](https://github.com/AinaRazafinjato)