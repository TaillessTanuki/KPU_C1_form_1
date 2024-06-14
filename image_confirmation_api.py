from flask import Flask, request, jsonify
import logging
import ocr_lembar_1_v2_api
import ocr_lembar_2
import ocr_lembar_3

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json
    base64_image = data.get('base64')
    lembar = data.get('lembar')

    if not base64_image or not lembar:
        return jsonify({'error': 'Invalid input'}), 400

    logging.debug(f"Lembar: {lembar}")

    if lembar == 'lembar_1':
        boxes, result_image = ocr_lembar_1_v2_api.show_detected_boxes_lembar_1(base64_image)
    elif lembar == 'lembar_2':
        boxes, result_image = ocr_lembar_2.show_detected_boxes_lembar_2(base64_image)
    elif lembar == 'lembar_3':
        boxes, result_image = ocr_lembar_3.show_detected_boxes_lembar_3(base64_image)
    else:
        return jsonify({'error': 'Invalid lembar value'}), 400

    logging.debug(f"Result: {boxes}")

    response = {
        'boxes': boxes,
        'image': result_image
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
