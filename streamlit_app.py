import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- GESTION DE LA BASE DE DONNÉES LOCALE ---
DB_FILE = "evaluations_mobilite.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame()

def save_entry(data):
    df = pd.DataFrame([data])
    if not os.path.isfile(DB_FILE):
        df.to_csv(DB_FILE, index=False)
    else:
        df.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- CONFIGURATION DE L'INTERFACE ---
st.set_page_config(page_title="Performance Lab - Mobility", layout="wide")

# --- BARRE LATÉRALE : GESTION DES ATHLÈTES ---
st.sidebar.header("📋 Gestion des Athlètes")
data_load = load_data()

if not data_load.empty:
    # Nettoyage et préparation de la liste des athlètes
    data_load['full_name'] = data_load['prenom'].astype(str) + " " + data_load['nom'].astype(str)
    liste_athletes = ["+ Ajouter un nouvel athlète"] + sorted(data_load['full_name'].unique().tolist())
else:
    liste_athletes = ["+ Ajouter un nouvel athlète"]

choix_athlete = st.sidebar.selectbox("Sélectionner un athlète", liste_athletes)

if choix_athlete == "+ Ajouter un nouvel athlète":
    st.sidebar.subheader("Nouveau Profil")
    nom = st.sidebar.text_input("Nom")
    prenom = st.sidebar.text_input("Prénom")
    dob = st.sidebar.date_input("Date de Naissance", min_value=datetime(1950, 1, 1), value=datetime(2000, 1, 1))
    is_new = True
else:
    # Récupérer les infos de l'athlète sélectionné
    info = data_load[data_load['full_name'] == choix_athlete].iloc[0]
    nom = info['nom']
    prenom = info['prenom']
    dob = info['dob']
    st.sidebar.success(f"Profil actif : {prenom} {nom}")
    st.sidebar.info(f"Né(e) le : {dob}")
    is_new = False

# --- INTERFACE PRINCIPALE ---
st.title(f"🚀 Évaluation : {prenom} {nom}" if nom else "🚀 Lab de Mobilité")

if not nom or not prenom:
    st.info("👋 Bienvenue Coach ! Veuillez sélectionner un athlète ou en créer un nouveau dans le menu à gauche.")    e_ri_d = e1.number_input("Épaule RI D", value=60)
    e_re_d = e2.number_input("Épaule RE D", value=90)
    
    st.header("🏢 Tronc")
    th1, th2 = st.columns(2)
    thor_g = th1.number_input("Rot. Thoracique G", value=50)
    thor_d = th2.number_input("Rot. Thoracique D", value=50)

# --- SAUVEGARDE ---
if st.button("💾 Sauvegarder l'évaluation"):
    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "nom": nom,
        "prenom": prenom,
        "dob": dob,
        "h_ri_g": h_ri_g, "h_re_g": h_re_g, "h_ri_d": h_ri_d, "h_re_d": h_re_d,
        "ch_g": ch_g, "ch_d": ch_d,
        "e_ri_g": e_ri_g, "e_re_g": e_re_g, "e_ri_d": e_ri_d, "e_re_d": e_re_d,
        "thor_g": thor_g, "thor_d": thor_d,
        "t_flags": sum([t_q_g, t_f_g, t_it_g, t_q_d, t_f_d, t_it_d])
    }
    save_data(new_entry)
    st.success(f"Évaluation enregistrée pour {prenom} {nom} !")

# --- HISTORIQUE & VISUALISATION ---
st.divider()
st.header("📈 Historique de l'athlète")

if os.path.exists(DB_FILE):
    all_data = pd.read_csv(DB_FILE)
    athlete_history = all_data[(all_data['nom'] == nom) & (all_data['prenom'] == prenom)]
    
    if not athlete_history.empty:
        st.dataframe(athlete_history.sort_values(by="date", ascending=False))
        
        # Petit graphique d'évolution pour la cheville par exemple
        st.subheader("Évolution de la mobilité de cheville")
        st.line_chart(athlete_history.set_index("date")[["ch_g", "ch_d"]])
    else:
        st.info("Aucun historique pour cet athlète.")
else:
    st.info("Base de données vide. Créez la première évaluation !")
# --- SECTION CONSULTATION DU PASSÉ ---
if not is_new and not hist.empty:
    st.divider()
    st.header(f"🔍 Consultation des évaluations passées")
    
    # On crée une liste des dates disponibles pour cet athlète
    dates_dispo = hist['date'].unique().tolist()
    date_choisie = st.selectbox("Choisir une date pour voir le détail", sorted(dates_dispo, reverse=True))
    
    # On filtre les données pour cette date précise
    eval_precise = hist[hist['date'] == date_choisie].iloc[0]
    
    # Affichage en colonnes des résultats de l'époque
    c_past1, c_past2, c_past3 = st.columns(3)
    
    with c_past1:
        st.metric("Cheville G/D", f"{eval_precise['ch_g']} / {eval_precise['ch_d']} cm")
        st.metric("Thoracique G/D", f"{eval_precise['thor_g']}° / {eval_precise['thor_d']}°")
        
    with c_past2:
        st.metric("Hanche RI G/D", f"{eval_precise['h_ri_g']}° / {eval_precise['h_ri_d']}°")
        st.metric("Épaule RI G/D", f"{eval_precise['e_ri_g']}° / {eval_precise['e_ri_d']}°")
        
    with c_past3:
        st.write("**Flags Thomas Test :**")
        if eval_precise['t_flags'] == 0:
            st.success("Aucune raideur")
        else:
            st.warning(f"{int(eval_precise['t_flags'])} zone(s) de raideur")

    # Optionnel : Bouton pour comparer avec aujourd'hui
    st.info(f"💡 Cette évaluation a été réalisée le {date_choisie}. Tu peux voir l'évolution sur le graphique plus haut.")
