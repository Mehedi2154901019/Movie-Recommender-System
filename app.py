import streamlit as st
import pickle
import pandas as pd
import requests

# --- TMDB API fetch ---
def api_fetch(movie_id):
    api_key = '40d02bd045476e03db301888469c1ff6'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return 'http://image.tmdb.org/t/p/w500' + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# --- Recommendation Function ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:50]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(api_fetch(movie_id))
    return recommended_movies, recommended_movies_posters

# --- Load Pickled Data ---
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Page Config ---
st.set_page_config(layout="wide")

# --- Custom CSS Styling ---
st.markdown(
    """
    <style>
    body {
        background-image: url('https://images.pexels.com/photos/952670/pexels-photo-952670.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }
    .stApp {
        background: rgba(0, 0, 0,0.8);
        padding: 2rem;
        border-radius: 10px;
    }
    .poster:hover {
        transform: scale(1.05);
        transition: transform 0.3s ease;
        box-shadow: 0 8px 20px rgba(255, 255, 255, 0.4);
    }
    .centered-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 5px;
    }
    .custom-selectbox {
        width: 50%;
        margin-bottom: 10px;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title ---
st.title('🎬 Movie Recommender System')

# --- Centered Search Box & Button ---
st.markdown('<div class="centered-box">', unsafe_allow_html=True)
selected_movie_name = st.selectbox(
    'Choose a movie you like:',
    movies['title'].values,
    key='movie_select',
    label_visibility='collapsed'
)
st.markdown('<style>div[data-baseweb="select"] { width: 50% !important; align-items: center }</style>', unsafe_allow_html=True)
recommend_clicked = st.button('Recommend')
st.markdown('</div>', unsafe_allow_html=True)

# --- Recommend Logic ---
if recommend_clicked:
    with st.spinner('Loading your recommendations...'):
        names, posters = recommend(selected_movie_name)

    # Display in 7 columns per row
    for row in range((len(names) + 6) // 7):
        cols = st.columns(7)
        for i in range(7):
            idx = row * 7 + i
            if idx < len(names):
                with cols[i]:
                    st.markdown(
                        f"""
                        <div style="text-align: center;">
                            <img class="poster" src="{posters[idx]}" 
                                 style="width: 100%; height: auto; border-radius: 10px; 
                                        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4); margin-bottom: 5px;">
                            <p style="font-weight: bold; font-size: 15px; color: white; word-wrap: break-word; margin: 0;">
                                {names[idx]}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
