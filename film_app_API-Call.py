import httpx 
# This loads the secret api key on .env file 
from dotenv import load_dotenv 
import os

load_dotenv()

# This is a function that outputs details about a movie given a query
def get_movie(query):
    # This is the basic url required for api calls on themovieDB.com
    url = "https://api.themoviedb.org/3/search/movie"
    key = os.getenv("IMDB_KEY")

    # Required for API calls
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {key}" 
    }   
    params = {
        "query": query,
        "language": "en-US",
    }

    # Gets response
    response = httpx.get(url, headers=headers, params=params)
        # response_cast = httpx.get(url_cast, headers=headers, params=params)

    # Converts response into json
    data = response.json() 

    movie = data['results'][0]
    movie_id = movie['id']

    url_cast = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

    response_cast = httpx.get(url_cast, headers=headers, params=params)

    data_cast = response_cast.json()

    cast_name = []
    cast_image = [] 

    for actor in data_cast['cast'][:3]:
        cast_name.append(actor['name'])
        cast_image.append(actor['profile_path'])

    for person in data_cast['crew']:
        if person['job'] == 'Director': 
            director_name = person['name']
            director_image = person['profile_path']
    
    return movie['title'], movie['poster_path'], movie['overview'], director_name, director_image, cast_name, cast_image

