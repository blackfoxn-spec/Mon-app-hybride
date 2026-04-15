import streamlit as st
import pandas as pd
from datetime import date
import os

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="Hybrid Coach Premium", page_icon="🦾", layout="centered")

st.markdown("""
    <style>
    /* Fond sombre propre */
    .main { background-color: #0e1117; color: #ffffff; }
    
    /* Carte Protocole - Texte Blanc Obligatoire */
    .protocol-card {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 12px;
        border-left: 6px solid #ff4b4b;
        margin-bottom: 20px;
        color: white !important;
    }
    
    /* Bouton de validation massif et bleu */
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        height: 4em; 
        background-color: #007bff !important; 
        color: white !important; 
        font-size: 18px !important;
        font-weight: bold !important;
        border: none;
    }

    /* Input fields plus contrastés */
    input { background-color: #262730 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- STRUCTURE PROGRAMME ---
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
    
    # Correction visuelle ici
    st.markdown(f"""
    <div class='protocol-card'>
        <h3 style='color: white; margin-top:0;'>🚨 Protocole Épaule Obligatoire</h3>
        [span_0](start_span)<p style='color: #ff4b4b; font-weight: bold;'>Ne pas zapper : Band Pull-Apart & Rotations[span_0](end_span)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.checkbox("Protocole terminé ✅")

    ex = st.selectbox("Exercice", PROGRAMME[jour]["main"])
    
    # Rappel Record
    logs = load_data("workout_logs.csv")
    if not logs.empty:
        prev = logs[logs['Exercice'] == ex].tail(1)
        if not prev.empty:
            st.info(f"💪 Dernier record : {prev['Poids'].values[0]}kg x {prev['Reps'].values[0]}")

    with st.form("set_form"):
        c1, c2 = st.columns(2)
        w = c1.number_input("Poids (kg)", step=0.5)
        r = c2.number_input("Reps", step=1)
        rpe = st.select_slider("RPE (Intensité)", options=range(1,11), value=8)
        note = st.text_input("Gêne épaule ? (0-10)")
        if st.form_submit_button("VALIDER LA SÉRIE"):
            save_entry(pd.DataFrame([[date.today(), ex, w, r, rpe, note]], columns=["Date", "Exercice", "Poids", "Reps", "RPE", "Note"]), "workout_logs.csv")
            st.success("Série enregistrée !")

# --- TAB 2: PHYSIQUE ---
with tabs[1]:
    st.header("Check-in Anthropométrique")
    
    img = st.file_uploader("📸 Ajouter une photo de progression", type=['jpg', 'jpeg', 'png'])
    if img: st.image(img)

    with st.form("body_metrics"):
        c1, c2 = st.columns(2)
        poids = c1.number_input("Poids (kg)", value=116.0)
        taille = c2.number_input("Taille/Nombril (cm)")
        cou = c1.number_input("Cou (cm)")
        poitrine = c2.number_input("Poitrine (cm)")
        epaules = c1.number_input("Épaules (cm)")
        bras = c2.number_input("Bras (cm)")
        hanches = c1.number_input("Hanches (cm)")
        cuisse = c2.number_input("Cuisse (cm)")
        
        if st.form_submit_button("SAUVEGARDER TOUTES LES MESURES"):
            data_body = pd.DataFrame([[date.today(), poids, taille, cou, poitrine, epaules, bras, hanches, cuisse]], 
                                    columns=["Date", "Poids", "Taille", "Cou", "Poitrine", "Epaules", "Bras", "Hanches", "Cuisse"])
            save_entry(data_body, "metrics.csv")
            st.balloons()
