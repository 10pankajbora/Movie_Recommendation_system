import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=79f02bad41ed9815f92e5a68daf1a3d1&language=en-US")
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']

    except:
        return "https://via.placeholder.com/500x750.png?text=No+Image"


def recommend(movie):
    """
    This function grabs a element(movie) from user and uses the element to provide its similarity
    with the element from the list and gives the top 5 movies similar to it
    """
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # "fetch poster from api"
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


# We loaded the movie dictionary and made a movies dataframe having list of movies
movies_list = pickle.load(open("movies_dict.pkl", 'rb'))

movies = pd.DataFrame(movies_list)

# We have loaded the similarity from the code in VSCOde movie_recommend file
import lzma

with lzma.open('Similarity.xz', 'rb') as f:
    similarity = pickle.load(f)

# Below is the command to show a title in my web page
st.title("Movie Recommender System")

# Below command will show an option bar to select a movie from a list
selected_movie_name = st.selectbox(
    "How would you like to be recommended?", movies['title'].values
)

# Condition receiving data from above selected option and recommends movie as option provided
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

# API key: 79f02bad41ed9815f92e5a68daf1a3d1
