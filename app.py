from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    description = request.form.get('description')
    if description:
        # Crie uma imagem simples com a descrição de texto
        img = Image.new('RGB', (400, 200), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        d.text((10,10), description, fill=(255,255,0), font=font)

        # Salve a imagem em um buffer
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)

        return send_file(buf, mimetype='image/png')
    else:
        return 'Descrição não fornecida', 400

if __name__ == '__main__':
    app.run(debug=True)

