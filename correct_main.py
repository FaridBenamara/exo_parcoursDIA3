import pandas as pd
import numpy as np

# Chargement des données depuis le fichier CSV
df = pd.read_csv('parcours_explorateurs.csv')

# Création de dictionnaires pour relier les nœuds et pour stocker les distances entre eux
dict_relations = df.set_index('noeud_amont')['noeud_aval'].to_dict()
dict_distances = df.set_index(['noeud_amont', 'noeud_aval'])['distance'].to_dict()

# Identification des noeuds de départ et d'arrivée
noeuds_depart = df[df['type_aretes'] == 'depart']['noeud_amont'].unique()
noeuds_arrivee = df[df['type_aretes'] == 'arrivee']['noeud_aval'].unique()


# Fonction pour construire un trajet à partir d'un noeud de départ
def construire_trajet(noeud_depart):
    trajet = [noeud_depart]
    distance_totale = 0

    while trajet[-1] not in noeuds_arrivee:
        noeud_actuel = trajet[-1]
        if noeud_actuel not in dict_relations:
            return None, 0
        noeud_suivant = dict_relations[noeud_actuel]
        trajet.append(noeud_suivant)
        distance_totale += dict_distances.get((noeud_actuel, noeud_suivant), 0)

    return trajet, distance_totale


# Collecte de tous les trajets et de leur longueur
trajets = []
longueurs = []

# Construction des trajets pour chaque point de départ
for depart in noeuds_depart:
    trajet, longueur_trajet = construire_trajet(depart)
    if trajet and len(trajet) == 10:
        trajets.append(trajet)
        longueurs.append(longueur_trajet)

# Calcul des statistiques sur les trajets trouvés
if longueurs:
    longueur_max = max(longueurs)
    longueur_min = min(longueurs)
    moyenne = np.mean(longueurs)
    mediane = np.median(longueurs)
    ecart_type = np.std(longueurs)
    q1, q3 = np.percentile(longueurs, [25, 75])
    ecart_interquartile = q3 - q1

# Affichage des trajets
print("Parcours:")
for trajet in trajets:
    print(trajet)

# Affichage des statistiques
print(f"Le chemin le plus long: {longueur_max}")
print(f"Le chemin le plus court: {longueur_min}")
print(f"Moyenne des longueurs: {moyenne}")
print(f"Médiane des longueurs: {mediane}")
print(f"Écart-type des longueurs: {ecart_type}")
print(f"Écart interquartile des longueurs: {ecart_interquartile}")
