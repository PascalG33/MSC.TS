import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import BytesIO
from datetime import datetime
import os
os.makedirs("references", exist_ok=True)


# Fonction pour charger une référence spécifique depuis un fichier CSV
def load_reference(ref):
    try:
        df = pd.read_csv(f"references/{ref}.csv")
        return df.to_dict(orient="list")
    except FileNotFoundError:
        return None

# Fonction pour sauvegarder une référence spécifique dans un fichier CSV
def save_reference(ref, data):
    df = pd.DataFrame(data)
    df.to_csv(f"references/{ref}.csv", index=False)

# Fonction pour supprimer une référence
def delete_reference(ref):
    try:
        os.remove(f"references/{ref}.csv")
        st.success(f"La référence '{ref}' a été supprimée.")
    except FileNotFoundError:
        st.error(f"La référence '{ref}' n'existe pas.")

# Créer les onglets avec le nouveau nom pour l'onglet de calcul
tab_pepite, tab_classif = st.tabs(["Nouvelle Pépite !", "Tableau des Classifications"])

with tab_pepite:
    # Centrer le titre
    st.markdown("<h2 style='text-align: center;'>Nouvelle Pépite !</h2>", unsafe_allow_html=True)
    
    # Affichage du GIF centré pour engager l'utilisateur
    st.markdown(
        """
        <div style='display: flex; justify-content: center;'>
            <iframe src="https://giphy.com/embed/lIVbObSh0ewOSZvbLN" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Modification du texte d'invite pour la nouvelle référence
    ref = st.text_input("Rentre la référence de la nouvelle pépite")

    if ref:
        # Ajout des nouvelles classifications dans le selectbox
        classification = st.selectbox("Classification", [
            "1 2 - JUPE", "1 3 - PANTALON", "1 5 - ROBES", "1 6 - JEAN'S", "1 8 - ENSEMBLE",
            "2 1 - HAUT TENDANCE", "2 2 - TEE SHIRTS", "2 3 - CHEMISES", "2 4 - PULLS", "2 5 - GILETS",
            "3 2 - VESTES", "3 4 - MANTEAUX", "3 6 - BLOUSONS", "4 3 - BIJOUX"
        ], key="classification_calcul")
        
        # Ajout des nouvelles sous-classifications
        sous_classification = st.selectbox("Sous-classification", ["Basics", "Commerciales", "Audacieux", "Capsules"], key="sous_classification_calcul")
        sales_dates = st.text_area("Dates de Vente (une date par ligne, format jj/mm/aaaa)")
        sales_values = st.text_area("Quantités de Vente (valeurs négatives pour les retours)")
        periode = st.slider("Durée de Période (Jours)", 1, 31, 10, key="periode_calcul")

        if st.button("Calculer le Taux de Sortie"):
            if sales_dates.strip() and sales_values.strip():
                dates = sales_dates.strip().split('\n')
                ventes = [int(value) for value in sales_values.strip().split('\n') if value.isdigit()]
                data = sorted(zip(dates, ventes), key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))
                dates, ventes = zip(*data)
                periods = [ventes[i:i + periode] for i in range(0, len(ventes), periode)]
                dates_par_periode = [dates[i:i + periode] for i in range(0, len(dates), periode)]
                dates_par_periode = [d for d, p in zip(dates_par_periode, periods) if len(d) == len(p)]
                ventes_par_periode = [p for d, p in zip(dates_par_periode, periods) if len(d) == len(p)]
                min_length = min(len(dates_par_periode), len(ventes_par_periode))

                reference_data = {
                    "classification": [classification] * min_length,
                    "sous_classification": [sous_classification] * min_length,
                    "periodes": [f"Période {i+1}" for i in range(min_length)],
                    "taux_de_sortie": [round(sum(period) / len(period), 1) for period in ventes_par_periode[:min_length] if period],
                    "total_ventes": [sum(period) for period in ventes_par_periode[:min_length]],
                    "dates_par_periode": dates_par_periode[:min_length],
                    "ventes_par_periode": ventes_par_periode[:min_length],
                    "derniere_mise_a_jour": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * min_length,
                    "P": [periode] * min_length  # Utilisation du libellé "P" pour la durée de la période
                }
                save_reference(ref, reference_data)
                st.success("Référence ajoutée et calculée avec succès.")

with tab_classif:
    st.subheader("Taux de sortie")
    
    # Ajout des nouvelles classifications dans le selectbox de filtre
    classif_filter = st.selectbox("Classification", [
        "1 2 - JUPE", "1 3 - PANTALON", "1 5 - ROBES", "1 6 - JEAN'S", "1 8 - ENSEMBLE",
        "2 1 - HAUT TENDANCE", "2 2 - TEE SHIRTS", "2 3 - CHEMISES", "2 4 - PULLS", "2 5 - GILETS",
        "3 2 - VESTES", "3 4 - MANTEAUX", "3 6 - BLOUSONS", "4 3 - BIJOUX"
    ], key="classification_filter")
    
    # Ajout des nouvelles sous-classifications dans le selectbox de filtre
    sous_classif_filter = st.selectbox("Sous-classification", ["Basics", "Commerciales", "Audacieux", "Capsules"], key="sous_classification_filter")

    ref_list = [f.split('.')[0] for f in os.listdir("references") if f.endswith('.csv')]
    filtered_data = {ref: load_reference(ref) for ref in ref_list if load_reference(ref) and load_reference(ref).get("classification", [""])[0] == classif_filter and load_reference(ref).get("sous_classification", [""])[0] == sous_classif_filter}
  
    if filtered_data:
        table_data = []
        for ref, data in filtered_data.items():
            ref_row = {
                "Référence": ref,
                "Dernière Mise à Jour": data.get("derniere_mise_a_jour", [""])[0],
                "P": data.get("P", [""])[0]  # Utilisation de "P" comme nom de colonne
            }
            for i, (period, taux) in enumerate(zip(data.get("periodes", []), data.get("taux_de_sortie", [])), start=1):
                ref_row[f"P{i}"] = round(taux, 1)
            table_data.append(ref_row)
        df_filtered = pd.DataFrame(table_data)
        
        # Afficher le tableau avec les dates de mise à jour et période (P)
        st.write("### Taux de sortie")
        st.dataframe(df_filtered)

        # Création du graphique des taux de sortie par période pour chaque référence
        fig, ax = plt.subplots()
        
        # Calculer la période maximale parmi toutes les références
        max_periods = max(len(data.get("periodes", [])) for data in filtered_data.values())
        
        for ref, data in filtered_data.items():
            periods = data.get("periodes", [])
            taux_de_sortie = data.get("taux_de_sortie", [])
            
            # Compléter les données manquantes avec NaN pour aligner toutes les périodes
            if len(periods) < max_periods:
                periods += [f"Période {i+1}" for i in range(len(periods), max_periods)]
                taux_de_sortie += [None] * (max_periods - len(taux_de_sortie))

            ax.plot(periods, taux_de_sortie, marker="o", linestyle="-", label=ref)

        ax.set_title("Graphique des Taux de Sortie par Période")
        ax.set_xlabel("Période")
        ax.set_ylabel("Taux de Sortie")
        ax.legend(title="Références")

        # Rotation des étiquettes de l'axe x pour éviter le chevauchement
        plt.xticks(rotation=45)
        
        # Afficher le graphique
        st.pyplot(fig)

        # Bouton pour télécharger le graphique en PNG
        buf_graph = BytesIO()
        fig.savefig(buf_graph, format="png")
        buf_graph.seek(0)
        st.download_button(
            "Télécharger le graphique en PNG",
            data=buf_graph,
            file_name="graphique_taux_de_sortie.png",
            mime="image/png"
        )

        # Menu déroulant pour sélectionner et supprimer une référence
        ref_to_delete = st.selectbox("Sélectionner une référence à supprimer", [""] + list(filtered_data.keys()))
        if st.button("Supprimer la référence"):
            if ref_to_delete:
                delete_reference(ref_to_delete)
                st.experimental_rerun()  # Rafraîchir la page après suppression pour mettre à jour le tableau
            else:
                st.warning("Veuillez sélectionner une référence à supprimer.")
        
