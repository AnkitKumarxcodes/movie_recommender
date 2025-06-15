import pandas as pd
import streamlit as st
import pickle
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')

print(api_key)

st.title('Movie Recommendation System')
st.text('Get ur movie here')

df = pd.read_csv('processed_data.csv')
print(df.columns)

similarity = pickle.load(open('similarity.pkl' , 'rb'))

def fetch_posters(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id,api_key)
    response =requests.get(url)
    data = response.json()
    # st.text(data)
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse = True ,key = lambda x:x[1])[1:6]

    recommended_movies = []
    movie_posters = []

    for i in movies_list:
        movie_id = df.iloc[i[0]].movie_id
        recommended_movies.append(df.iloc[i[0]].title)
        movie_posters.append(fetch_posters(movie_id))
    return recommended_movies,movie_posters
        # print(i[0])
    

selected_movie = st.selectbox('Select Your Movie', df['title'].values)

if st.button('Recommmend'):
    recommendations,posters = recommend(selected_movie)
    col1,col2,col3,col4,col5 = st.columns(5)
    cols = [col1,col2,col3,col4,col5]
    for i in range(5):
        with cols[i]:
            st.markdown(f"<h5 style='text-align: center;'>{recommendations[i]}</h5>", unsafe_allow_html=True)
            st.image(posters[i])
