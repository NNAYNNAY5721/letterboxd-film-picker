import random
import streamlit as st
import pandas as pd
import urllib.parse
import requests

# --- Configuration de la page ---
st.set_page_config(page_title="Nouka Pictures", layout="wide")

# --- CSS cinéma stylé ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Roboto:wght@500&display=swap');

body {
    background-color: #121212;
    color: #ffffff;
}

h1 {
    font-family: 'Cinzel', serif;
    color: gold;
    text-align: center;
    font-size: 70px;
    margin-bottom: 30px;
    text-shadow: 2px 2px 5px #000000;
}

h2 {
    font-family: 'Cinzel', serif;
    color: #ffffff;
    text-align: center;
    margin: 20px 0;
}

button {
    font-family: 'Roboto', sans-serif;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    border-radius: 12px;
    font-size: 18px;
    padding: 15px 30px;
    margin: 10px;
}

button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 10px #ffffff;
    opacity: 0.95;
}

.button-letterboxd {
    background-color: #FFB700;
    color: black;
}

.button-justwatch {
    background-color: #00ADB5;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- Titre ---
st.markdown("<h1>🎬 Nouka Pictures</h1>", unsafe_allow_html=True)

# --- Import CSV Letterboxd ---
uploaded_file = st.file_uploader("Importer votre CSV Letterboxd", type="csv")

films = []

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
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
            st.success(f"{len(films)} films chargés ✅")
        else:
            st.error("Impossible de détecter Title, Year et URL.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du CSV : {e}")

# --- Fonction pour récupérer l'affiche via TMDb ---
def get_tmdb_poster(title, year):
    api_key = "VOTRE_API_KEY_TMDb"  # <-- Remplace par ta clé TMDb
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={urllib.parse.quote(title)}&year={year}&language=fr"
    res = requests.get(url).json()
    if res.get('results'):
        poster_path = res['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# --- Tirage aléatoire ---
if st.button("🎥 Nouveau film"):
    if not films:
        st.warning("Aucun film disponible. Importez un CSV.")
    else:
        film = random.choice(films)
        st.markdown(f"<h2>{film['title']} ({film['year']})</h2>", unsafe_allow_html=True)

        # --- Affiche via TMDb ---
        poster_url = get_tmdb_poster(film['title'], film['year'])
        if poster_url:
            st.image(poster_url, use_column_width=True)
        else:
            st.warning("Affiche non disponible.")

        # --- Lien JustWatch ---
        query = urllib.parse.quote(film['title'])
        justwatch_url = f"https://www.justwatch.com/fr/recherche?q={query}"

        st.markdown(
            f"<div style='text-align:center;'>"
            f"<a href='{film['url']}' target='_blank'><button class='button-letterboxd'>Letterboxd</button></a>"
            f"<a href='{justwatch_url}' target='_blank'><button class='button-justwatch'>JustWatch</button></a>"
            f"</div>",
            unsafe_allow_html=True
        )
