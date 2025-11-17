import random
import streamlit as st
import pandas as pd
import urllib.parse
import time

# --- Configuration page ---
st.set_page_config(page_title="Nouka Pictures", layout="wide")

# --- CSS global ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@700&family=Roboto:wght@500&display=swap');

body {
    background-color: #121212;
    color: #ffffff;
}

h1 {
    font-family: 'Raleway', sans-serif;
    font-weight: 800;
    font-size: 72px;
    text-align: center;
    background: linear-gradient(90deg, #FFD700, #FFFACD);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 1px 1px 5px rgba(0,0,0,0.5);
    margin-bottom: 40px;
}

h2 {
    font-family: 'Raleway', sans-serif;
    color: #ffffff;
    text-align: center;
    margin: 30px 0;
    font-size: 40px;
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(-20px);}
    to {opacity: 1; transform: translateY(0);}
}

button {
    font-family: 'Roboto', sans-serif;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    border-radius: 12px;
    font-size: 18px;
    padding: 15px 35px;
    margin: 10px;
    color: white;
    box-shadow: 0 0 5px #000000;
}

button:hover {
    transform: scale(1.1);
    box-shadow: 0 0 15px #ffffff;
    opacity: 0.95;
}

.button-letterboxd {
    background: linear-gradient(45deg, #FFB700, #FF6F00);
    color: black;
}

.button-justwatch {
    background: linear-gradient(45deg, #00ADB5, #007B7F);
    color: white;
}

.button-instagram {
    background-color: #AAAAAA;
    color: #121212;
    padding: 8px 20px;
    font-size: 14px;
    border-radius: 8px;
    box-shadow: none;
}

.button-instagram:hover {
    transform: scale(1.05);
    box-shadow: 0 0 5px #ffffff;
}

/* Roulette */
.roulette-container {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
    flex-wrap: wrap;
}
.roulette-item {
    width: 220px;
    padding: 15px;
    border-radius: 12px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 6px 15px rgba(0,0,0,0.3);
    text-align: center;
    transition: 0.2s;
}

.footer {
    text-align: center;
    margin-top: 50px;
    font-family: 'Roboto', sans-serif;
    color: #AAAAAA;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# --- Titre ---
st.markdown("<h1>Nouka Pictures</h1>", unsafe_allow_html=True)

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

# --- Tirage roulette ---
def run_roulette(films_list, spins=25):
    placeholder = st.empty()
    n = len(films_list)
    final_film = random.choice(films_list)

    for i in range(spins):
        display_films = random.sample(films_list, min(3, n))
        html_items = "".join([f"<div class='roulette-item'><h3>{f['title']}</h3></div>" for f in display_films])
        placeholder.markdown(f"<div class='roulette-container'>{html_items}</div>", unsafe_allow_html=True)
        t = i / spins
        time.sleep(0.02 + t**2 * 0.08)

    # Affichage final
    placeholder.empty()
    st.markdown(f"<h2>{final_film['title']} ({final_film['year']})</h2>", unsafe_allow_html=True)
    query = urllib.parse.quote(final_film['title'])
    justwatch_url = f"https://www.justwatch.com/fr/recherche?q={query}"
    st.markdown(
        f"<div style='text-align:center;'>"
        f"<a href='{final_film['url']}' target='_blank'><button class='button-letterboxd'>Letterboxd</button></a>"
        f"<a href='{justwatch_url}' target='_blank'><button class='button-justwatch'>JustWatch</button></a>"
        f"</div>",
        unsafe_allow_html=True
    )

# --- Bouton roulette ---
if st.button("🎰 Lancer la Roulette"):
    if not films:
        st.warning("Aucun film disponible. Importez un CSV.")
    else:
        run_roulette(films)

# --- Footer avec pseudo créateur et bouton Instagram minimaliste ---
st.markdown(
    "<div class='footer'>Créé par NNAY<br>"
    "<a href='https://www.instagram.com/watch_me_nnay/' target='_blank'>"
    "<button class='button-instagram'>Instagram</button></a></div>",
    unsafe_allow_html=True
)
