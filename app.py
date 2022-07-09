from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='templates', static_url_path='/static')

def getLocation():
    search_url = 'http://ip-api.com/json/?fields=status,message,country,query'
    response = requests.get(search_url)
    print(response)

@app.route('/', methods=['GET', 'POST'])
def index():
    local = getLocation()
    return local

if __name__ == '__main__':
    app.run(debug=True)