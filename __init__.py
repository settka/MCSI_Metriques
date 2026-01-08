from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
from collections import Counter
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html') #Comm2

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

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route('/commits/')
def commits():
    # Récupérer TOUS les commits avec pagination
    all_commits = []
    page = 1
    while True:
        response = requests.get(
            f'https://api.github.com/repos/settka/MCSI_Metriques/commits?page={page}&per_page=100'
        )
        commits_data = response.json()
        
        if not commits_data or not isinstance(commits_data, list):
            break
            
        all_commits.extend(commits_data)
        page += 1
        
        if page > 10:  # Limite de sécurité
            break
    
    # Extraire les minutes
    minutes = []
    for commit in all_commits:
        try:
            date_string = commit['commit']['author']['date']
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            minutes.append(date_object.minute)
        except:
            continue
    
    # Compter
    minute_counts = Counter(minutes)
    labels = list(range(60))
    data = [minute_counts.get(i, 0) for i in labels]
    
    total_commits = len(all_commits)
    minute_la_plus_active = max(minute_counts, key=minute_counts.get) if minute_counts else 0
    
    return render_template('commits.html', 
                          labels=labels, 
                          data=data,
                          total_commits=total_commits,
                          minute_la_plus_active=minute_la_plus_active)

@app.route('/commits/hours/')
def commits_by_hour():
    all_commits = []
    page = 1
    while True:
        response = requests.get(
            f'https://api.github.com/repos/settka/MCSI_Metriques/commits?page={page}&per_page=100'
        )
        commits_data = response.json()
        
        if not commits_data or not isinstance(commits_data, list):
            break
            
        all_commits.extend(commits_data)
        page += 1
        
        if page > 10:
            break
    
    hours = []
    for commit in all_commits:
        try:
            date_string = commit['commit']['author']['date']
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            hours.append(date_object.hour)
        except:
            continue
    
    hour_counts = Counter(hours)
    labels = [f'{i}h' for i in range(24)]
    data = [hour_counts.get(i, 0) for i in range(24)]
    
    total_commits = len(all_commits)
    heure_la_plus_active = max(hour_counts, key=hour_counts.get) if hour_counts else 0
    
    return render_template('commits_hours.html', 
                          labels=labels, 
                          data=data,
                          total_commits=total_commits,
                          heure_la_plus_active=heure_la_plus_active)

@app.route('/commits/days/')
def commits_by_day():
    all_commits = []
    page = 1
    while True:
        response = requests.get(
            f'https://api.github.com/repos/settka/MCSI_Metriques/commits?page={page}&per_page=100'
        )
        commits_data = response.json()
        
        if not commits_data or not isinstance(commits_data, list):
            break
            
        all_commits.extend(commits_data)
        page += 1
        
        if page > 10:
            break
    
    days = []
    day_names = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    
    for commit in all_commits:
        try:
            date_string = commit['commit']['author']['date']
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            days.append(date_object.weekday())
        except:
            continue
    
    day_counts = Counter(days)
    data = [day_counts.get(i, 0) for i in range(7)]
    
    total_commits = len(all_commits)
    jour_le_plus_actif = day_names[max(day_counts, key=day_counts.get)] if day_counts else 'N/A'
    
    return render_template('commits_days.html', 
                          labels=day_names, 
                          data=data,
                          total_commits=total_commits,
                          jour_le_plus_actif=jour_le_plus_actif)

@app.route('/commits/dashboard/')
def commits_dashboard():
    all_commits = []
    page = 1
    while True:
        response = requests.get(
            f'https://api.github.com/repos/settka/MCSI_Metriques/commits?page={page}&per_page=100'
        )
        commits_data = response.json()
        
        if not commits_data or not isinstance(commits_data, list):
            break
            
        all_commits.extend(commits_data)
        page += 1
        
        if page > 10:
            break
    
    minutes, hours, days = [], [], []
    
    for commit in all_commits:
        try:
            date_string = commit['commit']['author']['date']
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            minutes.append(date_object.minute)
            hours.append(date_object.hour)
            days.append(date_object.weekday())
        except:
            continue
    
    minute_data = [Counter(minutes).get(i, 0) for i in range(60)]
    hour_data = [Counter(hours).get(i, 0) for i in range(24)]
    day_data = [Counter(days).get(i, 0) for i in range(7)]
    
    day_names = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    
    return render_template('commits_dashboard.html',
                          minute_labels=list(range(60)),
                          minute_data=minute_data,
                          hour_labels=list(range(24)),
                          hour_data=hour_data,
                          day_labels=day_names,
                          day_data=day_data,
                          total_commits=len(all_commits))

if __name__ == "__main__":
  app.run(debug=True)
