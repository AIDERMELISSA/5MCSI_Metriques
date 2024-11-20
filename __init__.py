from flask import Flask, render_template, jsonify
from urllib.request import urlopen
import json

app = Flask(__name__)

# Route pour la page de contact
@app.route("/contact/")
def contact():
    return "<h2>Ma page de contact</h2>"

# Route pour afficher un graphique
@app.route("/rapport/")
def graphique():
    return render_template("graphique.html")

# Route pour afficher les données météorologiques de Tawarano
@app.route('/tawarano/')
def meteo():
    # Remplacez 'xxx' par votre clé API valide
    api_url = 'https://api.openweathermap.org/data/2.5/forecast?lat=35&lon=139&appid=xxx'
    try:
        response = urlopen(api_url)
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        results = []
        for list_element in json_content.get('list', []):
            dt_value = list_element.get('dt')
            temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
            results.append({'Jour': datetime.utcfromtimestamp(dt_value).strftime('%Y-%m-%d %H:%M:%S'), 
                            'temp': round(temp_day_value, 2)})
        return jsonify(results=results)
    except Exception as e:
        return jsonify(error=str(e))

# Route pour une page d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')

if __name__ == "__main__":
    app.run(debug=True)
