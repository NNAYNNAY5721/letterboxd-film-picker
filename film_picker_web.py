import random
import streamlit as st
import pandas as pd
import urllib.parse

# --- Configuration de la page ---
st.set_page_config(page_title="Nouka Pictures", layout="centered")

# --- CSS pour style cinématographique ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap');

body {
    background-color: #121212;
    color: #ffffff;
}

h1 {
    font-family: 'Cinzel', serif;
    color: gold;
    text-align: center;
    font-size: 60px;
    margin-bottom: 20px;
}

h2 {
    font-family: 'Cinzel', serif;
    color: #ffffff;
    background-color: #222831;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

button {
    font-family: 'Cinzel', serif;
    cursor: pointer;
    transition: 0.3s;
}

button:hover {
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# --- Titre ---
st.markdown("<h1>🎬 Nouka Pictures</h1>", unsafe_allow_html=True)

# --- Import CSV Letterboxd ---
st.markdown("### 📂 Importer votre fichier CSV Letterboxd")
uploaded_file = st.file_uploader("Choisissez un fichier CSV exporté depuis Letterboxd", type="csv")

films = []

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')

        # --- Détecter les colonnes ---
        col_map = {}
        for col in df.columns:
            c = col.lower()
            if 'title' in c or 'name' in c:
                col_map['title'] = col
            elif 'year' in c:
                col_map['year'] = col
            elif 'url' in c or 'letterboxd' in c:
                col_map['url'] = col

        if 'title' in col_map and 'year' in col_map and 'url' in col_map:
            for _, row in df.iterrows():
                films.append({
                    "title": row[col_map['title']],
                    "year": row[col_map['year']],
                    "url": row[col_map['url']]
                })
            st.success(f"✅ {len(films)} films chargés depuis le CSV Letterboxd !")
        else:
            st.error(f"Impossible de détecter Title, Year et URL automatiquement.\nColonnes détectées : {list(df.columns)}")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du CSV : {e}")

# --- Tirer un film aléatoire ---
if st.button("🎥 Nouveau film"):
    if not films:
        st.warning("Aucun film disponible. Importez un CSV.")
    else:
        film = random.choice(films)
        st.markdown(
            f"<h2>{film['title']} ({film['year']})</h2>",
            unsafe_allow_html=True
        )

        # --- Lien JustWatch ---
        query = urllib.parse.quote(film['title'])
        justwatch_url = f"https://www.justwatch.com/fr/recherche?q={query}"

        st.markdown(
            f"<div style='text-align:center; margin-top:20px;'>"
            f"<a href='{film['url']}' target='_blank'>"
            f"<button style='background-color:#FFB700; color:black; padding:12px 25px; border:none; border-radius:8px; font-size:18px; margin-right:15px;'>Voir sur Letterboxd</button>"
            f"</a>"
            f"<a href='{justwatch_url}' target='_blank'>"
            f"<button style='background-color:#00ADB5; color:white; padding:12px 25px; border:none; border-radius:8px; font-size:18px;'>Voir sur JustWatch</button>"
            f"</a></div>",
            unsafe_allow_html=True
        )
