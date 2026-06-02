import streamlit as st
import pickle
import pandas as pd
import requests

# Fetch poster from TMDB
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=5a4fbeca573e3bad9a257c6d55814c5b'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # ✅ FIXED
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# Load Data
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a Movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)