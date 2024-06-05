from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import logging

app = Flask(__name__)
model = load_model('flower_classifier.h5')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.error('Nenhum arquivo encontrado na requisição')
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        app.logger.error('Nenhum arquivo selecionado')
        return jsonify({'error': 'No selected file'})
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        app.logger.info(f'Arquivo salvo em: {file_path}')

        try:
            img = image.load_img(file_path, target_size=(150, 150))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            app.logger.info('Imagem carregada e processada corretamente')

            prediction = model.predict(img_array)
            predicted_class = np.argmax(prediction, axis=1)[0]
            app.logger.info(f'Predição realizada: {predicted_class}')

            # Mapear a classe prevista para um nome de classe
            class_names = ["Classe 1", "Classe 2", "Classe 3", "Classe 4", "Classe 5"]
            classname = class_names[predicted_class]

            return jsonify({'classname': classname})
        except Exception as e:
            app.logger.error(f'Erro ao processar a imagem: {e}')
            return jsonify({'error': 'Erro ao processar a imagem'})

if __name__ == '__main__':
    app.run(debug=True)
