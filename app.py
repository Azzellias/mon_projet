from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# Nom du fichier pour stocker les données
data_file = "esp_data.json"

# Route pour récupérer et afficher le fichier index.html
@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

# Route pour recevoir les données de l'ESP
@app.route('/updateData', methods=['GET'])
def update_data():
    temperature = request.args.get('temperature')
    humidity = request.args.get('humidity')

    if temperature and humidity:
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": request.args.get('timestamp', 'inconnu')
        }

        # Enregistrer les données dans un fichier JSON
        with open(data_file, "w") as f:
            json.dump(data, f)

        return f"Données reçues : Température = {temperature}, Humidité = {humidity}"
    else:
        return "Paramètres manquants.", 400

# Route pour récupérer les dernières données
@app.route('/getData', methods=['GET'])
def get_data():
    try:
        with open(data_file, "r") as f:
            data = json.load(f)
            return jsonify(data)
    except FileNotFoundError:
        return "Aucune donnée disponible.", 404

# Route de vérification de santé
@app.route('/health', methods=['GET'])
def health_check():
    return "Server is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))  # Utilise le port défini dans les variables d'environnement ou 80 par défaut
    app.run(host='0.0.0.0', port=port)
