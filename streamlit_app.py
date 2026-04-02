import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- GESTION DE LA BASE DE DONNÉES LOCALE ---
DB_FILE = "evaluations_mobilite.csv"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame()
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
    info = data_load[data_load['full_name'] == choix_athlete].iloc[0]
    nom = info['nom']
    prenom = info['prenom']
    dob = info['dob']
    st.sidebar.success(f"Profil actif : {prenom} {nom}")
    is_new = False

# --- INTERFACE PRINCIPALE ---
st.title("🚀 Lab de Mobilité")

if not nom or not prenom:
    st.info("👋 Bienvenue Coach ! Veuillez sélectionner un athlète ou en créer un nouveau dans le menu à gauche.")
    st.stop()

# --- FORMULAIRE DE SAISIE ---
st.markdown(f"### 📝 Nouvelle Évaluation : {prenom} {nom}")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🦵 Bas du corps")
    c1, c2 = st.columns(2)
    h_ri_g = c1.number_input("Hanche RI Gauche (°)", 0, 90, 35)
    h_re_g = c2.number_input("Hanche RE Gauche (°)", 0, 90, 45)
    h_ri_d = c1.number_input("Hanche RI Droite (°)", 0, 90, 35)
    h_re_d = c2.number_input("Hanche RE Droite (°)", 0, 90, 45)
    ch_g = c1.number_input("Cheville G (cm)", 0.0, 30.0, 12.0)
    ch_d = c2.number_input("Cheville D (cm)", 0.0, 30.0, 12.0)

with col2:
    st.subheader("💪 Haut du corps & Tronc")
    e1, e2 = st.columns(2)
    e_ri_g = e1.number_input("Épaule RI G (°)", 0, 120, 60)
    e_re_g = e2.number_input("Épaule RE G (°)", 0, 120, 90)
    e_ri_d = e1.number_input("Épaule RI D (°)", 0, 120, 60)
    e_re_d = e2.number_input("Épaule RE D (°)", 0, 120, 90)
    thor_g = e1.number_input("Rot. Thoracique G (°)", 0, 90, 50)
    thor_d = e2.number_input("Rot. Thoracique D (°)", 0, 90, 50)

st.write("**Thomas Test (Cocher si raideur détectée)**")
t1, t2, t3, t4, t5, t6 = st.columns(6)
tqg = t1.checkbox("Quad G")
tfg = t2.checkbox("Flex G")
itg = t3.checkbox("ITB G")
tqd = t4.checkbox("Quad D")
tfd = t5.checkbox("Flex D")
itd = t6.checkbox("ITB D")

if st.button("💾 Enregistrer l'évaluation"):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H
