from flask import Flask, request, jsonify
import os
import logging
import ocr_lembar_1_v2_api
import ocr_lembar_2
import ocr_lembar_3
app = Flask(__name__)


@app.route('/ocr', methods=['POST'])
def ocr():
    data = request.json
    boxes = data.get('boxes')
    image = data.get('image')
    lembar = data.get('lembar')

    if not image or not boxes or not lembar:
        return jsonify({'error': 'Invalid input'}), 400

    logging.debug(f"Lembar: {lembar}")

    if lembar == 'lembar_1':
        grouped_predictions = ocr_lembar_1_v2_api.predict_numbers_lembar_1(boxes, image)
    elif lembar == 'lembar_2':
        grouped_predictions = ocr_lembar_2.predict_numbers_lembar_2(boxes, image)
    elif lembar == 'lembar_3':
        grouped_predictions = ocr_lembar_3.predict_numbers_lembar_3(boxes, image)
    else:
        return jsonify({'error': 'Invalid lembar value'}), 400

    logging.debug(f"Result: {grouped_predictions}")

    response = {
        'Hasil': grouped_predictions
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
