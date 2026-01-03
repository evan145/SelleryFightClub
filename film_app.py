
#========Dependancies========================================#

# Fasthtml allows front end to be coded in python
from fasthtml import common as fh 

# Monsterui is used for formatting and making things look pretty
from monsterui import all as mui  # type: ignore 

# Used for API call
import httpx 

# This loads the secret api key on .env file 
from dotenv import load_dotenv 
import os
load_dotenv()

# Date and time stuff from calendar 
from datetime import datetime, timedelta  # noqa: E402

#===============Functions===============================================#

#  This is a function that outputs details about a movie given a query
def get_movie(query):
    # This is the basic url required for api calls on themovieDB.com
    url = 'https://api.themoviedb.org/3/search/movie'
    key = os.getenv('IMDB_KEY')

    # Required for API calls
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {key}' 
    }   
    # This is a simpler alternative to writing /query=godfather/lan=en-US
    params = {
        'query': query,
        'language': 'en-US',
    }

    # Gets response
    response = httpx.get(url, headers=headers, params=params)

    # Converts response into json
    data = response.json() 

    # This gets all info about one movie
    movie = data['results'][0]
    # This only takes the id of the movie 
    movie_id = movie['id']

    url_cast = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'

    response_cast = httpx.get(url_cast, headers=headers, params=params)
    data_cast = response_cast.json()

    cast_name = []
    cast_image = [] 
    # Because movie is a data, it can only store one value, a list has to be used for actors/directors
    # For Actors
    for actor in data_cast['cast'][:5]:
        cast_name.append(actor['name'])
        cast_image.append(actor['profile_path'])
    # For Directors
    for person in data_cast['crew']:
        if person['job'] == 'Director': 
            director_name = person['name']
            director_image = person['profile_path']
    # Returns everything 
    return movie['title'], movie['poster_path'], movie['overview'], director_name, director_image, cast_name, cast_image

# function for getting a list of browse movies
def get_browse(page=1):
    key = os.getenv('IMDB_KEY')
    url = 'https://api.themoviedb.org/3/discover/movie'

    # Required for API calls
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {key}' 
    }   
    # This is a simpler alternative to writing /query=godfather/lan=en-US
    params = {
        'language': 'en-US',
        'page': page,
        # Made the most sense but could be anything
        'sort_by': 'popularity.desc'
    }

    # Gets response
    response = httpx.get(url, headers=headers, params=params)
    # Converts response into json
    data = response.json() 

    # Finds the first item of json file and saves it 
    movies = []
    movies_image = []

    # This is the name for loop, just with movies instead of actors
    for n in data['results'][:20]: 
        movies.append(n['title']), 
        movies_image.append(n['poster_path'])
    # Returns the title, image, and overview
    return (movies, movies_image)

def day_cal():
    # Sets the date to today
    today = datetime.today()
    # Gets a list of the next 10 days 
    days = []
    for i in range(10):
        # Timedelta says that each date should be one day apart from previous 
        day = today + timedelta(days=i)
        days.append({
            # date format is day:month
            'date': day.strftime('%d-%m'),
            'day_name': day.strftime('%A'),      # Day name
            'day_num': day.strftime('%d'),       # Day number
            'month': day.strftime('%b'),         # Month name 
            'is_today': i == 0 # Aligns list at today
        })
    return days

# This is a function for the starts that light up in rating route
def make_stars(title:str, rating:int):  # noqa: F811
    # rated movies is a dictionary with {'title': rating}
    rated_movies[title] = rating
    return fh.Div(
        fh.H2('Rank this movie', cls='text-2xl font-bold mb-4 text-white'),
        fh.Div(
            # This unpacks the list of stars and colors them based on which one was clicked
            *[mui.Button(
                mui.UkIcon('star', height=25, width=25, cls='text-yellow-500' if i < rating else 'text-gray-400'), 
                    # This outsources all of the logic to the /review/{title} route
                    hx_post=f'/review/{title}/{i + 1}',
                    # Here is the id of the star container 
                    hx_target='#star-container',
                    # Swaps everything
                    hx_swap='outerHTML',
                    cls='!p-0 !m-0 !min-w-0 bg-transparent border-none hover:scale-125 transition-transform duration-200'
            ) for i in range(5)],
            cls='flex gap-2',
        ),
        fh.P(
            f'{rating} out of 5 stars' if rating > 0 else 'Click to rate',
            cls='mt-3 text-gray-400 text-sm'
        ),
        # this is where all of the stars go
        id='star-container',
        cls='bg-gray-800 rounded-xl p-6 text-center max-w-md mx-auto mt-8 shadow-lg'
    )

#================Fast HTML CODE=============================================#

# Sets the theme to blue (could be any color)
hdrs = mui.Theme.blue.headers()
# Initializes Fasthtml
app,rt = fh.fast_app(hdrs=hdrs, live=True)

#List of favorite movies 
favorite_movies = []
favorite_movies_img = []

#Dictionaries for rated movies and scheduled movies
rated_movies = {}
scheduled_movies = {}

# This is the nav bar at the top of the screen (same for each route)
navbar = mui.NavBar(
            fh.A(mui.UkIcon('search'), href='/search'),
            fh.A('Browse',href='/browse'),
            fh.A('Saved',href='/saved'),
            fh.A('Reviews',href='/all_rated_movies'),
            fh.A('Calandar',href='/calendar'),
            fh.A(mui.UkIcon('settings'), href='/under_construction'),
            brand=mui.DivLAligned(
                fh.A(mui.UkIcon('film',height=30,width=30), href='/'),
                fh.P('Sellery Fight Club')), 
                cls='bg-blue-950 px-6 py-4 shadow-lg'
                )
# This is the back to search button (to save space I used a var)
back_to_search = fh.Div(
    fh.A(
        mui.Button(
            'Back to Search',
            cls='bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-lg font-medium transition-colors duration-300'
        ),
        href='/search'
    ),
    cls='mt-8 text-center'
)

# Home directory 
@rt('/')
def get(): 
    return ( 
        navbar, 
        fh.Div(
            # Header/Top 
            fh.Div(
                fh.H1('Welcome to the', cls='text-2xl font-medium text-gray-400 mb-2'),
                fh.H1('Sellery Fight Club!', cls='text-6xl font-bold mb-6 text-white bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent'),
                fh.P('This is a private database of all of the films watched in the 10th floor lounge', 
                     cls='text-xl text-gray-400 mb-10 max-w-2xl mx-auto'),
                fh.A('Start Browsing →', href='/browse',
                     cls='bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 px-8 rounded-full inline-block hover:scale-105 transition-all duration-300 shadow-lg shadow-blue-500/30'),
                cls='text-center'
            ),
            cls='py-24 px-8 bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900'
        ),
        
        fh.Div(
            # Stats Section
            fh.Div(
                fh.Div(
                    fh.P(f'{len(favorite_movies)}', cls='text-4xl font-bold text-blue-400'),
                    fh.P('Saved Movies', cls='text-gray-400'),
                    cls='text-center'
                ),
                fh.Div(
                    fh.P(f'{len(rated_movies)}', cls='text-4xl font-bold text-yellow-400'),
                    fh.P('Rated Movies', cls='text-gray-400'),
                    cls='text-center'
                ),
                fh.Div(
                    fh.P(f'{len(scheduled_movies)}', cls='text-4xl font-bold text-green-400'),
                    fh.P('Scheduled', cls='text-gray-400'),
                    cls='text-center'
                ),
                cls='grid grid-cols-3 gap-8 max-w-2xl mx-auto'
            ),
            cls='py-12 px-8 bg-gray-800/50 border-y border-gray-700'
        ),

        # Features 
        fh.Div(
            fh.H2('Features', cls='text-3xl font-bold mb-12 text-center text-white'),
            fh.Div(
                fh.A(
                    fh.Div(
                        fh.Div(
                            mui.UkIcon('search', height=50, width=50, cls='text-blue-400'),
                            cls='mb-4 group-hover:scale-110 transition-transform duration-300'
                        ),
                        fh.H3('Search', cls='text-xl font-bold mb-2 text-white'),
                        fh.P('Find movies by query', cls='text-gray-400'),
                        cls='bg-gray-800 p-8 rounded-2xl text-center hover:bg-gray-700 transition-all duration-300 border border-gray-700 hover:border-blue-500 group h-full'
                    ),
                    href='/search',
                ),
                fh.A(
                    fh.Div(
                        fh.Div(
                            mui.UkIcon('heart', height=50, width=50, cls='text-red-400'),
                            cls='mb-4 group-hover:scale-110 transition-transform duration-300'
                        ),
                        fh.H3('Save & Rank', cls='text-xl font-bold mb-2 text-white'),
                        fh.P('Save your favorites and rank movies', cls='text-gray-400'),
                        cls='bg-gray-800 p-8 rounded-2xl text-center hover:bg-gray-700 transition-all duration-300 border border-gray-700 hover:border-red-500 group h-full'
                    ),
                    href='/saved'
                ),
                fh.A(
                    fh.Div(
                        fh.Div(
                            mui.UkIcon('calendar', height=50, width=50, cls='text-green-400'),
                            cls='mb-4 group-hover:scale-110 transition-transform duration-300'
                        ),
                        fh.H3('Calendar', cls='text-xl font-bold mb-2 text-white'),
                        fh.P('View upcoming movies in the lounge', cls='text-gray-400'),
                        cls='bg-gray-800 p-8 rounded-2xl text-center hover:bg-gray-700 transition-all duration-300 border border-gray-700 hover:border-green-500 group h-full'
                    ),
                    href='/calendar'
                ),
                cls='grid grid-cols-1 md:grid-cols-3 gap-8'
            ),
            cls='py-16 px-8 max-w-6xl mx-auto'
        ),
        # Footer/Credits
        fh.Div(
            fh.A(
                fh.Div(
                    mui.UkIcon('github', height=25, width=25, cls='text-gray-400'),
                    fh.Span('Made by Evan Blonien', cls='ml-2 text-gray-500 text-sm'),
                    cls='flex items-center justify-center hover:text-white transition'
                ),
                href='https://github.com/evan145',
                target='_blank'
            ),
            cls='py-8 text-center border-t border-gray-800'
        )
    )

# Browse page 
@rt('/browse')
        # This sets the page as the first page
def get(page: int = 1):  # noqa: F811
    # Calls the get_browse function 
    movies, movies_image = get_browse(page=page)
    return(
        navbar, 
        fh.Div(
            fh.Div(
                fh.H1('Browse Movies', cls='text-4xl font-bold'),
                cls='text-center py-8'
            )),
        fh.Div(
            # The * upacks the list [red, orange, blue] -> 1 arguement, *[red, orange, blue] -> 3 arguements
            *[fh.Div(
                fh.Img(
                    src=f'https://image.tmdb.org/t/p/w185/{movies_image[n]}', 
                    cls='rounded-lg shadow-lg hover:scale-105 transition duration-300 mx-auto'
                ),
                fh.A(
                    movies[n], 
                    # Creates a link to the search page for each individual movie
                    href=f'/search?movie_selection={movies[n]}', 
                    cls='block mt-2 text-sm text-gray-300 text-center hover:text-blue-400 hover:underline transition'
                # Instead of writing 'for n in len(movies)(): print(m), this says print(m) for n in len(movies)'
                 # Python won't allow fh.Group in for loop 
                ) if movies[n] else None,
                cls='text-center bg-gray-800 p-4 rounded-xl hover:bg-gray-700 transition-colors duration-300'
            ) for n in range(len(movies))], 
            cls='grid grid-cols-5 gap-6 p-8'
        ),
        fh.Div(
            fh.A(
                # undo button
                mui.UkIcon('undo', height=30, width=30), 
                # this creates a link to the previous browsing page
                href=f'/browse?page={page - 1}', 
                # CSS stuff
                cls='mx-4 p-2 rounded-full hover:bg-gray-700 transition'
            ) if page > 1 else None,
            # fh.Span is not semantic and is only used for styling
            fh.Span(f'Page {page}', cls='text-lg font-medium'),
            fh.A(
                mui.UkIcon('forward', height=30, width=30), 
                # thsi creates a link to the next browsing page
                href=f'/browse?page={page + 1}', 
                cls='mx-4 p-2 rounded-full hover:bg-gray-700 transition'
            ),
            cls='flex justify-center items-center py-6'
        )
    )

@rt('/search')
# Sets the movie selection value as an empty string 
def get(movie_selection: str=''):  # noqa: F811 (# noqa: F811 is used because otherwise my code says there's an error)
    return(
        navbar,
        fh.Div(
            # Title 
            fh.H1('Search Movies', cls='text-4xl fond-bold text-center mb-2'),
            fh.Div(
                mui.Form(
                    # This is the text box for searching movies
                    mui.Input(
                        name='movie_selection', 
                        placeholder='search for a movie', 
                        value = movie_selection, 
                        id='input', 
                        required=True, 
                        type='text', 
                        cls='w-full p-4 text-lg rounded-lg bg-gray-800 border border-gray-600 focus:border-blue-500 focus:outline-none'
                        ), 
                    # This puts the results of the text input into @rt('/results')
                    hx_post='/results',
                    # Put the results of get_list into id=results (when hashtag is used that means id)
                    hx_target='#results',
                    # This loads the page if there is a movie selection (enter key pressed)
                    hx_trigger='load' if movie_selection else None,
                    cls='w-full'
                    ),
                cls='max-w-xl mx-auto px-6'
            ), 
            # Where the results of get_list go
            fh.Div(
                # this is '#results'
                id='results',
                cls='mt-8 px-6'
            ),
            cls='py-12',
        )
    )

@rt('/results')
# (POST = put information somewhere), movie_selection is a string
def Form(movie_selection: str):
    # first output = var:title, second output = var:poster_path, etc ... 
    title, poster_path, overview, director_name, director_image, cast_name, cast_image = get_movie(movie_selection)
    # This variable is used to check if a movie is already favorited by saving only the title from the favorite_movies dict 
    is_favorited = title in favorite_movies

    return (
        # Div = HTML Tag (this thing: <tag>)
        fh.Div(
            # Movie info
            fh.Div( 
                # Movie poster
                fh.Div(
                    # f-string url to get the poster image 
                    fh.Img(src=f'https://image.tmdb.org/t/p/w185/{poster_path}', cls='rounded-lg shadow-lg'),
                    fh.Div(
                        # Gives the title and overview
                        fh.Group(
                            fh.H1(title, cls='text-3xl fond-bold mb-4'),
                            mui.Button(
                                # mui.UKIcon is a list of icons that are included in Monster UI
                                mui.UkIcon('heart', height=25, width=25, 
                                cls='text-red-500' if is_favorited else 'text-gray-400',
                                ), 
                                # Calls the /toggle-favorite route to add/subtract movies from favorite list 
                                hx_post = f'/toggle-favorite/{title}?poster_path={poster_path}',
                                # Swaps everything 
                                hx_swap = 'outerHTML',
                                cls = 'w-12 h-12 flex items-center justify-center bg-transparent border-none'
                            ), 
                            fh.A(
                                mui.Button(
                                    'Review', 
                                    cls='text-red-500' if is_favorited else 'text-gray-400',
                                    ),
                                # This button redirects to the review page 
                                href=f'/review/{title}?poster_path={poster_path}'
                            ),
                            fh.A(
                                mui.Button(
                                    '📅', 
                                    ),
                                # This button redirects to the schedule page 
                                href=f'/schedule/{title}'

                            )
                        ),
                        fh.P(overview, cls='text-gray-300 leading-relaxed'),
                        cls='ml-6 flex-1'
                    ), 
                    cls='flex items-start mb-8'
                ),
                cls='px-6 py-4'
            ), 
    
            fh.Div(
                # This is the part of the page that lists the actors/directors
                fh.H2('Director', cls='text-2xl font-bold mb-4'),
                fh.Div(
                    # f-string url to get the director image 
                    # There is only one director so the list does not need to be unpacked
                    fh.Img(src=f'https://image.tmdb.org/t/p/w185/{director_image}', cls='w-24 h-auto rounded-lg'),
                    # gives director name 
                    fh.P(director_name, cls='mt-2 text-center font-medium'),
                    cls='inline-block text-center'
                    ), 
                    cls='px-6 py-4 border-t border-gray-700'
                ),

                fh.Div(
                    fh.H2('Cast', cls='text-2xl font-bold mb-4'),
                    fh.Div(
                        # The * upacks the list [red, orange, blue] -> 1 arguement, *[red, orange, blue] -> 3 arguements
                        # Unpacks all of the actors' names and their photos 
                        *[fh.Div(
                            # for each actor, gives the cast_image (if it exists) and the name of the actor
                            fh.Img(src=f'https://image.tmdb.org/t/p/w185/{cast_image[n]}', cls='w-24 h-auto rounded-lg mx-auto') if cast_image[n] else None,
                            fh.A(cast_name[n], cls='mt-2 text-center text-sm text-gray-300 hover:text-blue-400 transition'),
                            cls='text-center'  
                            # Instead of writing 'for n in len(movies)(): print(m), this says print(m) for n in len(movies)'
                            # Python won't allow fh.Group in for loop 
                            ) for n in range(len(cast_name))], 
                            cls='grid grid-cols-5 gap-4'
                        ),

                        cls='px-6 py-4 border-t border-gray-700'
                    ), 

                    cls='max-w-4xl mx-auto',
                ),

                # This resets the text box 
                mui.Input(
                    name='movie_selection', 
                    id='input', 
                    placeholder='search for a movie', 
                    required=True, 
                    type='text', 
                    # id attribute relplaces id attribute
                    # oob stands for 'out-of-band' 
                    hx_swap_oob='true',
                    cls='w-full p-4 text-lg rounded-lg bg-gray-800 border border-gray-600 focus:border-blue-500 focus:outline-none'
                )
            )

@rt('/toggle-favorite/{title}')
def post(title:str, poster_path: str):  # noqa: F811
    # If the title is already in favorite_movies remove it
    if title in favorite_movies: 
        favorite_movies.remove(title)
        favorite_movies_img.remove(poster_path)
        is_favorited = False
    # If the title in not in favorite_movies, add it
    else:
        favorite_movies.append(title)
        favorite_movies_img.append(poster_path)
        is_favorited = True

    # Returns the heart button (it is red if favorited)
    return  mui.Button(
                mui.UkIcon('heart', height=25, width=25, 
                cls='text-red-500' if is_favorited else 'text-gray-400',
                ), 
                hx_post = f'/toggle-favorite/{title}?poster_path={poster_path}',
                hx_swap = 'outerHTML',
                cls = 'w-12 h-12 flex items-center justify-center bg-transparent border-none'
            ), 

# Here is the page with all of the saved movies
@rt('/saved')
def get():  # noqa: F811
    return(
    navbar,
    fh.Div(
        fh.H1('Saved Movies', cls='text-3xl font-bold mb-8 text-white'),
        fh.Div(
            # Unpacks the favorite_movies list
            *[fh.Div(
                fh.Div(   
                    fh.Img(
                        src=f'https://image.tmdb.org/t/p/w185/{poster_path}',
                        cls='w-full rounded-lg shadow-lg group-hover:opacity-75 transition-opacity duration-300'
                    ),
                    cls='relative overflow-hidden rounded-lg'
                ),
                fh.A(
                    fh.P(title, cls='mt-3 text-center font-medium text-white group-hover:text-blue-400 transition-colors'),
                    href=f'/search?movie_selection={title}'
                ),
                cls='bg-gray-800 rounded-xl p-4 hover:bg-gray-700 transition-colors duration-300 group'
                # This combines the title and the movie poster so it looks like one card
            )  for title, poster_path in zip(favorite_movies, favorite_movies_img)],
                cls='grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6'
        ) if favorite_movies else fh.P('No Saved Movies Yet', cls='text-gray-400 text-lg'),
        back_to_search,
        cls='p-8 max-w-7xl mx-auto'
    ),
)

# This is the rating page that pops up for each movie that is clicked
@rt('/review/{title}')
def get(title:str, poster_path: str):  # noqa: F811
    # Sets the current rating to zero for each title
    current_rating = rated_movies.get(title, 0)
    return(
    navbar,
    fh.Div(
        fh.Div(
            fh.Img(src=f'https://image.tmdb.org/t/p/w185/{poster_path}',
                   cls='rounded-xl shadow-2xl'
                ),
                cls='flex justify-center'
            ),
            fh.H1(title, cls='text-3xl font-bold mt-6 text-center text-white'),
            fh.Div(
                # This is the function that gives the stars
                make_stars(title, current_rating),
                cls='mt-6'
            ),
        fh.Div(
            fh.A(
                # This brings the user back to the search page for that movie
                mui.Button(
                    'Back to Search',
                    cls='bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-lg font-medium transition-colors duration-300'
                ),
                href=f'/search?movie_selection={title}',
                cls='hover:text-blue-400 transition'
            ),
            cls='mt-8 text-center'
        ),
        cls='bg-gray-800 rounded-2xl p-8 shadow-xl max-w-md mx-auto mt-8'
    ),
)

# This is the intermediary between the review page and the get_stars function
@rt('/review/{title}/{star}')
def post(title:str, star:int):  # noqa: F811
    rated_movies[title] = star
    return make_stars(title, star)

# This is the page that lists all of the movies that were ranked and their rankings
@rt('/all_rated_movies')
def get():  # noqa: F811
    return(
    navbar, 
        fh.Div(
            fh.H1('Rated Movies', cls='text-3xl font-bold mb-8 text-white'),
            fh.Div(
                *[fh.Div(   
                    fh.A(
                        fh.Div(
                            fh.P(title, cls='text-white font-medium text-lg'),
                            fh.P('⭐' * rating + '☆' * (5-rating), cls='text-yellow-500'), 
                        ),
                        href=f'/search?movie_selection={title}'
                    ),
                    cls='bg-gray-800 rounded-xl p-4 hover:bg-gray-700 transition-colors duration-300'
                # This outputs each movie and rating in the rated_movies dict 
                ) for title, rating in rated_movies.items()],
                cls='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4'
            ) if rated_movies else fh.P('No rated movies yet',  cls='text-gray-400 text-lg'),
            back_to_search,
            cls='p-8 max-w-7xl mx-auto'
        ) 
    )

@rt('/calendar')
def get():  # noqa: F811
    # gets the 10 next days from day_cal function
    days = day_cal()
    # sets the day_cards as empty list 
    day_cards = []
    # Checks to see if there is an event in the range of day
    for i, day in enumerate(days):
        # This gets the date from the scheduled_movies dict
        events = scheduled_movies.get(day['date'], [])
         # creates a card of the Day, Month, day number
        card = fh.Div(
            fh.P(day['day_name'], cls='font-bold text-lg text-white'),
            fh.P(f'{day['month']} {day['day_num']}', cls='text-3xl font-bold text-white'),
            # This unpacks each movie in the scheduled_movies dict 
            *[fh.A(
                movie['title'], 
                href=f'/search?movie_selection={movie['title']}', 
                cls='text-sm text-gray-300 mt-2 hover:text-blue-400 hover:underline block transition'
            # Unpacks the dict for every movie 
             ) for movie in events] if events else [], 
              cls=f'p-4 rounded-xl text-center {'bg-blue-600 ring-2 ring-blue-400' if day['is_today'] else 'bg-gray-800'} hover:bg-blue-500 transition-all duration-300 min-h-32'
        )
        # Adds each card to a list 
        day_cards.append(card)
    
    return (
        navbar,
        fh.Div(
            fh.H2('Upcoming Movies', cls='text-2xl font-bold mb-4'),
            fh.Div(
                # unpacks the list of cards
                *day_cards,
                cls='grid grid-cols-5 gap-4'
            ),
            cls='p-6'
        )
    )

# This is the page that allows the user to schedule viewings for each individual movie
@rt('/schedule/{title}')
def get(title:str):  # noqa: F811
    # sets days equal to the day_cal()
    days = day_cal()
    return(
    navbar,
        fh.Div(
            fh.H1(f'Schedule viewing for: {title}', cls='text-2xl font-bold mb-6'),
            fh.Form(
                fh.P('Select a day:', cls='mb-4'),
                fh.Div(
                    # Creates a card that has the day, day number, and month for each of the 10 days
                    *[fh.Button(
                        fh.Div(
                            fh.P(day['day_name'][:3], cls='text-xs uppercase tracking-wide'),
                            fh.P(day['day_num'], cls='text-xl font-bold'),
                            fh.P(day['month'], cls='text-xs')
                        ),
                        name = 'selected_date',
                        value=day['date'],
                        type='submit',
                        cls=f'p-4 rounded-xl {'bg-blue-600 ring-2 ring-blue-400' if day['is_today'] else 'bg-gray-800'} hover:bg-blue-500 hover:scale-105 transition-all duration-200 min-w-16'
                    ) for day in days],
                    cls='flex gap-2 overflow-x-auto'
                ),
                # This outsources the list of the scheduled movies to another route
                hx_post=f'/schedule/{title}',
                # Puts the results into the confirmation id
                hx_target='#confirmation',
                # Only replaces inside of id, not entire id
                hx_swap='innerHTML'
            ),   
            fh.Div(id='confirmation', cls='mt-6'),
            cls='p-8 max-w-4xl mx-auto'
        )
    ) 

# This is where the outsourced work in the schedule route goes
# This is done because it uses a post function and makes code easier to read
@rt('/schedule/{title}')
def post(title:str, selected_date:str):  # noqa: F811
    # If a date does not already have a list, create one
    # This allows multiple movies to be under the same date 
    if selected_date not in scheduled_movies: 
        scheduled_movies[selected_date] = []
    # Checks for any duplicates than adds that movie to the list 
    if not any(n['title'] == title for n in scheduled_movies[selected_date]):
        scheduled_movies[selected_date].append({'title': title})
    
    return(
        fh.Div(
            fh.P(f'✓{title} scheduled for {selected_date}', cls='text-green-500 text-lg'),
            fh.A('View calendar', href='/calendar', cls='text-gray-300 hover:text-blue-400 underline mt-2 block transition')
        )
    )

# under construction page
@rt('/under_construction')
def get():  # noqa: F811
    return(
        navbar,
        fh.Div(
            fh.Div(
                mui.UkIcon('construction', height=80,width=80, cls='text-yellow-500 mb-6'),
                fh.H1('Under Construction', cls='text-4xl font-bold mb-4'),
                fh.A('← Back to Home', href=('/'), cls='bg-blue-600 hover:bg-blue-700 text-white py-3 px-6 rounded-lg'),
                cls='text-center' 
            ),
            cls='flex items-center justify-center min-h-[70vh]'
        )
    )
# Runs the code
fh.serve()