import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURATION & DB ---
DB_FILE = "athletes_data.csv"

def save_data(data):
    df = pd.DataFrame([data])
    if not os.path.isfile(DB_FILE):
        df.to_csv(DB_FILE, index=False)
    else:
        df.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- UI CONFIG ---
st.set_page_config(page_title="Performance Lab", layout="wide")

# --- SIDEBAR : GESTION ATHLÈTE ---
st.sidebar.header("👤 Profil Athlète")
nom = st.sidebar.text_input("Nom")
prenom = st.sidebar.text_input("Prénom")
dob = st.sidebar.date_input("Date de Naissance (DOB)", min_value=datetime(1970, 1, 1))

athlete_id = f"{nom}_{prenom}_{dob}".replace(" ", "_").lower()

# --- MAIN INTERFACE ---
st.title("🚀 Évaluation Mobilité Haute Performance")

if not nom or not prenom:
    st.warning("⚠️ Veuillez entrer le nom et le prénom de l'athlète dans la barre latérale pour commencer.")
    st.stop()

# --- INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.header("🦵 Membres Inférieurs")
    c1, c2 = st.columns(2)
    h_ri_g = c1.number_input("Hanche RI Gauche", value=35)
    h_re_g = c2.number_input("Hanche RE Gauche", value=45)
    h_ri_d = c1.number_input("Hanche RI Droite", value=35)
    h_re_d = c2.number_input("Hanche RE Droite", value=45)
    
    ch_g = c1.number_input("Cheville Gauche (cm)", value=12.0)
    ch_d = c2.number_input("Cheville Droite (cm)", value=12.0)

    st.subheader("Thomas Test")
    t_col1, t_col2 = st.columns(2)
    t_q_g = t_col1.checkbox("Quad (G)")
    t_f_g = t_col1.checkbox("Fléchisseurs (G)")
    t_it_g = t_col1.checkbox("IT Band (G)")
    t_q_d = t_col2.checkbox("Quad (D)")
    t_f_d = t_col2.checkbox("Fléchisseurs (D)")
    t_it_d = t_col2.checkbox("IT Band (D)")

with col2:
    st.header("💪 Membres Supérieurs")
    e1, e2 = st.columns(2)
    e_ri_g = e1.number_input("Épaule RI G", value=60)
    e_re_g = e2.number_input("Épaule RE G", value=90)
    e_ri_d = e1.number_input("Épaule RI D", value=60)
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
