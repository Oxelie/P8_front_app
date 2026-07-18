# Projet 8 — Interface Streamlit de segmentation d'image pour voiture autonome

Interface de démonstration pour le projet de segmentation sémantique d'images urbaines (véhicule autonome).  
Développée avec Streamlit, déployée sur Azure App Service.

---

## Contexte

Ce dépôt contient uniquement le **frontend** (application Streamlit).  
L'API Flask backend est maintenue dans le dépôt `P8_api_app`.  
Le code d'entraînement des modèles est maintenu dans le dépôt `P8_Segmentation_Images`.

---

## Fonctionnement

L'interface permet de :

1. **Sélectionner une image** parmi les 11 images de test disponibles (subset Frankfurt, Cityscapes)
2. **Visualiser** l'image originale et le masque de segmentation réel côte à côte
3. **Lancer une prédiction** et afficher le masque généré par le modèle

> La prédiction peut prendre 30 à 60 secondes (inférence CPU sur Azure B1).

---

## Structure

```
P8_front_app/
│
├── app.py           # Application Streamlit
├── Procfile         # Commande de démarrage pour Azure App Service
└── requirements.txt # Dépendances Python
```

---

## Configuration

L'application se connecte à l'API via la variable d'environnement `API_URL` :

```bash
# Par défaut (développement local)
API_URL=http://127.0.0.1:4444

# En production (Azure)
API_URL=https://projet8-api.azurewebsites.net
```

---

## Lancer l'application en local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'API (dépôt P8_api_app) dans un autre terminal au préalable

# Lancer Streamlit
API_URL=http://127.0.0.1:4444 streamlit run app.py
```

---

## Déploiement Azure

| Ressource | Détail |
|-----------|--------|
| App Service | `projet8-front` (Sweden Central) |
| Plan | B1 (partagé avec l'API) |
| URL | `https://projet8-front.azurewebsites.net` |

> **État actuel :** l'application est **arrêtée** (économies — coût Azure même sans trafic). L'API (`projet8-api`) doit également être redémarrée avant utilisation. Redémarrage en moins d'une minute.

### Déploiement via zip deploy

```bash
zip -r front.zip . -x "*.git*" -x "__pycache__/*" -x "*.DS_Store"

az webapp deployment source config-zip \
  --resource-group rg-projet8 \
  --name projet8-front \
  --src front.zip
```

### Gestion des crédits Azure

> **État actuel :** l'App Service est **arrêtée** (économies). Redémarrer aussi l'API (`projet8-api`) avant utilisation.

```bash
# Redémarrer avant démonstration (API + frontend)
az webapp start --name projet8-api --resource-group rg-projet8
az webapp start --name projet8-front --resource-group rg-projet8

# Remettre en pause après démonstration
az webapp stop --name projet8-front --resource-group rg-projet8
az webapp stop --name projet8-api --resource-group rg-projet8
```

---

## Dépendances

```
streamlit
requests
```
