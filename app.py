import streamlit as st
import pandas as pd
from datetime import date
import os
import time

# --- CONFIGURATION LOOK & FEEL ---
st.set_page_config(page_title="Hybrid Coach Pro", page_icon="⚡", layout="centered")

# Custom CSS pour un look "App Mobile"
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #007bff; color: white; }
    .stProgress > div > div > div > div { background-color: #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
PROGRAMME = {
    "Lundi: Poitrine/Triceps": {
        "main": ["Incline Machine Press", "Cable Crossover bas -> haut", "Flat DB Press", "Cable Crossover horiz", "Dips lestés", "Rope Pushdown", "Overhead DB Extension", "Diamond Push-ups"],
        "correctif": ["Face Pull câble", "Reverse Fly haltères"]
    },
    "Mardi: Dos/Gainage": {
        "main": ["Hollow Body", "L-Sit Tuck", "Dead Hang actif", "Australian Pull-ups", "Tractions large", "Tractions supi", "Straight Arm Pulldown", "Ab Wheel", "Dragon Flag Tuck"],
        "correctif": []
    },
    "Mercredi: Jambes": {
        "main": ["Leg Extension", "Leg Press", "Hack Squat", "Smith Squat", "Romanian Deadlift", "Leg Curl Couché", "Bulgarian Split Squat", "Calf Raises"],
        "correctif": []
    },
    "Vendredi: Épaules/Biceps": {
        "main": ["Lateral Raise", "Seated DB Press", "Rear Delt Face Pull", "Cable Lateral Raise", "Barbell Curl", "Hammer Curl", "Concentration Curl"],
        "correctif": ["Face Pull câble", "Cuban Press léger", "Prone Y-T-W"]
    },
    "Samedi: Full Body": {
        "main": ["Australian Pull-ups", "Dips parallèles", "Tractions large", "Pistol Squat assisté", "Pike Push-up", "L-Sit Tuck"],
        "correctif": ["Dragon Flag Tuck", "Ab Wheel genoux", "Hollow Body", "Side Plank"]
    }
}

def load_data(file): return pd.read_csv(file) if os.path.exists(file) else pd.DataFrame()
def save_entry(df, file):
    old = load_data(file)
    pd.concat([old, df], ignore_index=True).to_csv(file, index=False)

# --- LOGIQUE D'INTERFACE ---
st.title("⚡ Hybrid Coach v1.4")

tabs = st.tabs(["🏋️ Entraînement", "🥗 Nutrition", "📏 Physique", "📊 Stats"])

# --- TAB 1: ENTRAÎNEMENT ---
with tabs[0]:
    jour = st.selectbox("Session actuelle", list(PROGRAMME.keys()))
    
    # 🚨 Rappel Protocole Épaule (Source: [cite: 9, 10])
    with st.expander("🚨 PROTOCOLE ÉPAULE (AVANT SÉANCE)", expanded=False):
        st.write("3x20 Band Pull-Apart | 3x20 Face Pull | 3x15 Rotation Externe")
        st.checkbox("Protocole validé ✅")

    # Saisie des séries
    ex = st.selectbox("Exercice", PROGRAMME[jour]["main"])
    
    # Historique (Bio-feedback)
    logs = load_data("workout_logs.csv")
    if not logs.empty:
        prev = logs[logs['Exercice'] == ex].tail(1)
        if not prev.empty:
            st.warning(f"Dernière perf: {prev['Poids'].values[0]}kg x {prev['Reps'].values[0]}")

    with st.form("log_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        w = c1.number_input("Poids (kg)", step=0.5)
        r = c2.number_input("Reps", step=1)
        rpe = st.select_slider("Intensité (RPE)", options=range(1,11), value=8)
        note = st.text_input("Note / Gêne épaule")
        if st.form_submit_button("VALIDER SÉRIE"):
            save_entry(pd.DataFrame([[date.today(), ex, w, r, rpe, note]], columns=["Date", "Exercice", "Poids", "Reps", "RPE", "Note"]), "workout_logs.csv")
            st.success("Série enregistrée !")

    # 🔧 Renforcement Correctif (Source: )
    if PROGRAMME[jour]["correctif"]:
        st.subheader("🔧 Renforcement Fin de Séance")
        for c_ex in PROGRAMME[jour]["correctif"]:
            st.checkbox(f"{c_ex} (Correctif)")

# --- TAB 2: NUTRITION (Source: [cite: 66, 68]) ---
with tabs[1]:
    st.header("Plan Alimentaire Recomposition")
    repas = ["Repas 1: Pré-workout", "Repas 2: Post-workout", "Repas 3: Midi", "Repas 4: Après-midi", "Repas 5: Dîner", "Repas 6: Pré-sommeil"]
    for r in repas:
        st.checkbox(r)
    st.info("Objectif: 2500-2800 kcal | 220-240g Protéines")

# --- TAB 3: PHYSIQUE (Source: [cite: 71]) ---
with tabs[2]:
    st.header("Check-in Mensurations")
    with st.form("physique_form"):
        col1, col2 = st.columns(2)
        p = col1.number_input("Poids (kg)", value=116.0)
        t = col2.number_input("Taille/Nombril (cm)")
        bras = col1.number_input("Bras (cm)")
        cuisse = col2.number_input("Cuisse (cm)")
        if st.form_submit_button("ENREGISTRER MESURES"):
            save_entry(pd.DataFrame([[date.today(), p, t, bras, cuisse]], columns=["Date", "Poids", "Taille", "Bras", "Cuisse"]), "metrics.csv")
            st.balloons()
