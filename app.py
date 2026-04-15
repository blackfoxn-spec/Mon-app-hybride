
import streamlit as st
import pandas as pd
from datetime import date
import os

# Configuration de la page
st.set_page_config(page_title="Hybrid Coach 40", page_icon="🦾")

# --- CATALOGUE DU PROGRAMME PERSO ---
PROGRAMME = {
    "Lundi: Poitrine/Triceps": [
        "Incline Machine Press (Amplitude 90°)", "Cable Crossover bas -> haut", 
        "Flat Dumbbell Press (Partiel)", "Cable Crossover horizontal", 
        "Dips lestés (Max 90°)", "Rope Pushdown", "Overhead DB Extension", "Diamond Push-ups"
    ],
    "Mardi: Dos/Gainage": [
        "Hollow Body Hold", "L-Sit Tuck", "Dead Hang actif", 
        "Australian Pull-ups", "Tractions prise large", "Tractions supination", 
        "Straight Arm Pulldown", "Ab Wheel Rollout", "Dragon Flag Tuck"
    ],
    "Mercredi: Jambes": [
        "Leg Extension", "Leg Press Prise Large", "Hack Squat", 
        "Smith Machine Squat", "Romanian Deadlift", "Leg Curl Couché", 
        "Bulgarian Split Squat assisté", "Calf Raises"
    ],
    "Vendredi: Épaules/Biceps": [
        "Lateral Raise (Poids réduit)", "Seated DB Press (Partiel)", 
        "Rear Delt Face Pull", "Cable Lateral Raise", "Barbell Curl", 
        "Hammer Curl", "Concentration Curl"
    ],
    "Samedi: Full Body": [
        "Australian Pull-ups", "Dips parallèles", "Pike Push-up mural", 
        "Pistol Squat assisté", "L-Sit Tuck", "Dragon Flag Tuck"
    ]
}

# --- FONCTIONS DE SAUVEGARDE ---
def save_entry(df, file):
    if os.path.exists(file):
        old = pd.read_csv(file)
        df = pd.concat([old, df], ignore_index=True)
    df.to_csv(file, index=False)

# --- INTERFACE ---
st.title("🦾 My Hybrid Coach")

menu = ["🏋️ Ma Séance", "📏 Check-in Physique", "🚨 Récup Épaule", "📊 Mes Stats"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "🏋️ Ma Séance":
    st.info("💡 Règle d'or : Chaque kilo perdu = +1 rep en callisthénie[cite: 4, 5].")
    jour_actuel = st.selectbox("Quelle session ?", list(PROGRAMME.keys()))
    
    with st.form("set_log", clear_on_submit=True):
        exercice = st.selectbox("Exercice", PROGRAMME[jour_actuel])
        col1, col2 = st.columns(2)
        weight = col1.number_input("Charge (kg)", step=0.5)
        reps = col2.number_input("Reps", step=1)
        note = st.text_input("Gêne épaule ? (0 à 10)")
        
        if st.form_submit_button("Enregistrer la série"):
            new_row = pd.DataFrame([[date.today(), jour_actuel, exercice, weight, reps, note]], 
                                   columns=["Date", "Seance", "Exercice", "Poids", "Reps", "Note"])
            save_entry(new_row, "workout_logs.csv")
            st.success(f"Série validée !")

elif choice == "📏 Check-in Physique":
    st.header("Suivi Mensurations")
    with st.form("body"):
        poids = st.number_input("Poids (kg)", value=116.0, step=0.1)
        taille = st.number_input("Tour de taille (cm)", step=0.5)
        if st.form_submit_button("Sauvegarder"):
            save_entry(pd.DataFrame([[date.today(), poids, taille]], columns=["Date", "Poids", "Taille"]), "metrics.csv")
            st.success(f"Données enregistrées. Objectif : 95 kg[cite: 3].")

elif choice == "🚨 Récup Épaule":
    st.header("Protocole Correctif Obligatoire")
    st.warning("À faire AVANT chaque séance impliquant les épaules[cite: 10].")
    st.write("- **Band Pull-Apart** (3 x 20) [cite: 14]")
    st.write("- **Face Pull élastique** (3 x 15-20) [cite: 14]")
    st.write("- **Rotation externe élastique** (3 x 15/côté) [cite: 14]")
    st.write("- **Wall Slide** (2 x 12) [cite: 14]")
    st.checkbox("Protocole terminé")

elif choice == "📊 Mes Stats":
    st.header("Évolution")
    if os.path.exists("workout_logs.csv"):
        data = pd.read_csv("workout_logs.csv")
        st.line_chart(data.groupby("Date")["Poids"].max())
    else:
        st.write("Aucune donnée pour le moment.")
