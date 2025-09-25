import streamlit as st
import pickle
import requests

movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1MjkwOWMxOGJjYzJjN2UyNWJkMmM5NTRiZDQ3MjY4OSIsIm5iZiI6MTc1NzYwNjY2My40MzI5OTk4LCJzdWIiOiI2OGMyZjMwNzZlYmU5OGM3MWU0ZTc0MTMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.k07o6if3zAjGRycebhSpTnRw8Po5jlaEjYbX9BRhBTY"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500{}".format(data['poster_path'])


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_distance = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended = []
    for i in movies_distance:
        movie_id = movies_list.iloc[i[0]].movie_id
        title = movies_list.iloc[i[0]].title
        recommended.append((title, movie_id))
    return recommended


# set the title
st.title("Movie Recommender System")
movies_title = movies_list['title'].values
selected_movie_name = st.selectbox(
    'Select a movie to show Recommended Movies ',
    movies_title)

if st.button('Recommend'):
    recommended_movies = recommend(selected_movie_name)
    cols = st.columns(len(recommended_movies))
    st.write(" Recommended Movies:")
    for idx, (title, movie_id) in enumerate(recommended_movies):
        with cols[idx]:
            st.image(fetch_poster(movie_id), use_container_width=True)
            st.write(title)