# Sellery Fight Club
## This is a film website that I created using TMDB (an open source movie database like IMDB) and FastHTML and MonsterUI 
#### At my university dorm there is a common room for watching movies and this website/program was made to help people organize watch parties and to create a database of the movie prefrences of just college students (instead of every person, like on IMDB). 

### How it works: 
1. The movie database (TMDB) has API documentation that gives you a api url and a private API key for free 
   1. https://developer.themoviedb.org/docs/getting-started
2. Using that url and key, my program calls a list of movies, actors, directors, and images and stores them in their individual lists
   1. (Just the API of this project is in the film_app_API-call.py program)
3. Then I use fastHTML to create a local webpage just within the python file
   1. This works because fastHTML is super abstracted and uses web-features like uvicorn and HTMX to do all of the front-end
   2. https://fastht.ml/about/
The entire application is written by combining the API call with fasthtml in different ways. 
