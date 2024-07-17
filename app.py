from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

reader = None
initialized = False

def initialize_ocr():
    global reader
    reader = easyocr.Reader(['ch_sim', 'en'])

@app.route('/upload', methods=['POST'])
def upload_file():
    global initialized
    if not initialized:
        initialize_ocr()
        initialized = True

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            image = Image.open(io.BytesIO(file.read()))
            result = reader.readtext(image)

            # Extract text and confidence from OCR result
            detected_text = [{'text': text, 'confidence': confidence} for (bbox, text, confidence) in result]

            return jsonify({'detected_text': detected_text})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Unknown error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
