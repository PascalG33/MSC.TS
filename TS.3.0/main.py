import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from io import BytesIO
import os

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
    st.markdown("<h2 style='text-align: center;'>Nouvelle Pépite !</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='display: flex; justify-content: center;'>
            <iframe src="https://giphy.com/embed/lIVbObSh0ewOSZvbLN" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )
    ref = st.text_input("Rentre la référence de la nouvelle pépite")

    if ref:
        classification = st.selectbox("Classification", [
            "1 2 - JUPE", "1 3 - PANTALON", "1 5 - ROBES", "1 6 - JEAN'S", "1 8 - ENSEMBLE",
            "2 1 - HAUT TENDANCE", "2 2 - TEE SHIRTS", "2 3 - CHEMISES", "2 4 - PULLS", "2 5 - GILETS",
            "3 2 - VESTES", "3 4 - MANTEAUX", "3 6 - BLOUSONS", "4 3 - BIJOUX"
        ], key="classification_calcul")
        
        sous_classification = st.selectbox("Sous-classification", ["Basics", "Commerciales", "Audacieux", "Capsules"], key="sous_classification_calcul")
        sales_dates = st.text_area("Dates de Vente (une date par ligne, format jj/mm/aaaa)")
        sales_values = st.text_area("Quantités de Vente (valeurs négatives pour les retours)")
        periode = st.slider("Durée de Période (Jours)", 1, 31, 10, key="periode_calcul")

        if st.button("Calculer le Taux de Sortie"):
            if sales_dates.strip() and sales_values.strip():
                dates = [datetime.strptime(date, "%d/%m/%Y") for date in sales_dates.strip().split('\n')]
                ventes = [int(value) for value in sales_values.strip().split('\n') if value]
                sorted_data = sorted(zip(dates, ventes))
                dates, ventes = zip(*sorted_data)

                start_date = dates[0]
                end_date = dates[-1]
                all_periods = []

                while start_date <= end_date:
                    period_end_date = start_date + timedelta(days=periode)
                    period_dates = [date for date in dates if start_date <= date < period_end_date]
                    period_ventes = [ventes[i] for i, date in enumerate(dates) if start_date <= date < period_end_date]

                    if period_ventes:
                        total_ventes = sum(period_ventes)
                        taux_de_sortie = total_ventes / periode  # Moyenne par jour
                    else:
                        taux_de_sortie = 0  # Pas de ventes, taux de sortie défini à 0

                    all_periods.append({
                        "dates": period_dates,
                        "ventes": period_ventes,
                        "taux_de_sortie": round(taux_de_sortie, 2)
                    })

                    start_date = period_end_date

                reference_data = {
                    "classification": [classification] * len(all_periods),
                    "sous_classification": [sous_classification] * len(all_periods),
                    "periodes": [f"Période {i+1}" for i in range(len(all_periods))],
                    "taux_de_sortie": [p["taux_de_sortie"] for p in all_periods],
                    "total_ventes": [sum(p["ventes"]) for p in all_periods],
                    "dates_par_periode": [[d.strftime("%d/%m/%Y") for d in p["dates"]] for p in all_periods],
                    "ventes_par_periode": [p["ventes"] for p in all_periods],
                    "derniere_mise_a_jour": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * len(all_periods),
                    "P": [periode] * len(all_periods)
                }
                save_reference(ref, reference_data)
                st.success("Référence ajoutée et calculée avec succès.")

with tab_classif:
    st.subheader("Taux de sortie")
    classif_filter = st.selectbox("Classification", [
        "1 2 - JUPE", "1 3 - PANTALON", "1 5 - ROBES", "1 6 - JEAN'S", "1 8 - ENSEMBLE",
        "2 1 - HAUT TENDANCE", "2 2 - TEE SHIRTS", "2 3 - CHEMISES", "2 4 - PULLS", "2 5 - GILETS",
        "3 2 - VESTES", "3 4 - MANTEAUX", "3 6 - BLOUSONS", "4 3 - BIJOUX"
    ], key="classification_filter")
    
    sous_classif_filter = st.selectbox("Sous-classification", ["Basics", "Commerciales", "Audacieux", "Capsules"], key="sous_classification_filter")

    ref_list = [f.split('.')[0] for f in os.listdir("references") if f.endswith('.csv')]
    filtered_data = {ref: load_reference(ref) for ref in ref_list if load_reference(ref) and load_reference(ref).get("classification", [""])[0] == classif_filter and load_reference(ref).get("sous_classification", [""])[0] == sous_classif_filter}

    if filtered_data:
        table_data = []
        for ref, data in filtered_data.items():
            ref_row = {
                "Référence": ref,
                "Dernière Mise à Jour": data.get("derniere_mise_a_jour", [""])[0],
                "P": data.get("P", [""])[0]
            }
            for i, taux in enumerate(data.get("taux_de_sortie", []), start=1):
                ref_row[f"P{i}"] = taux
            table_data.append(ref_row)
        
        df_filtered = pd.DataFrame(table_data)
        st.write("### Taux de sortie")
        st.dataframe(df_filtered)

        fig, ax = plt.subplots()
        max_periods = max(len(data.get("periodes", [])) for data in filtered_data.values())

        for ref, data in filtered_data.items():
            periods = data.get("periodes", [])
            taux_de_sortie = data.get("taux_de_sortie", [])
            
            if len(periods) < max_periods:
                periods += [f"Période {i+1}" for i in range(len(periods), max_periods)]
                taux_de_sortie += [0] * (max_periods - len(taux_de_sortie))  # Mettre à zéro pour périodes sans vente

            ax.plot(periods, taux_de_sortie, marker="o", linestyle="-", label=ref)

        ax.set_title("Graphique des Taux de Sortie par Période")
        ax.set_xlabel("Période")
        ax.set_ylabel("Taux de Sortie")
        ax.legend(title="Références")
        plt.xticks(rotation=45)
        
        st.pyplot(fig)

        buf_graph = BytesIO()
        fig.savefig(buf_graph, format="png")
        buf_graph.seek(0)
        st.download_button(
            "Télécharger le graphique en PNG",
            data=buf_graph,
            file_name="graphique_taux_de_sortie.png",
            mime="image/png"
        )

        ref_to_delete = st.selectbox("Sélectionner une référence à supprimer", [""] + list(filtered_data.keys()))
        if st.button("Supprimer la référence"):
            if ref_to_delete:
                delete_reference(ref_to_delete)
                st.experimental_rerun()
            else:
                st.warning("Veuillez sélectionner une référence à supprimer.")
