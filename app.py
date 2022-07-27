from flask import Flask, render_template, request, url_for
# from http.client import responses
# from importlib.util import module_for_loader
import requests
import pandas as pd
import json

app = Flask(__name__, template_folder='templates', static_url_path='/static')

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

movie_type = "series"
headers = {
    "X-RapidAPI-Key": "710918eac5msh667cd317416a88dp15c140jsnaeb4f681bd95",
    "X-RapidAPI-Host": "unogs-unogs-v1.p.rapidapi.com"
}

def search_netflix(title,type):
    url = "https://unogs-unogs-v1.p.rapidapi.com/search/titles"
    querystring = {"order_by":"date","title":title,"type":type}

    response = requests.get(url, headers=headers, params=querystring)
    search_results = response.json()

    return search_results


def get_countries(id):
    url = "https://unogs-unogs-v1.p.rapidapi.com/title/countries"
    querystring = {"netflix_id":id}

    response = requests.get(url, headers=headers, params=querystring)
    search_results = response.json()

    return search_results['results']


def actors(id):
    url = "https://unogs-unogs-v1.p.rapidapi.com/search/people"
    querystring = {"netflix_id":id,"person_type":"Actor","limit":"10"}

    response = requests.get(url, headers=headers, params=querystring)
    search_results = response.json()

    actors_list = []
    for actor in search_results['results']:
        actors_list.append(actor['full_name'])
    return actors_list


def get_details(id):
    url = "https://unogs-unogs-v1.p.rapidapi.com/title/details"
    querystring = {"netflix_id":id}
    
    response = requests.get(url, headers=headers, params=querystring)
    search_results = response.json()

    return search_results



def read_countries():
    df = pd.read_csv('countries.csv', usecols=[0,1,2])
    return df


def getWordsInTitle(movie):
    title_lower = movie['title'].lower().strip()
    words_in_title = set(title_lower.split(" "))
    return words_in_title


def movies_list(search_results,title):
    title = title.lower().strip()
    words_in_title = set(title.split(" "))
    movies_list = search_results['results']
    exact_titles = [movie for movie in movies_list if movie['title'].lower().strip() == title]

    best_ids = set()
    for movie in exact_titles:
        best_ids.add(movie['netflix_id'])

    similar_titles = [movie for movie in movies_list if len(getWordsInTitle(movie).intersection(words_in_title)) > 0]
    similar_titles = [movie for movie in similar_titles if movie['netflix_id'] not in best_ids]

    if len(exact_titles) > 0:
        version = "exact"
    elif len(similar_titles) > 0:
        version = "similar"
    elif len(similar_titles) == 0 and len(exact_titles) == 0:
        version = "sorry"

    return (exact_titles, similar_titles, version)

def country_data(countries, country):
    df_countries = pd.DataFrame(countries)
    countries_num = len(df_countries.index)-1
    df_countries['country'] = df_countries['country'].str.strip()
    chosen_country_data = df_countries.loc[df_countries['country'] == country]
    every_country = df_countries['country'].tolist()
    available = country in every_country
    other_countries = [x for x in every_country if x != country]
    return (countries_num, other_countries, available)

# response = search_netflix("Breaking Bad",movie_type,headers)
# movies_list = movies_list(response,title)
# pp.pprint(movies_list[0])

# id = movies_list[0]['netflix_id']
# countries = get_countries(id, headers)

# chosen_country_data, countries_num, other_countries_list = country_data(countries,country)
# actors_list = actors(id)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template(
            'index.html')

@app.route('/results', methods=['GET','POST'])
def form():
    title = request.form.get('title').title().strip()
    country = request.form.get('country').title().strip()
    response = search_netflix(title,movie_type)
    exact_titles, similar_titles, version = movies_list(response,title)

    return render_template(
        'results.html', 
        title=title, 
        country=country, 
        exact=exact_titles, 
        similar=similar_titles, 
        version=version)

@app.route('/movie/<id>/<country>', methods=['GET', 'POST'])
def movie(id,country):
    countries = get_countries(id)
    details = get_details(id)
    countries_num, other_countries_list, available = country_data(countries,country)

    return render_template(
        'searchdetails.html', 
        id=id,
        country= country,
        num=countries_num,
        other=other_countries_list,
        avaliable=available,
        details=details)

@app.route('/movie/<id>/details', methods=['GET', 'POST'])
def details(id):
    actors_list = actors(id)
    details = get_details(id)
    return render_template(
        'moviedetails.html',
        actors_list=actors_list,
        details=details
    )

@app.route('/about-us', methods=['GET', 'POST'])
def about():
    return render_template(
            'about-us.html')

if __name__ == '__main__':
    app.run(debug=True)


# data to return: countries_cum, other_countries_list, actors_list
