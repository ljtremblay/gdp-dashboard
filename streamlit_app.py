import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- DATABASE ---
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

# --- UI ---
st.set_page_config(page_title="Performance Lab", layout="wide")

# --- SIDEBAR ---
st.sidebar.header("📋 Gestion Athlètes")
df_all = load_data()

if not df_all.empty:
    df_all['full_name'] = df_all['prenom'].astype(str) + " " + df_all['nom'].astype(str)
    options = ["+ Nouveau"] + sorted(df_all['full_name'].unique().tolist())
else:
    options = ["+ Nouveau"]

choix = st.sidebar.selectbox("Athlète", options)

if choix == "+ Nouveau":
    nom = st.sidebar.text_input("Nom")
    prenom = st.sidebar.text_input("Prénom")
    dob = st.sidebar.date_input("DOB", value=datetime(2000, 1, 1))
    is_new = True
else:
    info = df_all[df_all['full_name'] == choix].iloc[0]
    nom, prenom, dob = info['nom'], info['prenom'], info['dob']
    st.sidebar.success(f"Profil : {prenom} {nom}")
    is_new = False

# --- MAIN ---
st.title("🚀 Lab de Mobilité")

if not nom or not prenom:
    st.info("Sélectionnez ou créez un athlète à gauche.")
    st.stop()

st.subheader(f"Évaluation : {prenom} {nom}")
c1, c2 = st.columns(2)

with c1:
    st.write("**Bas du corps**")
    hri_g = st.number_input("Hanche RI G (°)", 0, 90, 35)
    hre_g = st.number_input("Hanche RE G (°)", 0, 90, 45)
    hri_d = st.number_input("Hanche RI D (°)", 0, 90, 35)
    hre_d = st.number_input("Hanche RE D (°)", 0, 90, 45)
    ch_g = st.number_input("Cheville G (cm)", 0.0, 30.0, 12.0)
    ch_d = st.number_input("Cheville D (cm)", 0.0, 30.0, 12.0)

with c2:
    st.write("**Haut & Tronc**")
    eri_g = st.number_input("Épaule RI G (°)", 0, 120, 60)
    ere_g = st.number_input("Épaule RE G (°)", 0, 120, 90)
    eri_d = st.number_input("Épaule RI D (°)", 0, 120, 60)
    ere_d = st.number_input("Épaule RE D (°)", 0, 120, 90)
    th_g = st.number_input("Rot. Thoracique G (°)", 0, 90, 50)
    th_d = st.number_input("Rot. Thoracique D (°)", 0, 90, 50)

st.write("**Thomas Test**")
t_cols = st.columns(6)
t1 = t_cols[0].checkbox("Quad G")
t2 = t_cols[1].checkbox("Flex G")
t3 = t_cols[2].checkbox("ITB G")
t4 = t_cols[3].checkbox("Quad D")
t5 = t_cols[4].checkbox("Flex D")
t6 = t_cols[5].checkbox("ITB D")

if st.button("💾 Enregistrer"):
    d_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = {
        "date": d_str, "nom": nom, "prenom": prenom, "dob": str(dob),
        "h_ri_g": hri_g, "h_re_g": hre_g, "h_ri_d": hri_d, "h_re_d": hre_d,
        "ch_g": ch_g, "ch_d": ch_d, "e_ri_g": eri_g, "e_re_g": ere_g,
        "e_ri_d": eri_d, "e_re_d": ere_d, "thor_g": th_g, "thor_d": th_d,
        "t_flags": sum([t1, t2, t3, t4, t5, t6])
    }
    save_entry(entry)
    st.success("Données sauvées !")
    st.rerun()

# --- HISTORIQUE ---
if not is_new and not df_all.empty:
    st.divider()
    h = df_all[df_all['full_name'] == choix].sort_values("date", ascending=False)
    if not h.empty:
        st.write("### Historique")
        st.line_chart(h.set_index("date")[["ch_g", "ch_d"]])
        date_sel = st.selectbox("Ancienne séance", h['date'].tolist())
        v = h[h['date'] == date_sel].iloc[0]
        m1, m2, m3 = st.columns(3)
        m1.metric("Cheville G/D", f"{v['ch_g']}/{v['ch_d']}")
        m2.metric("Hanche RI G/D", f"{v['h_ri_g']}/{v['h_ri_d']}")
        m3.metric("Épaule RI G/D", f"{v['e_ri_g']}/{v['e_ri_d']}")
