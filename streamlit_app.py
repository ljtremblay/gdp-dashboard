import streamlit as st

st.set_page_config(page_title="Performance Mobility Tracker", layout="wide")

st.title("🚀 Évaluation Mobilité Haute Performance")
st.write("Analyse biomécanique précise des amplitudes articulaires.")

# --- SECTION INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.header("🦵 Membres Inférieurs")
    
    # Hanche
    st.subheader("Hanche (Degrés)")
    c1, c2 = st.columns(2)
    h_ri_g = c1.number_input("RI Gauche", value=35)
    h_re_g = c2.number_input("RE Gauche", value=45)
    h_ri_d = c1.number_input("RI Droite", value=35)
    h_re_d = c2.number_input("RE Droite", value=45)
    
    # Cheville
    st.subheader("Cheville (Knee-to-wall cm)")
    ch_g = c1.number_input("Cheville Gauche", value=12.0)
    ch_d = c2.number_input("Cheville Droite", value=12.0)

    # Thomas Test
    st.subheader("Thomas Test (Raideur détectée)")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.write("**Gauche**")
        t_q_g = st.checkbox("Quad (G)", key="qg")
        t_f_g = st.checkbox("Fléchisseurs (G)", key="fg")
        t_it_g = st.checkbox("IT Band (G)", key="itg")
    with t_col2:
        st.write("**Droite**")
        t_q_d = st.checkbox("Quad (D)", key="qd")
        t_f_d = st.checkbox("Fléchisseurs (D)", key="fd")
        t_it_d = st.checkbox("IT Band (D)", key="itd")

with col2:
    st.header("💪 Membres Supérieurs & Tronc")
    
    # Épaule
    st.subheader("Épaule (Degrés)")
    e1, e2 = st.columns(2)
    e_ri_g = e1.number_input("RI Épaule G", value=60)
    e_re_g = e2.number_input("RE Épaule G", value=90)
    e_ri_d = e1.number_input("RI Épaule D", value=60)
    e_re_d = e2.number_input("RE Épaule D", value=90)
    
    # Thoracique
    st.subheader("Rotation Thoracique (Degrés)")
    th1, th2 = st.columns(2)
    thor_g = th1.number_input("Rotation Gauche", value=50)
    thor_d = th2.number_input("Rotation Droite", value=50)

# --- LOGIQUE DE DIAGNOSTIC ---
st.divider()
st.header("📊 Rapport de Flags")

def get_flag(val, green, yellow, lower_is_better=False):
    if lower_is_better: # Pour les asymétries par exemple
        return "🟢" if val <= green else "🟡" if val <= yellow else "🔴"
    return "🟢" if val >= green else "🟡" if val >= yellow else "🔴"

res1, res2, res3, res4 = st.columns(4)

with res1:
    st.subheader("Hanches")
    min_ri = min(h_ri_g, h_ri_d)
    asym_h = abs((h_ri_g + h_re_g) - (h_ri_d + h_re_d))
    st.write(f"RI Min: {get_flag(min_ri, 35, 25)}")
    st.write(f"Asymétrie Arc: {get_flag(asym_h, 10, 15, True)}")

with res2:
    st.subheader("Épaules")
    arc_g = e_ri_g + e_re_g
    arc_d = e_ri_d + e_re_d
    st.write(f"Arc G ({arc_g}°): {get_flag(arc_g, 150, 130)}")
    st.write(f"Arc D ({arc_d}°): {get_flag(arc_d, 150, 130)}")
    if abs(e_ri_g - e_ri_d) > 15: st.warning("⚠️ GIRD détecté (Déficit RI)")

with res3:
    st.subheader("Thoracique")
    st.write(f"Gauche: {get_flag(thor_g, 50, 40)}")
    st.write(f"Droite: {get_flag(thor_d, 50, 40)}")

with res4:
    st.subheader("Thomas Test")
    bad_flags = sum([t_q_g, t_f_g, t_it_g, t_q_d, t_f_d, t_it_d])
    if bad_flags == 0: st.success("🟢 Full Clear")
    elif bad_flags <= 2: st.warning("🟡 Raideurs mineures")
    else: st.error("🔴 Chaîne antérieure verrouillée")

# --- RÉSUMÉ PRIORITÉS ---
if min(ch_g, ch_d) < 10 or min(thor_g, thor_d) < 40:
    st.info("💡 **Priorité Coach :** Travail de mobilité cheville/thorax requis pour protéger les lombaires.")
