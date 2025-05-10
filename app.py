from flask import Flask, request, jsonify
from PIL import Image
import io
import os
import base64
import requests
import replicate
from dotenv import load_dotenv

app = Flask(__name__)
   
load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

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

@app.route('/ask', methods=['POST'])
def ask():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    prompt = request.form.get('prompt', 'Describe this scene.')

    try:
        image_bytes = image_file.read()
        image_format = image_file.filename.split('.')[-1]
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:image/{image_format};base64,{image_base64}"

        output = replicate.run(
            "yorickvp/llava-13b:80537f9eead1a5bfa72d5ac6ea6414379be41d4d4f6679fd776e9535d1eb58bb",
            input={"image": image_url, "prompt": prompt}
        )

        # Return as plain text or json, depending on the model's output type
        return jsonify({"response": ''.join(output).strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    return 'Flask server is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
