import streamlit as st
import pandas as pd
from datetime import date
import os
import time
from PIL import Image

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="Hybrid Coach Pro", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #00ff00; }
    .stCheckbox { background-color: #1e2130; padding: 10px; border-radius: 8px; margin-bottom: 5px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #1e2130; border-radius: 5px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- STRUCTURE DU PROGRAMME (DÉPART SAMEDI : POITRINE/TRICEPS) ---
PROGRAMME = {
    "1. Samedi: Salle - Poitrine/Triceps": {
        "main": ["Incline Machine Press (90°)", "Cable Crossover bas->haut", "Flat DB Press (Partiel)", "Dips lestés (90°)", "Rope Pushdown", "Overhead DB Extension", "Diamond Push-ups"],
        "correctif": ["Face Pull câble", "Reverse Fly haltères"]
    },
    "2. Dimanche: Repos Actif / Mobilité": {
        "main": ["Marche LISS (40 min)", "Mobilité Épaule", "Étirements légers"],
        "correctif": ["Protocole Épaule Complet"]
    },
    "3. Lundi: Callisthénie - Dos/Gainage": {
        "main": ["Hollow Body Hold", "L-Sit Tuck", "Dead Hang actif", "Australian Pull-ups", "Tractions large", "Ab Wheel"],
        "correctif": ["Face Pull élastique"]
    },
    "4. Mardi: Salle - Jambes": {
        "main": ["Leg Extension", "Leg Press Large", "Hack Squat", "Romanian Deadlift", "Leg Curl Couché", "Bulgarian Split Squat", "Calf Raises"],
        "correctif": ["Mobilité Hanche"]
    },
    "5. Mercredi: Repos Actif / Cardio": {
        "main": ["Marche LISS (40 min)", "Gainage statique"],
        "correctif": ["Protocole Épaule Complet"]
    },
    "6. Jeudi: Salle - Épaules/Biceps": {
        "main": ["Lateral Raise (Léger)", "Seated DB Press (Partiel)", "Rear Delt Face Pull", "Cable Lateral Raise", "Barbell Curl", "Hammer Curl"],
        "correctif": ["Cuban Press léger", "Prone Y-T-W"]
    },
    "7. Vendredi: Callisthénie - Full Body": {
        "main": ["Australian Pull-ups", "Dips parallèles", "Pike Push-up mural", "Pistol Squat assisté", "L-Sit Tuck", "Dragon Flag Tuck"],
        "correctif": ["Hollow Body"]
    }
}

def load_data(file): return pd.read_csv(file) if os.path.exists(file) else pd.DataFrame()
def save_entry(df, file):
    old = load_data(file)
    pd.concat([old, df], ignore_index=True).to_csv(file, index=False)

# --- INTERFACE ---
st.title("🦾 Hybrid Coach : Recomposition")

tabs = st.tabs(["🏋️ Séance", "📏 Physique", "🥗 Nutrition", "📊 Stats"])

# --- TAB 1: SÉANCE ---
with tabs[0]:
    jour_key = st.selectbox("Sélectionner la session", list(PROGRAMME.keys()))
    
    st.error("🚨 OBLIGATOIRE : Protocole Épaule (Band Pull-Apart / Face Pull / Rotation)")
    st.checkbox("Protocole validé ✅", key="check_proto")

    st.divider()
    ex = st.selectbox("Exercice", PROGRAMME[jour_key]["main"])
    
    # Rappel Record
    logs = load_data("workout_logs.csv")
    if not logs.empty:
        prev = logs[logs['Exercice'] == ex].tail(1)
        if not prev.empty:
            st.metric("Dernière fois", f"{prev['Poids'].values[0]} kg", f"{prev['Reps'].values[0]} reps")

    with st.form("set_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        w = c1.number_input("Poids", step=0.5)
        r = c2.number_input("Reps", step=1)
        rpe = c3.select_slider("RPE", options=range(1,11), value=8)
        note = st.text_input("Gêne épaule / Note")
        if st.form_submit_button("VALIDER SÉRIE"):
            save_entry(pd.DataFrame([[date.today(), ex, w, r, rpe, note]], columns=["Date", "Exercice", "Poids", "Reps", "RPE", "Note"]), "workout_logs.csv")
            st.success("Enregistré !")

    if PROGRAMME[jour_key]["correctif"]:
        st.subheader("🔧 Renforcements Fin de Séance")
        for c_ex in PROGRAMME[jour_key]["correctif"]:
            st.checkbox(f"Fait : {c_ex}")

# --- TAB 2: PHYSIQUE & PHOTOS ---
with tabs[1]:
    st.header("Check-in & Photos")
    
    # Section Photos
    st.subheader("📸 Photos du jour")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        img_file = st.file_uploader("Face / Profil / Dos", type=['jpg', 'png', 'jpeg'])
    if img_file:
        st.image(img_file, caption="Aperçu du jour", use_container_width=True)
    
    # Section Mensurations
    st.divider()
    with st.form("body_form"):
        c1, c2 = st.columns(2)
        poids = c1.number_input("Poids (kg)", value=116.0)
        taille = c2.number_input("Taille/Nombril (cm)")
        bras = c1.number_input("Bras (cm)")
        epaules = c2.number_input("Épaules (cm)")
        if st.form_submit_button("SAUVEGARDER CHECK-IN"):
            save_entry(pd.DataFrame([[date.today(), poids, taille, bras, epaules]], columns=["Date", "Poids", "Taille", "Bras", "Epaules"]), "metrics.csv")
            st.success("Données enregistrées !")

# --- TAB 3: NUTRITION ---
with tabs[2]:
    st.header("Discipline Alimentaire")
    st.info("Objectif : Déficit modéré | 2.5g Prot/kg")
    repas = ["Repas 1 (Pré-workout)", "Repas 2 (Post-workout)", "Repas 3 (Midi)", "Repas 4 (Collation)", "Repas 5 (Dîner)", "Repas 6 (Caséine)"]
    for r in repas:
        st.checkbox(r)
