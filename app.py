from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
import openai

app = Flask(__name__)
openai.api_key = "your-openai-api-key"  # Replace with your actual key

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream)

    # Process the image and make prediction here (stub)
    result = {"object": "cup", "confidence": 0.94}
    return jsonify(result)

# NEW: ChatGPT endpoint
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant that understands object layouts and spatial reasoning."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return 'Flask server is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
