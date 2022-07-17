# from flask import Flask, render_template, request
# from http.client import responses
# from importlib.util import module_for_loader
import requests
import pprint

# app = Flask(__name__, template_folder='templates', static_url_path='/static')


# def formDetails():
#     title = request.form.get('title')
#     country = request.form.get('country')
#     return (title, country)


def searchNetflix(title):
    url = "https://unogs-unogs-v1.p.rapidapi.com/search/titles"

    querystring = {"order_by":"date","title":{title},"type":"series"}

    headers = {
        "X-RapidAPI-Key": "710918eac5msh667cd317416a88dp15c140jsnaeb4f681bd95",
        "X-RapidAPI-Host": "unogs-unogs-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    search_results = response.json()

    return search_results

def getWordsInTitle(movie):
    title_lower = movie['title'].lower().strip()
    words_in_title = set(title_lower.split(" "))
    return words_in_title

pp = pprint.PrettyPrinter(indent=4)

# pp.pprint(searchNetflix("breaking bad"))
title = 'Breaking Bad'
title = title.lower().strip()
words_in_title = set(title.split(" "))
print(words_in_title)

response = searchNetflix("Breaking Bad")
# pp.pprint(response['results'])



movies_list = response['results']

exact_titles = [movie for movie in movies_list if movie['title'].lower().strip() == title]

best_ids = set()
for movie in exact_titles:
    best_ids.add(movie['netflix_id'])

print(best_ids)
similar_titles = [movie for movie in movies_list if len(getWordsInTitle(movie).intersection(words_in_title)) > 0]

similar_titles = [movie for movie in similar_titles if movie['netflix_id'] not in best_ids]
exact_titles.extend(similar_titles)

for s in exact_titles:
    pp.pprint(s['title'])

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         title, country = formDetails()y
#         searchNetflix()
#         return render_template(
#             'index.html', movie_details)

# if __name__ == '__main__':
#     app.run(debug=True)


