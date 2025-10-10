from flask import Flask, render_template, jsonify
from flask import json
from datetime import datetime
from urllib.request import urlopen, Request
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/histogramme/")
def monhisto():
    return render_template("histogramme.html")

@app.route("/rapport/")
def mongraphique():
    return render_template("histogramme.html")

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


@app.route('/commits/data')
def commits_data():
    # Repo source de l’énoncé (tu peux remplacer par ton fork : owner/repo)
    owner = "OpenRSI"
    repo = "5MCSI_Metriques"
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=100"

    req = Request(api_url, headers={"User-Agent": "metrics-app"})
    with urlopen(req) as resp:
        raw = resp.read()
    payload = json.loads(raw.decode("utf-8"))

    minute_counts = [0] * 60
    for item in payload:
        commit_info = item.get('commit', {})
        author_info = commit_info.get('author', {})
        date_str = author_info.get('date')  # ex: "2024-02-11T11:57:27Z"
        if not date_str:
            continue
        try:
            d = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute_counts[d.minute] += 1
        except Exception:
            continue

    results = [{'minute': i, 'count': minute_counts[i]} for i in range(60)]
    return jsonify(results=results)


@app.route('/commits/')
def commits_page():
    return render_template('commits.html')


  
if __name__ == "__main__":
  app.run(debug=True)
