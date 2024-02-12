from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)    
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2

@app.route("/contact/")
def contact():
    return render_template("contact.html")
  
@app.route("/submit_message/", methods=["POST"])
def submit_message():
    # Traitement de la soumission du formulaire (non implémenté dans cet exercice)
    return "Message soumis avec succès!"

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    
    print(results)  # Imprimez les données récupérées
    
    return render_template("histogramme.html", results=results)


# Route pour extraire le nombre de minutes à partir d'une date formatée
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Route pour afficher le nombre de commits par minute
@app.route('/commits/')
def commits():
    # Appel à l'API de GitHub pour extraire les données sur les commits
    response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    commits_data = json.loads(response.read().decode('utf-8'))

    # Initialiser un dictionnaire pour compter le nombre de commits par minute
    commits_per_minute = {}
    for commit in commits_data:
        # Extraire la date du commit et convertir en minute
        commit_date = commit['commit']['author']['date']
        commit_minute = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ').minute

        # Incrémenter le compteur de commits pour cette minute
        commits_per_minute[commit_minute] = commits_per_minute.get(commit_minute, 0) + 1

    # Préparer les données pour le graphique
    data = [{'minute': minute, 'commits': count} for minute, count in commits_per_minute.items()]

    return jsonify(data)

  
if __name__ == "__main__":
  app.run(debug=True)
