import streamlit as st
import pandas as pd
from datetime import date
import os
import time

# --- CONFIGURATION STYLE AVANCÉE ---
st.set_page_config(page_title="Hybrid Coach Premium", page_icon="🦾", layout="centered")

# CSS pour injecter du dynamisme et de la lisibilité
st.markdown("""
    <style>
    /* Fond général sombre mais plus profond */
    .main { background-color: #05070a; color: #e0e0e0; }
    
    /* Boutons : Bleu électrique et texte blanc gras pour lisibilité max */
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.5em; 
        background-color: #0070f3; 
        color: white !important; 
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 14px 0 rgba(0,118,255,0.39);
    }
    
    /* Cartes pour les exercices */
    .exercise-card {
        background-color: #111418;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #0070f3;
        margin-bottom: 20px;
    }
    
    /* Onglets plus visibles */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1c1f26;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #a0a0a0;
    }
    .stTabs [aria-selected="true"] { background-color: #0070f3 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DONNÉES DU PROGRAMME ---
PROGRAMME = {
    "1. Samedi: Poitrine/Triceps (Salle)": {
        "main": ["Incline Machine Press (90°)", "Cable Crossover bas->haut", "Flat DB Press (Partiel)", "Dips lestés (90°)", "Rope Pushdown", "Overhead DB Extension", "Diamond Push-ups"],
        "correctif": ["Face Pull câble", "Reverse Fly haltères"]
    },
    "2. Dimanche: Repos Actif": {"main": ["Marche LISS (40 min)", "Mobilité Épaule"], "correctif": ["Protocole Épaule"]},
    "3. Lundi: Dos/Gainage (Callisthénie)": {
        "main": ["Hollow Body", "L-Sit Tuck", "Dead Hang", "Australian Pull-ups", "Tractions large", "Ab Wheel"],
        "correctif": ["Face Pull élastique"]
    },
    "4. Mardi: Jambes (Salle)": {
        "main": ["Leg Extension", "Leg Press", "Hack Squat", "Romanian Deadlift", "Leg Curl", "Bulgarian Split Squat", "Calf Raises"],
        "correctif": ["Mobilité Hanche"]
    },
    "5. Mercredi: Repos Actif": {"main": ["Marche LISS", "Mobilité"], "correctif": ["Protocole Épaule"]},
    "6. Jeudi: Épaules/Biceps (Salle)": {
        "main": ["Lateral Raise", "Seated DB Press (90°)", "Rear Delt Face Pull", "Cable Lateral Raise", "Barbell Curl", "Hammer Curl"],
        "correctif": ["Cuban Press", "Prone Y-T-W"]
    },
    "7. Vendredi: Full Body (Callisthénie)": {
        "main": ["Australian Pull-ups", "Dips", "Pike Push-up", "Pistol Squat assisté", "L-Sit", "Dragon Flag"],
        "correctif": ["Hollow Body"]
    }
}

def load_data(file): return pd.read_csv(file) if os.path.exists(file) else pd.DataFrame()
def save_entry(df, file):
    old = load_data(file)
    pd.concat([old, df], ignore_index=True).to_csv(file, index=False)

# --- UI ---
st.title("🚀 Hybrid Coach Pro")

tabs = st.tabs(["🏋️ Séance", "📏 Physique", "🥗 Nutrition", "📊 Evolution"])

# --- TAB 1: SÉANCE ---
with tabs[0]:
    jour = st.selectbox("Session", list(PROGRAMME.keys()))
    
    st.markdown(f"<div class='exercise-card'><b>Protocole Épaule Obligatoire</b><br>Dernière gêne notée : 🚨</div>", unsafe_allow_html=True)
    st.checkbox("Protocole terminé ✅")

    ex = st.selectbox("Exercice", PROGRAMME[jour]["main"])
    
    # Historique
    logs = load_data("workout_logs.csv")
    if not logs.empty:
        prev = logs[logs['Exercice'] == ex].tail(1)
        if not prev.empty:
            st.success(f"Dernière perf : {prev['Poids'].values[0]}kg x {prev['Reps'].values[0]} (RPE {prev['RPE'].values[0]})")

    with st.form("set_form"):
        c1, c2, c3 = st.columns(3)
        w = c1.number_input("Poids", step=0.5)
        r = c2.number_input("Reps", step=1)
        rpe = c3.selectbox("RPE", range(1,11), index=7)
        note = st.text_input("Note (Douleur ?)")
        if st.form_submit_button("VALIDER LA SÉRIE"):
            save_entry(pd.DataFrame([[date.today(), ex, w, r, rpe, note]], columns=["Date", "Exercice", "Poids", "Reps", "RPE", "Note"]), "workout_logs.csv")

# --- TAB 2: PHYSIQUE (COMPLET) ---
with tabs[1]:
    st.header("Suivi Anthropométrique")
    
    # Upload Photo
    st.subheader("📸 Photos de progression")
    img = st.file_uploader("Prendre/Choisir une photo", type=['jpg', 'jpeg', 'png'])
    if img: st.image(img, use_container_width=True)

    with st.form("body_full"):
        c1, c2 = st.columns(2)
        poids = c1.number_input("Poids (kg)", value=116.0)
        taille = c2.number_input("Taille/Nombril (cm)")
        cou = c1.number_input("Cou (cm)")
        poitrine = c2.number_input("Poitrine (cm)")
        epaules = c1.number_input("Épaules (cm)")
        bras = c2.number_input("Bras (cm)")
        hanches = c1.number_input("Hanches (cm)")
        cuisse = c2.number_input("Cuisse (cm)")
        
        if st.form_submit_button("ENREGISTRER TOUTES LES MESURES"):
            data_body = pd.DataFrame([[date.today(), poids, taille, cou, poitrine, epaules, bras, hanches, cuisse]], 
                                    columns=["Date", "Poids", "Taille", "Cou", "Poitrine", "Epaules", "Bras", "Hanches", "Cuisse"])
            save_entry(data_body, "metrics.csv")
            st.balloons()

# --- TAB 3: NUTRITION ---
with tabs[2]:
    st.header("Plan 2500-2800 kcal")
    for r in ["Repas 1 (Pré)", "Repas 2 (Post)", "Repas 3 (Midi)", "Repas 4 (Collation)", "Repas 5 (Dîner)", "Caséine Dodo"]:
        st.checkbox(r)
