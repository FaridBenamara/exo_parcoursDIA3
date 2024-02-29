import pandas as pd


def lire_fichier_csv(chemin_fichier):
    """
    Cette fonction lit un fichier CSV et retourne un DataFrame pandas.
    - chemin_fichier : Chemin vers le fichier CSV à lire.
    """
    return pd.read_csv(chemin_fichier, low_memory=False)


def construire_dictionnaire_relations(df):
    """
    Construit un dictionnaire des relations amont-aval à partir d'un DataFrame.
    - df : DataFrame contenant les données des trajets.
    """
    sommets_depart = []
    sommets_arrivee = []
    dictionnaire_relations = {}
    identifiants_explorateurs = df['arete_id'].unique()

    for identifiant in identifiants_explorateurs:
        trajet = df[df['arete_id'] == identifiant]
        if trajet.empty:
            continue

        sommets_depart.append(trajet.iloc[0]['noeud_amont'])
        sommets_arrivee.append(trajet.iloc[-1]['noeud_aval'])

        for depart, arrivee in zip(trajet['noeud_amont'], trajet['noeud_aval']):
            if depart not in dictionnaire_relations:
                dictionnaire_relations[depart] = []
            dictionnaire_relations[depart].append(arrivee)

    return sommets_depart, sommets_arrivee, dictionnaire_relations


def calculer_statistiques(df):
    """
    Calcule et retourne les statistiques des chemins à partir d'un DataFrame.
    - df : DataFrame contenant les données des trajets.
    """
    somme_distances = df.groupby('arete_id')['distance'].sum()
    id_plus_long = somme_distances.idxmax()
    id_plus_court = somme_distances.idxmin()

    statistiques = {
        "Plus long chemin": (id_plus_long, somme_distances.max()),
        "Plus court chemin": (id_plus_court, somme_distances.min()),
        "Moyenne des distances": somme_distances.mean(),
        "Médiane des distances": somme_distances.median(),
        "Écart-type des distances": somme_distances.std(),
        "Écart interquartile des distances": somme_distances.quantile(0.75) - somme_distances.quantile(0.25)
    }

    return statistiques


def afficher_resultats(sommets_depart, sommets_arrivee, relations, statistiques):
    """
    Affiche les résultats des analyses effectuées.
    """
    print("Sommets de départ :", sommets_depart)
    print("Sommets d'arrivée :", sommets_arrivee)
    print("Relations  :", relations)
    print("\nStatistiques des chemins :")
    for cle, valeur in statistiques.items():
        print(f"{cle}: {valeur}")


def main():
    chemin_fichier = "parcours_explorateurs.csv"
    df_explorateurs = lire_fichier_csv(chemin_fichier)

    sommets_depart, sommets_arrivee, dictionnaire_relations = construire_dictionnaire_relations(df_explorateurs)
    statistiques_chemins = calculer_statistiques(df_explorateurs)

    afficher_resultats(sommets_depart, sommets_arrivee, dictionnaire_relations, statistiques_chemins)


if __name__ == "__main__":
    main()
