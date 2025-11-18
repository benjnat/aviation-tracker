# script_generate_lfmt_geojson_colored.py

from pyopensky.trino import Trino
from datetime import datetime, timedelta
import geojson
import pandas as pd

# ----------------------------
# CONFIGURATION
# ----------------------------

# Intervalle temporel : dernier mois
stop = datetime.utcnow()
start = stop - timedelta(days=30)

# Zone autour de LFMT (Montpellier)
bounds = (3.87, 43.52, 4.07, 43.65)  # lon_min, lat_min, lon_max, lat_max

# Nom du fichier GeoJSON à générer
output_file = "lfmt_month_lines_colored.geojson"

# ----------------------------
# CONNEXION OpenSky
# ----------------------------

trino = Trino()  # Assure-toi d'avoir un compte OpenSky si nécessaire

# Récupération des messages ADS-B
print("Récupération des données ADS-B...")
df = trino.history(
    start=start,
    stop=stop,
    bounds=bounds
)

if df is None or df.empty:
    print("Aucune donnée trouvée pour la période et la zone spécifiées.")
    exit()

print(f"Nombre de messages récupérés : {len(df)}")

# ----------------------------
# NETTOYAGE ET TRI
# ----------------------------

# Suppression des lignes avec lat/lon manquantes
df = df.dropna(subset=['lat', 'lon'])

# Tri par icao24 et timestamp pour reconstruire les trajectoires
df = df.sort_values(by=['icao24', 'time'])

# ----------------------------
# CONSTRUCTION DES TRAJECTOIRES
# ----------------------------

features = []
icao_list = df['icao24'].unique()

print(f"Nombre d'avions détectés : {len(icao_list)}")

for icao in icao_list:
    flight_df = df[df['icao24'] == icao].copy()
    
    # Création de la liste de coordonnées [lon, lat, alt]
    coords = flight_df[['lon', 'lat', 'altitude']].values.tolist()
    
    # Si moins de 2 points, on ignore
    if len(coords) < 2:
        continue
    
    # Obtenir le callsign s'il existe
    callsign = flight_df['callsign'].dropna().iloc[0] if 'callsign' in flight_df.columns and not flight_df['callsign'].dropna().empty else icao
    
    # Altitude moyenne pour attribuer une couleur
    avg_alt = flight_df['altitude'].mean()
    
    # Classification par altitude
    if avg_alt < 3000:
        color = "#FF0000"  # Rouge : basse altitude
        category = "Basse altitude (<3000m)"
    elif avg_alt < 10000:
        color = "#FFA500"  # Orange : moyenne altitude
        category = "Moyenne altitude (3000-10000m)"
    else:
        color = "#0000FF"  # Bleu : haute altitude
        category = "Haute altitude (>10000m)"
    
    # Création de la LineString GeoJSON
    line = geojson.LineString(coords)
    
    # Propriétés associées
    properties = {
        "icao24": icao,
        "callsign": str(callsign),
        "avg_altitude": round(avg_alt, 2),
        "num_points": len(coords),
        "color": color,
        "category": category
    }
    
    feature = geojson.Feature(geometry=line, properties=properties)
    features.append(feature)

# ----------------------------
# GÉNÉRATION DU FICHIER GEOJSON
# ----------------------------

feature_collection = geojson.FeatureCollection(features)

with open(output_file, 'w') as f:
    geojson.dump(feature_collection, f, indent=2)

print(f"Fichier GeoJSON généré : {output_file}")
print(f"Nombre de trajectoires exportées : {len(features)}")
