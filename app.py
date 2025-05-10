from flask import Flask, request, jsonify
from PIL import Image
import io
import os
import base64
import requests
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

@app.route('/blip', methods=['POST'])
def blip_caption():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    prompt = request.form.get('prompt', 'Describe this scene.')

    # Convert image to base64
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/png;base64,{image_base64}"

    # Prepare Replicate payload
    headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}"}
    json_data = {
        "version": "f677695e5e89f8b236e52ecd1d3f01beb44c34606419bcc19345e046d8f786f9",  # BLIP-2
        "input": {
            "image": image_url,
            "prompt": prompt
        }
    }

    # Call Replicate
    response = requests.post("https://api.replicate.com/v1/predictions", json=json_data, headers=headers)
    if response.status_code != 201:
        return jsonify({"error": "Replicate API error", "details": response.json()}), 500

    prediction = response.json()
    output_url = prediction['urls']['get']

    # Poll result
    while prediction["status"] not in ["succeeded", "failed"]:
        r = requests.get(output_url, headers=headers)
        prediction = r.json()

    if prediction["status"] == "succeeded":
        result = prediction["output"]
        return jsonify({"caption": result})
    else:
        return jsonify({"error": "Prediction failed"}), 500

@app.route('/', methods=['GET'])
def home():
    return 'Flask server is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
