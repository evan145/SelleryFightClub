import requests
import json 
import os 
import subprocess

url = "https://api.themoviedb.org/3/search/movie"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhNWU1NmM5NWQ2ZWYxYjM1NDA4ZmZiOTY1ZTUzMjBjZSIsIm5iZiI6MTc2MDMzMDcwNi44Niwic3ViIjoiNjhlYzgzZDJkNTMzOGM5YjIyNzg0ZDM5Iiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.Qaf1tWCCoDJjIFha_-HEYFt21gU8QaEpK8kWajY20ks"
}

params = {
    "query": "Your Name",
    "include_adult": "false",
    "language": "en-US",
    "page": 1
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

movie = data['results'][0]
image_path = movie['backdrop_path']
image_url = f"https://image.tmdb.org/t/p/original{image_path}"
print(image_url)
print(f"Release Date: {movie['release_date']}")
print(f"Overview: {movie['overview']}")  

# ==============================================================================

 