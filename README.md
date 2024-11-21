Voici un exemple de **README.md** détaillé pour vos deux scripts de scraping. Il inclut une présentation, les étapes d'installation, d'exécution, et des exemples de données extraites. 

---

# Aramisauto Scraping Project

Ce projet contient deux scripts Python permettant de scraper des données depuis la marketplace de vente de voitures d'occasion d'Aramisauto. Les scripts extraient des informations détaillées sur les véhicules disponibles, y compris leurs caractéristiques techniques, leurs prix, et leur disponibilité.

## Contenu

- **Script 1** : `extraction.py`  
  Scrape les données globales sur plusieurs véhicules d'Aramisauto.  
- **Script 2** : `main.py`  
  Récupère les détails d'un véhicule spécifique à partir de son URL.

---

## Prérequis

- Python 3.7 ou une version ultérieure
- **Modules Python** :
  - selenium
  - webdriver-manager
  - beautifulsoup4 (pour le script 2)

Installez les dépendances en exécutant la commande suivante dans le répertoire du projet :

```bash
pip install -r requirements.txt
```

---

## Fonctionnalités

### Script 1 : `extraction.py`

- **Description** :  
  Parcourt plusieurs pages d'annonces de véhicules pour extraire des informations clés, telles que le modèle, le prix, et les caractéristiques principales.  
- **Sortie** : Enregistre un fichier JSON (`detailed_data.json`) contenant les informations de toutes les voitures trouvées.

#### Exemple d'exécution

```bash
python extract_car_data.py
```

#### Exemple de données extraites

```json
[
    {
        "id": "123456",
        "marque": "Peugeot",
        "modele": "208",
        "title": "Peugeot 208 1.2 PureTech",
        "motorisation": "Essence",
        "finition": "Allure",
        "fuel_type": "Essence",
        "transmission": "Manuelle",
        "year": "2022",
        "mileage": "15 000 km",
        "price": "18 990 €",
        "availability": "En stock",
        "image_url": "https://images.aramisauto.com/peugeot-208.jpg",
        "link": "https://www.aramisauto.com/voitures/peugeot/208/?vehicleId=123456"
    }
]
```

---

### Script 2 : `main.py`

- **Description** :  
  Récupère les informations détaillées d'un véhicule spécifique en fournissant son URL.  

- **Sortie** : Renvoie un dictionnaire Python avec des sections clés comme la consommation, les options, les équipements, et les points techniques.  

#### Exemple d'exécution

```bash
python get_vehicle_data.py
```

Modifiez l’URL dans le script principal (`url = "https://www.aramisauto.com/...`) pour tester avec différents véhicules.

#### Exemple de données extraites

```json
{
    "reference": "RV831073",
    "price": "22 490 €",
    "availability": "Disponible sous 5 jours",
    "technical_data": {
        "Boîte de vitesses": "Manuelle",
        "Carburant": "Essence",
        "Nombre de portes": "5",
        "Sellerie": "Tissu"
    },
    "equipments": ["Climatisation automatique", "Radar de recul", "Régulateur de vitesse"],
    "options": [
        {
            "name": "Peinture métallisée",
            "price": "450 €"
        }
    ],
    "consumption": {
        "Consommation mixte": "5,9 L/100km",
        "Émission de CO₂": "135 g/km"
    },
    "vehicle_protection": ["Garantie constructeur", "Assistance 24/7"],
    "warranty": ["Garantie 12 mois", "Extension possible"],
    "funding": {
        "Durée": "48 mois",
        "Mensualité": "249 €/mois"
    },
    "key_points": {
        "Puissance moteur": "130 chevaux",
        "Volume de coffre": "380 L"
    },
    "delivery": "Livraison gratuite à domicile"
}
```

---

## Architecture des fichiers

```
.
├── extraction.py.py  # Script de scraping global
├── main.py.py  # Script de scraping détaillé
├── requirements.txt     # Liste des dépendances
└── README.md            # Documentation
```

---

## Limitations

- Le site Aramisauto peut modifier sa structure, ce qui rendrait les scripts non fonctionnels.
- Le temps de scraping peut augmenter avec le nombre de pages demandées.
- L'usage massif de scraping peut être détecté par le site, ce qui pourrait entraîner un blocage.

---

## Améliorations futures

- Ajouter une gestion des erreurs plus robuste pour les cas où les éléments ne sont pas disponibles.
- Implémenter un système de cache pour éviter de scraper les mêmes pages plusieurs fois.
- Utiliser une base de données pour stocker les résultats au lieu d’un fichier JSON.

---

## Auteur

- **Nom** : Thibaut TALOM  
- **Email** : thibaut.talom@tetrisnews.fr  
- **GitHub** : [DepotGitHub]([https://github.com/VotreProfilGitHub](https://github.com/Schmied07/Aramisauto.git))  

--- 

Avec ce README, vos utilisateurs pourront facilement comprendre et utiliser vos scripts.
