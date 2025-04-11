import streamlit as st
import numpy as np
from operator import itemgetter
# from PIL import Image
import json
from bs4 import BeautifulSoup
import requests
import io
import PIL.Image
import base64
from urllib.request import urlopen

with open('movie_data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open('movie_titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)
hdr = {'User-Agent': 'Mozilla/5.0'}
#


class KNearestNeighbours:
    def __init__(self, data, target, test_point, k):
        self.data = data
        self.target = target
        self.test_point = test_point
        self.k = k
        self.distances = list()
        self.categories = list()
        self.indices = list()
        self.counts = list()
        self.category_assigned = None

    @staticmethod
    def dist(p1, p2):
        """Method returns the euclidean distance between two points"""
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def fit(self):
        """Method that performs the KNN classification"""
        # Create a list of (distance, index) tuples from the test point to each point in the data
        self.distances.extend([(self.dist(self.test_point, point), i) for point, i in zip(
            self.data, [i for i in range(len(self.data))])])
        # Sort the distances in ascending order
        sorted_li = sorted(self.distances, key=itemgetter(0))
        # Fetch the indices of the k nearest point from the data
        self.indices.extend([index for (val, index) in sorted_li[:self.k]])
        # Fetch the categories from the train data target
        for i in self.indices:
            self.categories.append(self.target[i])
        # Fetch the count for each category from the K nearest neighbours
        self.counts.extend([(i, self.categories.count(i))
                           for i in set(self.categories)])
        # Find the highest repeated category among the K nearest neighbours
        self.category_assigned = sorted(
            self.counts, key=itemgetter(1), reverse=True)[0][0]


def movie_poster_fetcher(imdb_link):
    # st.markdown(
    #     f"""
    #      <style>
    #      .stApp {{
    #          background-image: url("https://img.freepik.com/free-vector/podium-illuminated-by-red-spotlights-empty-platform-stage-with-beams-lamps-spots-light-floor-realistic-interior-dark-hall-corridor-with-projectors-rays-smoke_107791-4352.jpg?w=1060&t=st=1688464333~exp=1688464933~hmac=8b1cdcedc88cbce339d74dff7ef9e1b762ade75d07c606fd69f1b94658ba5373");
    #          background-attachment: fixed;
    #          background-size: cover
    #      }}
    #      </style>
    #      """,
    #     unsafe_allow_html=True)
    
    with open('pic1.jpg', "rb") as image_file:        
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
     
    # Display Movie Poster
    url_data = requests.get(imdb_link, headers=hdr).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    imdb_dp = s_data.find("meta", property="og:image")
    # st.success(imdb_link)
    movie_poster_link = imdb_dp.attrs['content']
    # movie_poster_link = imdb_dp.attrs['content']
    u = urlopen(movie_poster_link)
    raw_data = u.read()
    image = PIL.Image.open(io.BytesIO(raw_data))
    image = image.resize((700, 401), )
    st.image(image, use_column_width=False)


# def get_movie_info(imdb_link):
#     url_data = requests.get(imdb_link, headers=hdr).text
#     s_data = BeautifulSoup(url_data, 'html.parser')
#     imdb_content = s_data.find("meta", property="og:description")
#     movie_descr = imdb_content.attrs['content']
#     movie_descr = str(movie_descr).split('.')
#     movie_director = movie_descr[0]
#     movie_cast = str(movie_descr[1]).replace('With', 'Cast: ').strip()
#     movie_story = 'Story: ' + str(movie_descr[2]).strip() + '.'
#     rating = s_data.find("span", class_="sc-bde20123-1 iZlgcd").text
#     movie_rating = 'Total Rating count: ' + str(rating)
#     return movie_director, movie_cast, movie_story, movie_rating


# def get_movie_info(imdb_link):
#     url_data = requests.get(imdb_link, headers=hdr).text
#     s_data = BeautifulSoup(url_data, 'html.parser')
#     imdb_content = s_data.find("meta", property="og:description")
#     movie_descr = imdb_content.attrs['content']
#     movie_descr = str(movie_descr).split('.')
#     movie_director = movie_descr[0]
#     movie_cast = str(movie_descr[1]).replace('With', 'Cast: ').strip()
#     movie_story = 'Story: ' + str(movie_descr[2]).strip() + '.'
#     rating = s_data.find("span", class_="sc-bde20123-1 iZlgcd").text
#     movie_rating = 'Total Rating count: ' + str(rating)
#     return movie_director, movie_cast, movie_story, movie_rating

def get_movie_info(imdb_link):
    url_data = requests.get(imdb_link, headers=hdr).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    # imdb_content = s_data.find("meta", property="og:description")
    imdb_content = s_data.find("meta",{"name" : "description"})    
    movie_descr = imdb_content.attrs['content']
    movie_descr = str(movie_descr).split('.')

    movie_director = movie_descr[0]

    if len(movie_descr) > 1:
        movie_cast = str(movie_descr[1]).replace('With', 'Cast: ').strip()
    else:
        movie_cast = "Site Updated Data , So web scraption description Changed  : : No cast information available."

    if len(movie_descr) > 2:
        movie_story = 'Story: ' + str(movie_descr[2]).strip() + '.'
    else:
        movie_story = "Site Updated Data , So web scraption description Changed  : : No story information available."

    rating = s_data.find("span", class_="sc-bde20123-1 iZlgcd").text
    movie_rating = 'Total Rating count: ' + str(rating)

    return movie_director, movie_cast, movie_story, movie_rating



def KNN_Movie_Recommender(test_point, k):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # model = __init__(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Print list of 10 recommendations < Change value of k for a different number >
    table = []
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2], data[i][-1]])
    print(table)
    return table


st.set_page_config(
    page_title="Movie Recommender System",
)


def run():    
    # st.markdown(
    #     f"""
    #      <style>
    #      .stApp {{
    #          background-image: url("https://img.freepik.com/free-vector/red-spotlight-background_1035-9217.jpg?5&w=740&t=st=1688459256~exp=1688459856~hmac=dfd15945311c08d6ea3d385676b9e5786ebd80e3003d0e60a07ec9fe370cdf88");
    #          background-attachment: fixed;
    #          background-size: cover
    #      }}
    #      </style>
    #      """,
        # unsafe_allow_html=True)
        
    with open('pic2.jpg', "rb") as image_file:        
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )


    st.title("**:red[Movie Magic - Your Ultimate Movie Recommendation App!]**")
    st.markdown('''<h4 style='text-align: left; color: #FFCCCB;'>* Data is based "IMDB 5000 Movie Dataset"</h4>''',
                unsafe_allow_html=True)
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    movies = [title[0] for title in movie_titles]
    category = ['--Select--', 'Movie based', 'Genre based']
    cat_op = st.selectbox('**Select Recommendation Type**', category)
    if cat_op == category[0]:
        st.warning('Please select Recommendation Type!!')
    elif cat_op == category[1]:
        select_movie = st.selectbox('**Select movie: (Recommendation will be based on this selection)**',
                                    ['--Select--'] + movies)
        if (select_movie != '--Select--'):
            dec = st.radio("**Want to Fetch Movie Poster?**", ('Yes', 'No'))
            st.markdown(
                '''<h4 style='text-align: left; color: #d73b5c;'>* Fetching a Movie Posters will take time."</h4>''',
                unsafe_allow_html=True)
            if dec == 'No':
                if select_movie == '--Select--':
                    st.warning('Please select Movie!!')
                else:
                    no_of_reco = st.slider(
                        '**Number of movies you want Recommended**:', min_value=5, max_value=50, step=1)
                    if st.button('Result'):
                        genres = data[movies.index(select_movie)]
                        test_points = genres
                        table = KNN_Movie_Recommender(
                            test_points, no_of_reco + 1)
                        table.pop(0)
                        c = 0
                        st.success(
                            '**Some of the movies from our Recommendation, have a look below**')
                        for movie, link, ratings in table:
                            c += 1
                            director, cast, story, total_rat = get_movie_info(
                                link)
                            st.markdown(f"({c})[ {movie}]({link})")
                            st.markdown(director)
                            st.markdown(cast)
                            st.markdown(story)
                            st.markdown(total_rat)
                            st.markdown('IMDB Rating: ' + str(ratings) + '⭐')
            else:
                if select_movie == '--Select--':
                    st.warning('Please select Movie!!')
                else:
                    no_of_reco = st.slider(
                        '**Number of movies you want Recommended**:', min_value=5, max_value=50, step=1)

                    if st.button('Result'):
                        genres = data[movies.index(select_movie)]
                        test_points = genres
                        table = KNN_Movie_Recommender(
                            test_points, no_of_reco + 1)
                        table.pop(0)
                        c = 0
                        st.success(
                            '**Some of the movies from our Recommendation, have a look below**')
                        for movie, link, ratings in table:
                            c += 1
                            st.markdown(f"**[({c})[ {movie}]({link})]**")
                            movie_poster_fetcher(link)
                            director, cast, story, total_rat = get_movie_info(
                                link)
                            st.markdown(f"**[{director}]**")
                            st.markdown(f"**[{cast}]**")
                            st.markdown(f"**[{story}]**")
                            st.markdown(f"**[{total_rat}]**")
                            st.markdown('IMDB Rating: ' + str(ratings) + '⭐')
    elif cat_op == category[2]:
        sel_gen = st.multiselect('**Select Genres**:', genres)
        dec = st.radio("**Want to Fetch Movie Poster?**", ('Yes', 'No'))
        st.markdown(
            '''<h4 style='text-align: left; color: #d73b5c;'>* Fetching a Movie Posters will take a time."</h4>''',
            unsafe_allow_html=True)
        if dec == 'No':
            if sel_gen:
                imdb_score = st.slider('**Choose IMDb score**:', 1, 10, 8)
                no_of_reco = st.number_input(
                    '**Number of movies**:', min_value=5, max_value=20, step=1)
                if st.button('**Result**'):
                    test_point = [
                        1 if genre in sel_gen else 0 for genre in genres]
                    test_point.append(imdb_score)
                    table = KNN_Movie_Recommender(test_point, no_of_reco)
                    c = 0
                    st.success(
                        '**Some of the movies from our Recommendation, have a look below**')
                    for movie, link, ratings in table:
                        c += 1
                        st.markdown(f"**[({c})[ {movie}]({link})]**")
                        director, cast, story, total_rat = get_movie_info(link)
                        st.markdown(f"**:red[{director}]**")
                        st.markdown(f"**[{cast}]**")
                        st.markdown(f"**[{story}]**")
                        st.markdown(f"**[{total_rat}]**")
                        st.markdown('IMDB Rating: ' + str(ratings) + '⭐')
        else:
            if sel_gen:
                imdb_score = st.slider('Choose IMDb score:', 1, 10, 8)
                no_of_reco = st.number_input(
                    '**Number of movies**:', min_value=5, max_value=20, step=1)
                if st.button('Result'):
                    test_point = [
                        1 if genre in sel_gen else 0 for genre in genres]
                    test_point.append(imdb_score)
                    table = KNN_Movie_Recommender(test_point, no_of_reco)
                    c = 0
                    st.success(
                        '**Some of the movies from our Recommendation, have a look below**')
                    for movie, link, ratings in table:
                        c += 1
                        st.markdown(f"**[({c})[ {movie}]({link})]**")
                        movie_poster_fetcher(link)
                        director, cast, story, total_rat = get_movie_info(link)
                        st.markdown(f"**:red[{director}]**")
                        st.markdown(f"**[{cast}]**")
                        st.markdown(f"**[{story}]**")
                        st.markdown(f"**[{total_rat}]**")
                        st.markdown('IMDB Rating: ' + str(ratings) + '⭐')

run()
