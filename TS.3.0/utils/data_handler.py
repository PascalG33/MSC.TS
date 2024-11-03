# utils/data_handler.py
import pandas as pd
import os

def load_references(csv_file):
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        references = {}
        for _, row in df.iterrows():
            references[row['Référence']] = {
                "classification": row['Classification'],
                "sous_classification": row['Sous-classification'],
                "periodes": eval(row['periodes']),
                "taux_de_sortie": eval(row['taux_de_sortie']),
                "total_ventes": eval(row['total_ventes']),
                "derniere_mise_a_jour": row['derniere_mise_a_jour']
            }
        return references
    else:
        return {}

def save_references(data, csv_file):
    rows = []
    for ref, info in data.items():
        rows.append({
            "Référence": ref,
            "Classification": info['classification'],
            "Sous-classification": info['sous_classification'],
            "periodes": info['periodes'],
            "taux_de_sortie": info['taux_de_sortie'],
            "total_ventes": info['total_ventes'],
            "derniere_mise_a_jour": info['derniere_mise_a_jour']
        })
    df = pd.DataFrame(rows)
    df.to_csv(csv_file, index=False)

