import random
import streamlit as st
import pandas as pd
import urllib.parse

# --- Configuration de la page ---
st.set_page_config(page_title="Nouka Pictures", layout="centered")

# --- CSS minimaliste ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Roboto:wght@500&display=swap');

body {
    background-color: #f9f9f9;
    color: #222831;
}

h1 {
    font-family: 'Cinzel', serif;
    color: gold;
    text-align: center;
    font-size: 50px;
    margin-bottom: 30px;
}

h2 {
    font-family: 'Cinzel', serif;
    color: #222831;
    text-align: center;
    margin: 20px 0;
}

button {
    font-family: 'Roboto', sans-serif;
    cursor: pointer;
    padding: 12px 25px;
    border-radius: 6px;
    border: none;
    font-size: 16px;
    margin: 5px;
    transition: 0.2s;
}

button:hover {
    opacity: 0.85;
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

        # --- Colonnes ---
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

# --- Tirage aléatoire ---
if st.button("🎥 Nouveau film"):
    if not films:
        st.warning("Aucun film disponible. Importez un CSV.")
    else:
        film = random.choice(films)
        st.markdown(f"<h2>{film['title']} ({film['year']})</h2>", unsafe_allow_html=True)

        # Lien JustWatch
        query = urllib.parse.quote(film['title'])
        justwatch_url = f"https://www.justwatch.com/fr/recherche?q={query}"

        st.markdown(
            f"<div style='text-align:center;'>"
            f"<a href='{film['url']}' target='_blank'><button style='background-color:#FFD700; color:black;'>Letterboxd</button></a>"
            f"<a href='{justwatch_url}' target='_blank'><button style='background-color:#00ADB5; color:white;'>JustWatch</button></a>"
            f"</div>",
            unsafe_allow_html=True
        )
