import streamlit as st

st.set_page_config(page_title="Performance Mobility Tool", layout="wide")

st.title("🚀 Diagnostic de Mobilité Haute Performance")
st.write("Entrez les mesures pour voir les alertes (Flags) s'afficher.")

# --- FONCTIONS DE DIAGNOSTIC ---
def check_flag(val, green, yellow, label):
    if val >= green:
        st.success(f"✅ {label} : {val} (Optimal)")
    elif val >= yellow:
        st.warning(f"🟡 {label} : {val} (Yellow Flag - Compensation)")
    else:
        st.error(f"🔴 {label} : {val} (Red Flag - Priorité)")

# --- INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.header("🦵 Bas du corps")
    
    # Cheville
    st.subheader("Cheville (Knee-to-wall)")
    ch_g = st.number_input("Gauche (cm)", 0.0, 30.0, 12.0)
    ch_d = st.number_input("Droite (cm)", 0.0, 30.0, 12.0)
    check_flag(ch_g, 12, 10, "Cheville G")
    check_flag(ch_d, 12, 10, "Cheville D")
    if abs(ch_g - ch_d) > 1.5:
        st.error("⚠️ ASYMÉTRIE CHEVILLE > 1.5cm")

    # Hanche
    st.subheader("Hanche (Rotation Interne)")
    h_ri_g = st.number_input("RI Gauche (°)", 0, 90, 35)
    h_ri_d = st.number_input("RI Droite (°)", 0, 90, 35)
    check_flag(h_ri_g, 35, 25, "Hanche RI G")
    check_flag(h_ri_d, 35, 25, "Hanche RI D")

with col2:
    st.header("💪 Haut du corps & Tronc")
    
    # Thoracique
    st.subheader("Rotation Thoracique")
    th_g = st.number_input("Rot. Gauche (°)", 0, 90, 50)
    th_d = st.number_input("Rot. Droite (°)", 0, 90, 50)
    check_flag(th_g, 50, 40, "Thorax G")
    check_flag(th_d, 50, 40, "Thorax D")

    # Épaule
    st.subheader("Épaule (Arc Total RI+RE)")
    e_ri_g = st.number_input("Épaule RI G", 0, 120, 60)
    e_re_g = st.number_input("Épaule RE G", 0, 120, 90)
    e_ri_d = st.number_input("Épaule RI D", 0, 120, 60)
    e_re_d = st.number_input("Épaule RE D", 0, 120, 90)
    
    arc_g = e_ri_g + e_re_g
    arc_d = e_ri_d + e_re_d
    check_flag(arc_g, 150, 130, "Arc Épaule G")
    check_flag(arc_d, 150, 130, "Arc Épaule D")

st.divider()

# --- THOMAS TEST ---
st.header("📋 Thomas Test & Synthèse")
t_cols = st.columns(6)
t1 = t_cols[0].checkbox("Quad G")
t2 = t_cols[1].checkbox("Flex G")
t3 = t_cols[2].checkbox("ITB G")
t4 = t_cols[3].checkbox("Quad D")
t5 = t_cols[4].checkbox("Flex D")
t6 = t_cols[5].checkbox("ITB D")

total_t = sum([t1, t2, t3, t4, t5, t6])
if total_t == 0:
    st.success("✅ Chaîne antérieure : Mobile")
else:
    st.error(f"🔴 Raideur détectée : {total_t} zone(s) impactée(s)")
