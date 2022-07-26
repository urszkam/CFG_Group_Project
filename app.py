from flask import Flask, render_template, request
# from http.client import responses
# from importlib.util import module_for_loader
import requests
import pprint
import pandas as pd
import json

# app = Flask(__name__, template_folder='templates', static_url_path='/static')


# def formDetails():
#     title = request.form.get('title')
#     country = request.form.get('country').capitalize()
#     return (title, country)

pp = pprint.PrettyPrinter(indent=4)

movie_type = "series"
country = 'Spain'
title = 'Breaking Bad'

headers = {
    "X-RapidAPI-Key": "710918eac5msh667cd317416a88dp15c140jsnaeb4f681bd95",
    "X-RapidAPI-Host": "unogs-unogs-v1.p.rapidapi.com"
}


def search_netflix(title,type,headers):
    url = "https://unogs-unogs-v1.p.rapidapi.com/search/titles"
    querystring = {"order_by":"date","title":{title},"type":{type}}

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
    exact_titles.extend(similar_titles)
    return exact_titles

def get_countries(id, headers):
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


def country_data(countries, country):
    df_countries = pd.DataFrame(countries)
    countries_num = len(df_countries.index)-1
    df_countries['country'] = df_countries['country'].str.strip()
    chosen_country_data = df_countries.loc[df_countries['country'] == country]
    every_country = df_countries['country'].tolist()
    other_countries = [x for x in every_country if x != country]
    return (chosen_country_data, countries_num, other_countries)

response = search_netflix("Breaking Bad",movie_type,headers)
movies_list = movies_list(response,title)
pp.pprint(movies_list[0])

id = movies_list[0]['netflix_id']
countries = get_countries(id, headers)

chosen_country_data, countries_num, other_countries_list = country_data(countries,country)
actors_list = actors(id)




# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template(
#             'index.html')

# @app.route('/search-outcome', methods=['POST'])
# def form():
#     form_data = request.get_json()
#     title_country = json.loads(form_data)
#     title = title_country['title']
#     country = title_country['country']

#     response = search_netflix(title,movie_type,headers)
#     movies_list = movies_list(response,title)

#     return title_country

# if __name__ == '__main__':
#     app.run(debug=True)


# data to return: countries_cum, other_countries_list, actors_list
