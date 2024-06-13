from flask import Flask, request, jsonify
import os

app = Flask(__name__)

from ocr_lembar_1_v2_api import ocr_lembar_1
from ocr_lembar_2 import ocr_lembar_2
from ocr_lembar_3 import ocr_lembar_3

OCR_FUNCTIONS = {
    'lembar_1': lambda image_path: ocr_lembar_1(image_path, auto_continue=True),
    'lembar_2': lambda image_path: ocr_lembar_2(image_path, auto_continue=True),
    'lembar_3': lambda image_path: ocr_lembar_3(image_path, auto_continue=True)
}

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files or 'lembar' not in request.form:
        return jsonify({"error": "Please provide an image and lembar type"}), 400

    image = request.files['image']
    lembar = request.form['lembar']

    if lembar not in OCR_FUNCTIONS:
        return jsonify({"error": "Invalid lembar type"}), 400

    image_path = os.path.join('api_test', image.filename)
    image.save(image_path)

    ocr_function = OCR_FUNCTIONS[lembar]
    ocr_result = ocr_function(image_path)

    os.remove(image_path)

    return jsonify({"ocr_result": ocr_result})

if __name__ == '__main__':
    app.run(debug=True)
