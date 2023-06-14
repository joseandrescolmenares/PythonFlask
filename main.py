from flask import Flask, jsonify, request
import requests
from elevenlabs import generate
from io import BytesIO
from pydub import AudioSegment
import simpleaudio as sa

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
        # Leer el contenido de la respuesta como bytes
        audio_bytes = BytesIO(response.content)

        # Convertir los bytes de audio a objeto de AudioSegment de pydub
        audio_segment = AudioSegment.from_file(audio_bytes, format="mp3")

        # Convertir el objeto AudioSegment a bytes
        audio_data = audio_segment.export(format="wav").read()

        # Reproducir el audio utilizando simpleaudio
        play_obj = sa.play_buffer(audio_data, num_channels=2, bytes_per_sample=2, sample_rate=44100)
        play_obj.wait_done()
    else:
        return jsonify({'message': 'Error en la solicitud'})

    return jsonify({'message': 'Audio generado'})

if __name__ == '__main__':
    app.run(debug=True)
