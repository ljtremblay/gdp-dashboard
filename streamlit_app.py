import streamlit as st

st.set_page_config(page_title="Athlete Mobility Tracker", layout="wide")

st.title("🚀 Évaluation Mobilité Haute Performance")
st.write("Entrez les mesures pour générer le rapport de Flags.")

col1, col2 = st.columns(2)

with col1:
    st.header("Mesures")
    # Cheville
    st.subheader("Cheville (cm)")
    ch_g = st.number_input("Gauche", value=12.0)
    ch_d = st.number_input("Droite", value=12.0)
    
    # Hanche RI
    st.subheader("Hanche RI (Degrés)")
    h_ri_g = st.number_input("Hanche RI G", value=35)
    h_ri_d = st.number_input("Hanche RI D", value=35)
    
    # Épaule RI
    st.subheader("Épaule RI (Degrés)")
    e_ri_g = st.number_input("Épaule RI G", value=60)
    e_ri_d = st.number_input("Épaule RI D", value=60)

with col2:
    st.header("Tests Qualitatifs")
    # Thoracique
    st.subheader("Thoracique (Degrés)")
    thor_rot = st.slider("Rotation Thoracique", 0, 90, 50)
    
    # Thomas Test
    st.subheader("Thomas Test")
    thomas_g = st.selectbox("Côté Gauche", ["Green (OK)", "Yellow (Psoas/Droit Fémoral)", "Red (Douleur)"])
    thomas_d = st.selectbox("Côté Droit", ["Green (OK)", "Yellow (Psoas/Droit Fémoral)", "Red (Douleur)"])

# --- ALGORITHME DE DIAGNOSTIC ---
st.divider()
st.header("📊 Rapport de Diagnostic")

def get_status(val, green, yellow):
    if val >= green: return "🟢 GREEN", "Normal"
    if val >= yellow: return "🟡 YELLOW", "Alerte / Compensation"
    return "🔴 RED", "Priorité Corrective"

# Affichage des résultats
res1, res2, res3, res4, res5 = st.columns(5)

with res1:
    status, msg = get_status(min(ch_g, ch_d), 12, 10)
    asym = abs(ch_g - ch_d)
    if asym > 1.5: status, msg = "🟡 YELLOW", "Asymétrie > 1.5cm"
    st.metric("Cheville", status, msg)

with res2:
    status, msg = get_status(min(h_ri_g, h_ri_d), 35, 25)
    if abs(h_ri_g - h_ri_d) > 10: status, msg = "🔴 RED", "Asymétrie majeure"
    st.metric("Hanche RI", status, msg)

with res3:
    status, msg = get_status(thor_rot, 50, 40)
    st.metric("Thoracique", status, msg)

with res4:
    status, msg = get_status(min(e_ri_g, e_ri_d), 60, 45)
    st.metric("Épaule RI", status, msg)

with res5:
    t_status = "🟢 GREEN" if "Green" in thomas_g and "Green" in thomas_d else "🟡 YELLOW"
    if "Red" in thomas_g or "Red" in thomas_d: t_status = "🔴 RED"
    st.metric("Thomas Test", t_status)
