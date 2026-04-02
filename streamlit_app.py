import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(page_title="Performance Mobility Tool", layout="wide")

st.title("🚀 Évaluation Mobilité Haute Performance")
st.write("Outil de diagnostic instantané (Sans sauvegarde)")

# --- INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.header("🦵 Bas du corps")
    c1, c2 = st.columns(2)
    # Hanche
    h_ri_g = c1.number_input("Hanche RI Gauche (°)", 0, 90, 35)
    h_re_g = c2.number_input("Hanche RE Gauche (°)", 0, 90, 45)
    h_ri_d = c1.number_input("Hanche RI Droite (°)", 0, 90, 35)
    h_re_d = c2.number_input("Hanche RE Droite (°)", 0, 90, 45)
    # Cheville
    ch_g = c1.number_input("Cheville Gauche (cm)", 0.0, 30.0, 12.0)
    ch_d = c2.number_input("Cheville Droite (cm)", 0.0, 30.0, 12.0)
    
    st.subheader("Thomas Test")
    t_col1, t_col2 = st.columns(2)
    tq_g = t_col1.checkbox("Quad G")
    tf_g = t_col1.checkbox("Flex G")
    it_g = t_col1.checkbox("ITB G")
    tq_d = t_col2.checkbox("Quad D")
    tf_d = t_col2.checkbox("Flex D")
    it_d = t_col2.checkbox("ITB D")

with col2:
    st.header("💪 Haut du corps & Tronc")
    e1, e2 = st.columns(2)
    # Épaule
    e_ri_g = e1.number_input("Épaule RI G (°)", 0, 120, 60)
    e_re_g = e2.number_input("Épaule RE G (°)", 0, 120, 90)
    e_ri_d = e1.number_input("Épaule RI D (°)", 0, 120, 60)
    e_re_d = e2.number_input("Épaule RE D (°)", 0, 120, 90)
    # Thoracique
    th_g = e1.number_input("Rot. Thoracique G (°)", 0, 90, 50)
    th_d = e2.number_input("Rot. Thoracique D (°)", 0, 90, 50)

# --- LOGIQUE DE DIAGNOSTIC ---
