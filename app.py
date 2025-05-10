from flask import Flask, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream)

    # Process the image and make prediction here (stub)
    result = {"object": "cup", "confidence": 0.94}

    return jsonify(result)

@app.route('/', methods=['GET'])
def home():
    return 'Flask server is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
