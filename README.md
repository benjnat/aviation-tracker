# Aviation Tracker - Trajectoires d'avions LFMT

Ce projet permet de générer des fichiers GeoJSON contenant les trajectoires d'avions autour de l'aéroport de Montpellier (LFMT) à partir des données OpenSky Network.

## Prérequis

- Python 3.8+
- Un compte OpenSky Network (pour accéder aux données historiques via Trino)

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/benjnat/aviation-tracker.git
cd aviation-tracker
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration OpenSky

Pour utiliser l'API Trino d'OpenSky et accéder aux données historiques, vous devez :

1. Créer un compte sur [OpenSky Network](https://opensky-network.org/)
2. Configurer vos identifiants (voir la [documentation pyopensky](https://open-aviation.github.io/pyopensky/))

## Utilisation

Exécutez le script pour générer un fichier GeoJSON avec les trajectoires des 30 derniers jours :

```bash
python script_generate_lfmt_geojson_colored.py
```

Le script va :
- Récupérer les données ADS-B des vols autour de LFMT (zone définie)
- Reconstruire les trajectoires de chaque avion
- Attribuer une couleur selon l'altitude moyenne :
  - 🔴 **Rouge** : Basse altitude (< 3000m)
  - 🟠 **Orange** : Moyenne altitude (3000-10000m)
  - 🔵 **Bleu** : Haute altitude (> 10000m)
- Générer le fichier `lfmt_month_lines_colored.geojson`

## Paramètres personnalisables

Dans le script `script_generate_lfmt_geojson_colored.py`, vous pouvez modifier :

- **Période temporelle** : `start` et `stop` (actuellement 30 jours)
- **Zone géographique** : `bounds` (lon_min, lat_min, lon_max, lat_max)
- **Nom du fichier de sortie** : `output_file`
- **Seuils d'altitude** pour la classification des couleurs

## Format de sortie

Le fichier GeoJSON généré contient :
- Une **LineString** par trajectoire d'avion
- Des **propriétés** pour chaque trajectoire :
  - `icao24` : Identifiant unique de l'avion
  - `callsign` : Indicatif de vol
  - `avg_altitude` : Altitude moyenne (en mètres)
  - `num_points` : Nombre de points de la trajectoire
  - `color` : Code couleur hex
  - `category` : Catégorie d'altitude

## Visualisation

Vous pouvez visualiser le fichier GeoJSON avec :
- [geojson.io](https://geojson.io/)
- QGIS
- Leaflet / Mapbox
- Ou tout autre outil compatible GeoJSON

## Ressources

- [Documentation pyopensky](https://open-aviation.github.io/pyopensky/)
- [OpenSky Network](https://opensky-network.org/)
- [Format GeoJSON](https://geojson.org/)

## Licence

MIT
