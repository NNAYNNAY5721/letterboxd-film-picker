import random
import streamlit as st
import pandas as pd
import urllib.parse

# --- Configuration de la page ---
st.set_page_config(page_title="Nouka Pictures", layout="wide")

# --- CSS pour style cinéma premium ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap');

body {
    background-image: url('https://images.unsplash.com/photo-1517602302552-471fe67acf66?auto=format&fit=crop&w=1740&q=80');
    background-size: cover;
    background-attachment: fixed;
    color: #ffffff;
}

h1 {
    font-family: 'Cinzel', serif;
    color: gold;
    text-align: center;
    font-size: 70px;
    margin-bottom: 40px;
    text-shadow: 2px 2px 5px #000000;
}

h2 {
    font-family: 'Cinzel', serif;
    color: #ffffff;
    background-color: rgba(34, 40, 49, 0.85);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 5px 5px 15px #000000;
}

button {
    font-family: 'Cinzel', serif;
    cursor: pointer;
    transition: all 0.3s ease;
}

button:hover {
    transform: scale(1.1);
    opacity: 0.9;
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
            f"<div style='text-align:center; margin-top:25px;'>"
            f"<a href='{film['url']}' target='_blank'>"
            f"<button style='background-color:#FFB700; color:black; padding:15px 30px; border:none; border-radius:10px; font-size:18px; margin-right:15px;'>Voir sur Letterboxd</button>"
            f"</a>"
            f"<a href='{justwatch_url}' target='_blank'>"
            f"<button style='background-color:#00ADB5; color:white; padding:15px 30px; border:none; border-radius:10px; font-size:18px;'>Voir sur JustWatch</button>"
            f"</a></div>",
            unsafe_allow_html=True
        )
