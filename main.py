from flask import Flask, jsonify, request
import requests
from elevenlabs import generate, play
from elevenlabs import set_api_key
from dotenv import load_dotenv
import os

# Establecer la clave de la API
load_dotenv()

# Obtener la API key del archivo .env
api_key = os.getenv('API_KEY')

# Establecer la clave de la API
set_api_key(api_key)
app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def get_data():
    data = request.json 
    dataJson = {
        "text": data,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    # URL y encabezados de la solicitud a la API
    url = "https://api.elevenlabs.io/v1/text-to-speech/sAb0Zy8068WiqnbBEvIf"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "0f297a2d26e0b278be6ac8a445f3e985"
    }

    # Realizar la solicitud a la API
    response = requests.post(url, json=dataJson, headers=headers)

    # Verificar el código de respuesta de la solicitud
    if response.status_code == 200:
        # Guardar el audio en un archivo
        with open('output.mp3', 'wb') as f:
            f.write(response.content)

        # Leer el contenido del archivo como bytes
        with open('output.mp3', 'rb') as f:
            audio = f.read()

        # Reproducir el audio
        play(audio)
    else:
        return jsonify({'message': 'Error en la solicitud'})

    return jsonify({'message': 'Audio generado'})


if __name__ == '__main__':
    app.run(debug=True)
