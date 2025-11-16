import random
import streamlit as st
import pandas as pd

# --- Configuration de la page ---
st.set_page_config(page_title="Nouka Pictures", layout="centered")

# --- Titre ---
st.markdown("<h1 style='text-align:center; color:#00ADB5;'>🎬 Nouka Pictures</h1>", unsafe_allow_html=True)

# --- Import CSV Letterboxd ---
st.markdown("### 📂 Importer votre fichier CSV Letterboxd")
uploaded_file = st.file_uploader("Choisissez un fichier CSV exporté depuis Letterboxd", type="csv")

films = []

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        
        # --- Détecter automatiquement les colonnes ---
        col_map = {}
        for col in df.columns:
            c = col.lower()
            if 'title' in c or 'name' in c:
                col_map['title'] = col
            elif 'year' in c:
                col_map['year'] = col
            elif 'url' in c or 'letterboxd' in c:
                col_map['url'] = col
        
        if len(col_map) == 3:
            for _, row in df.iterrows():
                films.append({
                    "title": row[col_map['title']],
                    "year": row[col_map['year']],
                    "url": row[col_map['url']]
                })
            st.success(f"✅ {len(films)} films chargés depuis le CSV Letterboxd !")
        else:
            st.error(f"Impossible de détecter automatiquement Title, Year et URL.\nColonnes détectées : {list(df.columns)}")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du CSV : {e}")

# --- Tirer un film aléatoire ---
if st.button("🎥 Nouveau film"):
    if not films:
        st.warning("Aucun film disponible. Importez un CSV.")
    else:
        film = random.choice(films)
        st.markdown(
            f"<h2 style='text-align:center; color:#222831; background-color:#00ADB5; padding:10px; border-radius:10px;'>"
            f"{film['title']} ({film['year']})</h2>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='text-align:center; margin-top:10px;'>"
            f"<a href='{film['url']}' target='_blank'>"
            f"<button style='background-color:#FF5722; color:white; padding:10px 20px; border:none; border-radius:5px; font-size:16px;'>Voir sur Letterboxd</button>"
            f"</a></div>",
            unsafe_allow_html=True
        )
